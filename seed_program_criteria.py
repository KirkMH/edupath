import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edupath.settings')
django.setup()

from customization.models import Program, ProgramCriteria

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
}

def sync_program_criteria():
    print("Syncing program criteria weights and minimum levels...")
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
    sync_program_criteria()
