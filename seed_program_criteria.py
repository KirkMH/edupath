import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edupath.settings')
django.setup()

from customization.models import Program, ProgramCriteria

PROGRAM_DEFINITIONS = [
    {
        "abbreviation": "BSCE",
        "program_name": "Bachelor of Science in Civil Engineering",
        "description": "Structural analysis, construction engineering, mechanics, physics, and infrastructure design.",
        "min_gwa": 85.00,
    },
    {
        "abbreviation": "BS InfoTech",
        "program_name": "Bachelor of Science in Information Technology",
        "description": "Software development, database administration, networking, web systems, and IT support.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BSIT",
        "program_name": "Bachelor of Science in Industrial Technology",
        "description": "Industrial manufacturing, equipment operation, shop floor maintenance, fabrication, and quality control.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BSHM",
        "program_name": "Bachelor of Science in Hospitality Management",
        "description": "Hotel and restaurant operations, culinary arts, customer service, event management, and tourism.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BTVTed",
        "program_name": "Bachelor of Technical Vocational Teacher Education",
        "description": "Pedagogy, technical-vocational instruction, shop teaching, student assessment, and TVET curriculum delivery.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BSA",
        "program_name": "Bachelor of Science in Architecture",
        "description": "Spatial layout, architectural drafting, visual design, building construction technology, and environmental design.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BIndTech",
        "program_name": "Bachelor of Industrial Technology",
        "description": "Focuses on hands-on technical training, trade skills, shop floor operations, equipment fabrication, and applied industrial innovations across diverse technology disciplines.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BSIS",
        "program_name": "Bachelor of Science in Information Systems",
        "description": "Focuses on the integration of information technology solutions and business enterprise processes, emphasizing systems analysis, database design, enterprise resource planning, and IT project management.",
        "min_gwa": None,
    },
    {
        "abbreviation": "BSEMC",
        "program_name": "Bachelor of Science in Entertainment and Multimedia Computing",
        "description": "Focuses on the concepts and technologies for creating interactive digital media, video game development, 2D/3D computer animation, digital visual effects, and multimedia systems.",
        "min_gwa": None,
    },
]

PROGRAM_CRITERIA_MAP = {
    "BSCE": {
        "Numerical Reasoning": (0.20, "High"),
        "Spatial Ability": (0.15, "High"),
        "Problem-Solving": (0.15, "High"),
        "Logical Reasoning": (0.10, "Moderate"),
        "Technical/Mechanical Reasoning": (0.10, "Moderate"),
        "Verbal/Communication Ability": (0.05, "Moderate"),
        "Realistic": (0.10, "High"),
        "Investigative": (0.10, "High"),
        "Conventional": (0.05, "Moderate"),
    },
    "BS InfoTech": {
        "Logical Reasoning": (0.20, "High"),
        "Problem-Solving": (0.15, "High"),
        "Numerical Reasoning": (0.10, "Moderate"),
        "Technical/Mechanical Reasoning": (0.10, "Moderate"),
        "Verbal/Communication Ability": (0.10, "Moderate"),
        "Spatial Ability": (0.05, "Low"),
        "Investigative": (0.10, "High"),
        "Conventional": (0.10, "High"),
        "Realistic": (0.05, "Moderate"),
        "Artistic": (0.05, "Not Applicable"),
    },
    "BSIT": {
        "Technical/Mechanical Reasoning": (0.25, "High"),
        "Problem-Solving": (0.15, "High"),
        "Spatial Ability": (0.10, "Moderate"),
        "Numerical Reasoning": (0.10, "Moderate"),
        "Logical Reasoning": (0.05, "Moderate"),
        "Verbal/Communication Ability": (0.05, "Moderate"),
        "Realistic": (0.15, "Very High"),
        "Conventional": (0.10, "High"),
        "Enterprising": (0.05, "Moderate"),
    },
    "BSHM": {
        "Verbal/Communication Ability": (0.25, "High"),
        "Problem-Solving": (0.15, "High"),
        "Logical Reasoning": (0.10, "Moderate"),
        "Numerical Reasoning": (0.10, "Moderate"),
        "Spatial Ability": (0.05, "Low"),
        "Technical/Mechanical Reasoning": (0.05, "Low"),
        "Social": (0.15, "Very High"),
        "Enterprising": (0.10, "High"),
        "Conventional": (0.05, "Moderate"),
    },
    "BTVTed": {
        "Verbal/Communication Ability": (0.25, "High"),
        "Technical/Mechanical Reasoning": (0.15, "High"),
        "Problem-Solving": (0.15, "High"),
        "Logical Reasoning": (0.05, "Moderate"),
        "Spatial Ability": (0.05, "Low"),
        "Numerical Reasoning": (0.05, "Low"),
        "Social": (0.15, "Very High"),
        "Realistic": (0.10, "High"),
        "Conventional": (0.05, "Moderate"),
    },
    "BSA": {
        "Spatial Ability": (0.25, "Very High"),
        "Problem-Solving": (0.15, "High"),
        "Numerical Reasoning": (0.10, "High"),
        "Logical Reasoning": (0.10, "Moderate"),
        "Technical/Mechanical Reasoning": (0.05, "Moderate"),
        "Verbal/Communication Ability": (0.05, "Moderate"),
        "Artistic": (0.15, "Very High"),
        "Realistic": (0.05, "Moderate"),
        "Investigative": (0.05, "Moderate"),
        "Conventional": (0.05, "Moderate"),
    },
    "BIndTech": {
        "Technical/Mechanical Reasoning": (0.25, "High"),
        "Problem-Solving": (0.15, "High"),
        "Spatial Ability": (0.15, "High"),
        "Numerical Reasoning": (0.05, "Moderate"),
        "Logical Reasoning": (0.05, "Moderate"),
        "Verbal/Communication Ability": (0.05, "Moderate"),
        "Realistic": (0.20, "Very High"),
        "Conventional": (0.05, "Moderate"),
        "Enterprising": (0.05, "Moderate"),
    },
    "BSIS": {
        "Logical Reasoning": (0.15, "High"),
        "Problem-Solving": (0.15, "High"),
        "Verbal/Communication Ability": (0.15, "High"),
        "Numerical Reasoning": (0.10, "Moderate"),
        "Technical/Mechanical Reasoning": (0.10, "Moderate"),
        "Spatial Ability": (0.05, "Low"),
        "Enterprising": (0.10, "High"),
        "Conventional": (0.10, "High"),
        "Investigative": (0.10, "High"),
    },
    "BSEMC": {
        "Spatial Ability": (0.20, "High"),
        "Logical Reasoning": (0.15, "High"),
        "Problem-Solving": (0.15, "High"),
        "Numerical Reasoning": (0.10, "Moderate"),
        "Technical/Mechanical Reasoning": (0.05, "Moderate"),
        "Verbal/Communication Ability": (0.05, "Moderate"),
        "Artistic": (0.15, "Very High"),
        "Investigative": (0.10, "High"),
        "Realistic": (0.05, "Moderate"),
    },
}

def sync_programs_and_criteria():
    print("Ensuring programs exist in database...")
    for prog_info in PROGRAM_DEFINITIONS:
        program, created = Program.objects.get_or_create(
            abbreviation=prog_info["abbreviation"],
            defaults={
                "program_name": prog_info["program_name"],
                "description": prog_info["description"],
                "min_gwa": prog_info["min_gwa"],
            }
        )
        if not created:
            updated = False
            if program.program_name != prog_info["program_name"]:
                program.program_name = prog_info["program_name"]
                updated = True
            if program.description != prog_info["description"]:
                program.description = prog_info["description"]
                updated = True
            if prog_info["min_gwa"] is None and program.min_gwa is not None:
                # Keep or reset as needed
                pass
            if updated:
                program.save()
        status_str = "Created" if created else "Found"
        print(f"[{status_str}] Program: {program.abbreviation} - {program.program_name} (min_gwa={program.min_gwa})")

    print("\nSyncing program criteria weights and minimum levels...")
    from customization.models import DEFAULT_DIMENSIONS

    # Clean up any removed dimensions from criteria
    ProgramCriteria.objects.exclude(dimension_name__in=DEFAULT_DIMENSIONS).delete()

    for abbrev, criteria_dict in PROGRAM_CRITERIA_MAP.items():
        try:
            program = Program.objects.get(abbreviation__iexact=abbrev)

            # Ensure all default dimensions exist for the program
            for dim in DEFAULT_DIMENSIONS:
                ProgramCriteria.objects.get_or_create(
                    program=program,
                    dimension_name=dim,
                    defaults={
                        'weight': 0.00,
                        'minimum_level': 'Not Applicable'
                    }
                )

            # Reset non-specified dimensions to 0.00 / Not Applicable
            for dim in DEFAULT_DIMENSIONS:
                if dim not in criteria_dict:
                    ProgramCriteria.objects.update_or_create(
                        program=program,
                        dimension_name=dim,
                        defaults={
                            'weight': 0.00,
                            'minimum_level': 'Not Applicable'
                        }
                    )

            for dim_name, (weight, min_lvl) in criteria_dict.items():
                ProgramCriteria.objects.update_or_create(
                    program=program,
                    dimension_name=dim_name,
                    defaults={
                        'weight': weight,
                        'minimum_level': min_lvl
                    }
                )
            print(f"Successfully updated criteria for: {program.abbreviation} - {program.program_name}")
        except Program.DoesNotExist:
            print(f"Warning: Program '{abbrev}' not found in database.")

if __name__ == '__main__':
    sync_programs_and_criteria()
