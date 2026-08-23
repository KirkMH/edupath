import urllib.request
import urllib.error
import urllib.parse
import json
from django.conf import settings

class OnetWebService:
    
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = getattr(settings, 'ONET_API_KEY', '')
        self._headers = {
            'User-Agent': 'python-OnetWebService/2.00 (bot)',
            'X-API-Key': api_key,
            'Accept': 'application/json'
        }
        self.set_version()
    
    def set_version(self, version = None):
        if version is None:
            self._url_root = 'https://api-v2.onetcenter.org/'
        else:
            self._url_root = 'https://api-v' + version + '.onetcenter.org/'
    
    def call(self, path, *query):
        try:
            url = self._url_root + path
            if len(query) > 0:
                url += '?' + urllib.parse.urlencode(query, True)
            req = urllib.request.Request(url, None, self._headers)
            handle = None
            try:
                handle = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                if e.code == 422:
                    try:
                        return json.load(e)
                    except json.JSONDecodeError:
                        return { 'error': 'Call to ' + url + ' failed to return valid JSON' }
                    except UnicodeDecodeError:
                        return { 'error': 'Call to ' + url + ' failed to return valid UTF-8' }
                else:
                    return { 'error': 'Call to ' + url + ' failed with error code ' + str(e.code) }
            except urllib.error.URLError as e:
                return { 'error': 'Call to ' + url + ' failed with reason: ' + str(e.reason) }
            code = handle.getcode()
            if (code != 200) and (code != 422):
                return { 'error': 'Call to ' + url + ' failed with error code ' + str(code),
                        'urllib2_info': handle }
            try:
                return json.load(handle)
            except json.JSONDecodeError:
                return { 'error': 'Call to ' + url + ' failed to return valid JSON' }
            except UnicodeDecodeError:
                return { 'error': 'Call to ' + url + ' failed to return valid UTF-8' }
        except Exception as e:
            return { 'error': 'Call failed with unexpected error', 'exception': e }


RIASEC_AREA_MAP = {
    'realistic': 'R',
    'investigative': 'I',
    'artistic': 'A',
    'social': 'S',
    'enterprising': 'E',
    'conventional': 'C',
}

def sync_interest_questions():
    """
    Fetches the 60 Interest Profiler questions from O*NET Web API
    and uses get_or_create (checking riasec_area & question_text)
    to populate the InterestQuestion model.
    """
    from customization.models import InterestQuestion

    service = OnetWebService()
    response = service.call('mnm/interestprofiler/questions', ('start', 1), ('end', 60))

    if isinstance(response, dict) and 'question' in response:
        questions_data = response.get('question', [])
        for q in questions_data:
            index = q.get('index')
            raw_area = str(q.get('area', '')).lower()
            riasec_area = RIASEC_AREA_MAP.get(raw_area, raw_area[0].upper() if raw_area else 'R')
            text = str(q.get('text', '')).strip()

            if text and index is not None:
                # Check for existence using riasec_area and question_text combination
                obj, created = InterestQuestion.objects.get_or_create(
                    riasec_area=riasec_area,
                    question_text=text,
                    defaults={
                        'item_number': index,
                        'status': True
                    }
                )
                if not created and obj.item_number != index:
                    obj.item_number = index
                    obj.save(update_fields=['item_number'])

    return InterestQuestion.objects.filter(status=True).order_by('item_number')


def get_riasec_results(student_profile):
    """
    Fetches RIASEC scores by sending student interest response ratings (item 1-60)
    to O*NET API mnm/interestprofiler/results?answers=[answerString].
    """
    from .models import StudentInterestResponse
    from customization.models import InterestQuestion

    all_questions = InterestQuestion.objects.filter(status=True).order_by('item_number')
    existing_responses = {
        resp.question.item_number: resp.rating
        for resp in StudentInterestResponse.objects.filter(student=student_profile).select_related('question')
    }

    # Build 60-character answer string in question item_number order
    answer_chars = []
    for q in all_questions:
        item_num = q.item_number
        rating = existing_responses.get(item_num, 3)  # default rating 3 if missing
        answer_chars.append(str(rating))

    answer_string = "".join(answer_chars)

    service = OnetWebService()
    api_response = service.call('mnm/interestprofiler/results', ('answers', answer_string))

    riasec_dict = {
        'r_score': 0,
        'i_score': 0,
        'a_score': 0,
        's_score': 0,
        'e_score': 0,
        'c_score': 0,
        'riasec_code': 'R-I-A'
    }

    field_map = {
        'realistic': 'r_score',
        'investigative': 'i_score',
        'artistic': 'a_score',
        'social': 's_score',
        'enterprising': 'e_score',
        'conventional': 'c_score',
    }

    code_map = {
        'realistic': 'R',
        'investigative': 'I',
        'artistic': 'A',
        'social': 'S',
        'enterprising': 'E',
        'conventional': 'C',
    }

    scored_areas = []

    if isinstance(api_response, dict):
        # 1. Primary parsing from 'result' list of interest dictionaries
        if 'result' in api_response and isinstance(api_response['result'], list) and len(api_response['result']) > 0:
            for item in api_response.get('result', []):
                code_key = str(item.get('code', '')).lower()
                try:
                    score_val = int(item.get('score', 0))
                except (ValueError, TypeError):
                    score_val = 0
                if code_key in field_map:
                    riasec_dict[field_map[code_key]] = score_val
                    scored_areas.append((code_map[code_key], score_val))

        # 2. Fallback parsing from 'careers' URL query parameters if 'result' list was not available
        elif 'careers' in api_response and isinstance(api_response['careers'], str):
            parsed_url = urllib.parse.urlparse(api_response['careers'])
            query_params = urllib.parse.parse_qs(parsed_url.query)
            for code_key, field_name in field_map.items():
                if code_key in query_params:
                    try:
                        score_val = int(query_params[code_key][0])
                    except (ValueError, TypeError, IndexError):
                        score_val = 0
                    riasec_dict[field_name] = score_val
                    scored_areas.append((code_map[code_key], score_val))

    if scored_areas:
        # Sort by score descending; tie-breaker: order in RIASEC
        tie_break_order = {'R': 0, 'I': 1, 'A': 2, 'S': 3, 'E': 4, 'C': 5}
        scored_areas.sort(key=lambda x: (-x[1], tie_break_order.get(x[0], 9)))
        top_codes = [area[0] for area in scored_areas[:3]]
        riasec_dict['riasec_code'] = "-".join(top_codes)

    return riasec_dict



def calculate_aptitude_dimension_scores(student_profile):
    """
    Calculates percentage score (0-100) for each of the 6 aptitude dimensions:
    numerical, logical, problem_solving, spatial, technical, verbal.
    """
    from .models import StudentAptitudeResponse
    from customization.models import AptitudeQuestion

    dimension_field_map = {
        'Numerical Reasoning': 'numerical_score',
        'Logical Reasoning': 'logical_score',
        'Problem-Solving': 'problem_solving_score',
        'Spatial Ability': 'spatial_score',
        'Technical/Mechanical Reasoning': 'technical_score',
        'Verbal/Communication Ability': 'verbal_score',
    }

    aptitude_scores = {field: 0 for field in dimension_field_map.values()}

    responses = StudentAptitudeResponse.objects.filter(student=student_profile).select_related('question')
    responses_by_dim = {}
    for resp in responses:
        dim = resp.question.dimension
        if dim not in responses_by_dim:
            responses_by_dim[dim] = []
        responses_by_dim[dim].append(resp.is_correct)

    for dim_name, field_name in dimension_field_map.items():
        dim_questions_count = AptitudeQuestion.objects.filter(dimension=dim_name, status=True).count()
        user_resps = responses_by_dim.get(dim_name, [])
        correct_count = sum(1 for is_correct in user_resps if is_correct)

        if dim_questions_count > 0:
            percentage = round((correct_count / dim_questions_count) * 100)
        elif len(user_resps) > 0:
            percentage = round((correct_count / len(user_resps)) * 100)
        else:
            percentage = 0

        aptitude_scores[field_name] = min(100, max(0, percentage))

    return aptitude_scores


def calculate_program_recommendations(student_profile, aptitude_scores, riasec_scores):
    """
    Evaluates all Programs using ProgramCriteria weights and thresholds to rank
    the top 3 recommended degree programs and overall alignment level.
    """
    from customization.models import Program, ProgramCriteria

    dim_to_student_score = {
        'Numerical Reasoning': aptitude_scores.get('numerical_score', 0),
        'Logical Reasoning': aptitude_scores.get('logical_score', 0),
        'Problem-Solving': aptitude_scores.get('problem_solving_score', 0),
        'Spatial Ability': aptitude_scores.get('spatial_score', 0),
        'Technical/Mechanical Reasoning': aptitude_scores.get('technical_score', 0),
        'Verbal/Communication Ability': aptitude_scores.get('verbal_score', 0),
        # RIASEC scores (0-40 scale normalized to 0-100)
        'Realistic': min(100.0, (riasec_scores.get('r_score', 0) / 40.0) * 100.0),
        'Investigative': min(100.0, (riasec_scores.get('i_score', 0) / 40.0) * 100.0),
        'Artistic': min(100.0, (riasec_scores.get('a_score', 0) / 40.0) * 100.0),
        'Social': min(100.0, (riasec_scores.get('s_score', 0) / 40.0) * 100.0),
        'Enterprising': min(100.0, (riasec_scores.get('e_score', 0) / 40.0) * 100.0),
        'Conventional': min(100.0, (riasec_scores.get('c_score', 0) / 40.0) * 100.0),
    }

    programs = Program.objects.all()
    program_rankings = []

    for prog in programs:
        criteria = ProgramCriteria.objects.filter(program=prog)
        total_score = 0.0
        total_weight = 0.0

        for crit in criteria:
            w = float(crit.weight)
            total_weight += w
            score_val = dim_to_student_score.get(crit.dimension_name, 0.0)
            total_score += (score_val * w)

        # Normalize score if total_weight > 0
        final_score = (total_score / total_weight) if total_weight > 0 else total_score
        program_rankings.append((prog, final_score))

    # Sort descending by final score
    program_rankings.sort(key=lambda x: x[1], reverse=True)

    top_prog = program_rankings[0][0] if len(program_rankings) > 0 else None
    sec_prog = program_rankings[1][0] if len(program_rankings) > 1 else None
    third_prog = program_rankings[2][0] if len(program_rankings) > 2 else None

    top_score = program_rankings[0][1] if len(program_rankings) > 0 else 0.0

    if top_score >= 70.0:
        alignment_level = 'Very High'
    elif top_score >= 55.0:
        alignment_level = 'High'
    elif top_score >= 40.0:
        alignment_level = 'Moderate'
    else:
        alignment_level = 'Low'

    explanation = (
        f"Based on your cognitive aptitude assessment and O*NET RIASEC interest profile ({riasec_scores.get('riasec_code', '')}), "
        f"your profile shows {alignment_level.lower()} alignment with {top_prog.program_name if top_prog else 'your recommended degree program'}."
    )

    return {
        'top_recommended_program': top_prog,
        'second_recommended_program': sec_prog,
        'third_recommended_program': third_prog,
        'alignment_level': alignment_level,
        'generated_explanation': explanation,
    }


def calculate_and_save_assessment_results(student_profile):
    """
    Master function: calculates RIASEC scores via O*NET, individual aptitude dimension scores,
    and program recommendations, then creates or updates the AssessmentResult for student_profile.
    """
    from .models import AssessmentResult

    riasec_scores = get_riasec_results(student_profile)
    aptitude_scores = calculate_aptitude_dimension_scores(student_profile)
    recs = calculate_program_recommendations(student_profile, aptitude_scores, riasec_scores)

    result_obj, created = AssessmentResult.objects.update_or_create(
        student=student_profile,
        defaults={
            'numerical_score': aptitude_scores['numerical_score'],
            'logical_score': aptitude_scores['logical_score'],
            'problem_solving_score': aptitude_scores['problem_solving_score'],
            'spatial_score': aptitude_scores['spatial_score'],
            'technical_score': aptitude_scores['technical_score'],
            'verbal_score': aptitude_scores['verbal_score'],
            'r_score': riasec_scores['r_score'],
            'i_score': riasec_scores['i_score'],
            'a_score': riasec_scores['a_score'],
            's_score': riasec_scores['s_score'],
            'e_score': riasec_scores['e_score'],
            'c_score': riasec_scores['c_score'],
            'riasec_code': riasec_scores['riasec_code'],
            'top_recommended_program': recs['top_recommended_program'],
            'second_recommended_program': recs['second_recommended_program'],
            'third_recommended_program': recs['third_recommended_program'],
            'alignment_level': recs['alignment_level'],
            'generated_explanation': recs['generated_explanation'],
        }
    )

    return result_obj
