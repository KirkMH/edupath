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