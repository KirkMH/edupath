import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edupath.settings')
django.setup()

from customization.models import Program, Major, MajorCriteria, DEFAULT_DIMENSIONS

MAJORS_DATA = {
    "BS InfoTech": [
        {
            "name": "Software Engineering",
            "description": "Focuses on software architecture, full-stack programming, algorithmic development, software testing, and agile methodologies.",
            "criteria": {
                "Logical Reasoning": (0.25, "High"),
                "Problem-Solving": (0.20, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Technical/Mechanical Reasoning": (0.05, "Moderate"),
                "Verbal/Communication Ability": (0.10, "Moderate"),
                "Spatial Ability": (0.05, "Low"),
                "Investigative": (0.15, "High"),
                "Conventional": (0.10, "High"),
            }
        },
        {
            "name": "Computer Hardware & Networking Technologies",
            "description": "Focuses on enterprise network design, server administration, hardware diagnostics, telecommunications, and cybersecurity infrastructure.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.25, "High"),
                "Problem-Solving": (0.15, "High"),
                "Logical Reasoning": (0.15, "High"),
                "Numerical Reasoning": (0.05, "Moderate"),
                "Spatial Ability": (0.05, "Moderate"),
                "Verbal/Communication Ability": (0.05, "Moderate"),
                "Realistic": (0.15, "High"),
                "Conventional": (0.10, "High"),
                "Investigative": (0.05, "Moderate"),
            }
        },
        {
            "name": "Instructional Systems Technology",
            "description": "Focuses on educational technology solutions, multimedia e-learning courseware design, digital pedagogy systems, and LMS administration.",
            "criteria": {
                "Verbal/Communication Ability": (0.20, "High"),
                "Logical Reasoning": (0.15, "High"),
                "Problem-Solving": (0.15, "High"),
                "Spatial Ability": (0.10, "Moderate"),
                "Numerical Reasoning": (0.05, "Moderate"),
                "Technical/Mechanical Reasoning": (0.05, "Moderate"),
                "Social": (0.15, "High"),
                "Artistic": (0.10, "Moderate"),
                "Conventional": (0.05, "Moderate"),
            }
        },
        {
            "name": "Service Management - Business Process Outsourcing",
            "description": "Focuses on IT service management (ITSM), BPO industry operations, client support management, and enterprise workflow optimization.",
            "criteria": {
                "Verbal/Communication Ability": (0.25, "High"),
                "Problem-Solving": (0.15, "High"),
                "Logical Reasoning": (0.15, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Technical/Mechanical Reasoning": (0.05, "Low"),
                "Enterprising": (0.15, "High"),
                "Conventional": (0.10, "High"),
                "Social": (0.05, "Moderate"),
            }
        },
    ],
    "BSIT": [
        {
            "name": "Architectural Drafting Technology",
            "description": "Focuses on computer-aided architectural drafting (CAD), 3D structural modeling, building blueprint interpretation, and construction documentation.",
            "criteria": {
                "Spatial Ability": (0.25, "Very High"),
                "Problem-Solving": (0.15, "High"),
                "Technical/Mechanical Reasoning": (0.15, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Logical Reasoning": (0.05, "Moderate"),
                "Realistic": (0.15, "High"),
                "Artistic": (0.10, "High"),
                "Conventional": (0.05, "Moderate"),
            }
        },
        {
            "name": "Electrical Technology",
            "description": "Focuses on industrial electrical wiring, power generation and distribution, motor controls, transformer maintenance, and electrical safety.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.25, "High"),
                "Problem-Solving": (0.15, "High"),
                "Logical Reasoning": (0.15, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Spatial Ability": (0.05, "Moderate"),
                "Realistic": (0.20, "Very High"),
                "Conventional": (0.10, "High"),
            }
        },
        {
            "name": "Electronics Technology",
            "description": "Focuses on circuit design, semiconductor devices, microcontrollers, embedded systems, instrumentation, and telecommunication electronics.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.25, "High"),
                "Logical Reasoning": (0.15, "High"),
                "Problem-Solving": (0.15, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Spatial Ability": (0.05, "Moderate"),
                "Realistic": (0.15, "High"),
                "Investigative": (0.10, "High"),
                "Conventional": (0.05, "Moderate"),
            }
        },
        {
            "name": "Mechanical Technology",
            "description": "Focuses on machining, metal fabrication, CNC programming, plant equipment operation, mechanical systems maintenance, and fluid power.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.25, "High"),
                "Spatial Ability": (0.15, "High"),
                "Problem-Solving": (0.15, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Logical Reasoning": (0.05, "Moderate"),
                "Realistic": (0.20, "Very High"),
                "Conventional": (0.10, "High"),
            }
        },
        {
            "name": "Automotive Technology",
            "description": "Focuses on internal combustion engines, vehicle electronic diagnostics, power train servicing, auto chassis systems, and hybrid technologies.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.30, "Very High"),
                "Problem-Solving": (0.15, "High"),
                "Spatial Ability": (0.10, "Moderate"),
                "Logical Reasoning": (0.10, "Moderate"),
                "Numerical Reasoning": (0.05, "Moderate"),
                "Realistic": (0.20, "Very High"),
                "Conventional": (0.10, "High"),
            }
        },
        {
            "name": "Civil Technology",
            "description": "Focuses on construction materials testing, site surveying, concrete technology, structural inspection, and public works supervision.",
            "criteria": {
                "Spatial Ability": (0.20, "High"),
                "Technical/Mechanical Reasoning": (0.20, "High"),
                "Numerical Reasoning": (0.15, "High"),
                "Problem-Solving": (0.15, "High"),
                "Logical Reasoning": (0.05, "Moderate"),
                "Realistic": (0.15, "High"),
                "Conventional": (0.10, "High"),
            }
        },
    ],
    "BIndTech": [
        {
            "name": "Beauty Care and Wellness Technology",
            "description": "Focuses on cosmetology sciences, salon and spa technology management, holistic wellness therapy, and beauty enterprise management.",
            "criteria": {
                "Verbal/Communication Ability": (0.20, "High"),
                "Problem-Solving": (0.15, "High"),
                "Spatial Ability": (0.15, "Moderate"),
                "Technical/Mechanical Reasoning": (0.10, "Moderate"),
                "Numerical Reasoning": (0.05, "Low"),
                "Realistic": (0.15, "High"),
                "Social": (0.10, "High"),
                "Enterprising": (0.10, "Moderate"),
            }
        },
        {
            "name": "Apparel and Fashion Technology",
            "description": "Focuses on garment construction, pattern drafting, textile fabrication technology, fashion illustration, and industrial apparel production.",
            "criteria": {
                "Spatial Ability": (0.25, "High"),
                "Problem-Solving": (0.15, "High"),
                "Technical/Mechanical Reasoning": (0.15, "High"),
                "Numerical Reasoning": (0.05, "Moderate"),
                "Verbal/Communication Ability": (0.05, "Moderate"),
                "Artistic": (0.20, "Very High"),
                "Realistic": (0.10, "High"),
                "Conventional": (0.05, "Moderate"),
            }
        },
        {
            "name": "Culinary Technology",
            "description": "Focuses on commercial culinary arts, food safety engineering, kitchen equipment technology, food preservation, and catering production.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.20, "High"),
                "Problem-Solving": (0.15, "High"),
                "Spatial Ability": (0.10, "Moderate"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Verbal/Communication Ability": (0.10, "Moderate"),
                "Realistic": (0.15, "High"),
                "Artistic": (0.10, "High"),
                "Enterprising": (0.10, "Moderate"),
            }
        },
    ],
    "BTVTed": [
        {
            "name": "Beauty Care and Wellness",
            "description": "Prepares technical-vocational educators in cosmetology, aesthetic wellness therapies, salon operations, and TVET instructional delivery.",
            "criteria": {
                "Verbal/Communication Ability": (0.25, "High"),
                "Technical/Mechanical Reasoning": (0.15, "High"),
                "Problem-Solving": (0.15, "High"),
                "Spatial Ability": (0.05, "Low"),
                "Social": (0.20, "Very High"),
                "Realistic": (0.10, "High"),
                "Conventional": (0.10, "Moderate"),
            }
        },
        {
            "name": "Computer System Servicing and Programming",
            "description": "Prepares educators for teaching computer assembly, network configuration, software programming fundamentals, and ICT workshop management.",
            "criteria": {
                "Logical Reasoning": (0.20, "High"),
                "Verbal/Communication Ability": (0.20, "High"),
                "Technical/Mechanical Reasoning": (0.15, "High"),
                "Problem-Solving": (0.15, "High"),
                "Social": (0.15, "Very High"),
                "Conventional": (0.10, "High"),
                "Investigative": (0.05, "Moderate"),
            }
        },
        {
            "name": "Hotel and Restaurant Services",
            "description": "Prepares TVET teachers for instructing food and beverage service, housekeeping operations, front office management, and hospitality standards.",
            "criteria": {
                "Verbal/Communication Ability": (0.25, "High"),
                "Problem-Solving": (0.15, "High"),
                "Technical/Mechanical Reasoning": (0.10, "Moderate"),
                "Logical Reasoning": (0.10, "Moderate"),
                "Social": (0.20, "Very High"),
                "Enterprising": (0.10, "High"),
                "Conventional": (0.10, "Moderate"),
            }
        },
        {
            "name": "Food Service Management",
            "description": "Prepares instructors in commercial meal management, institutional food preparation, cafeteria operations, nutrition, and food cost accounting.",
            "criteria": {
                "Verbal/Communication Ability": (0.20, "High"),
                "Problem-Solving": (0.15, "High"),
                "Numerical Reasoning": (0.10, "Moderate"),
                "Technical/Mechanical Reasoning": (0.10, "Moderate"),
                "Logical Reasoning": (0.10, "Moderate"),
                "Social": (0.15, "Very High"),
                "Enterprising": (0.10, "High"),
                "Conventional": (0.10, "Moderate"),
            }
        },
        {
            "name": "Electrical Technology",
            "description": "Prepares TVET educators in electrical circuitry, motor rewinding, industrial power controls, residential wiring, and shop safety instruction.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.20, "High"),
                "Verbal/Communication Ability": (0.20, "High"),
                "Problem-Solving": (0.15, "High"),
                "Logical Reasoning": (0.10, "Moderate"),
                "Numerical Reasoning": (0.05, "Moderate"),
                "Social": (0.15, "Very High"),
                "Realistic": (0.10, "High"),
                "Conventional": (0.05, "Moderate"),
            }
        },
        {
            "name": "Electronics Technology",
            "description": "Prepares vocational instructors in electronic circuits, consumer electronics repair, digital logic systems, radio/audio systems, and prototyping.",
            "criteria": {
                "Technical/Mechanical Reasoning": (0.20, "High"),
                "Verbal/Communication Ability": (0.20, "High"),
                "Problem-Solving": (0.15, "High"),
                "Logical Reasoning": (0.10, "Moderate"),
                "Numerical Reasoning": (0.05, "Moderate"),
                "Social": (0.15, "Very High"),
                "Realistic": (0.10, "High"),
                "Conventional": (0.05, "Moderate"),
            }
        },
    ],
}

def sync_majors_and_criteria():
    print("Syncing Majors and Major Criteria...")
    total_majors_created = 0
    total_majors_updated = 0

    for prog_abbrev, majors_list in MAJORS_DATA.items():
        try:
            program = Program.objects.get(abbreviation__iexact=prog_abbrev)
            print(f"\nProcessing Program: {program.abbreviation} - {program.program_name}")

            for major_info in majors_list:
                major, created = Major.objects.get_or_create(
                    program=program,
                    name=major_info["name"],
                    defaults={
                        "description": major_info["description"]
                    }
                )
                if created:
                    total_majors_created += 1
                    status = "Created"
                else:
                    total_majors_updated += 1
                    status = "Updated"
                    if major.description != major_info["description"]:
                        major.description = major_info["description"]
                        major.save()

                # Ensure default dimensions exist
                for dim in DEFAULT_DIMENSIONS:
                    MajorCriteria.objects.get_or_create(
                        major=major,
                        dimension_name=dim,
                        defaults={
                            'weight': 0.00,
                            'minimum_level': 'Not Applicable'
                        }
                    )

                # Reset all dimensions to 0.00 first
                for dim in DEFAULT_DIMENSIONS:
                    if dim not in major_info["criteria"]:
                        MajorCriteria.objects.update_or_create(
                            major=major,
                            dimension_name=dim,
                            defaults={
                                'weight': 0.00,
                                'minimum_level': 'Not Applicable'
                            }
                        )

                # Apply specific criteria
                for dim_name, (weight, min_lvl) in major_info["criteria"].items():
                    MajorCriteria.objects.update_or_create(
                        major=major,
                        dimension_name=dim_name,
                        defaults={
                            'weight': weight,
                            'minimum_level': min_lvl
                        }
                    )

                print(f"  [{status}] Major: {major.name} (Criteria mapped)")

        except Program.DoesNotExist:
            print(f"Warning: Program with abbreviation '{prog_abbrev}' not found.")

    print(f"\nCompleted: {total_majors_created} created, {total_majors_updated} updated.")

if __name__ == '__main__':
    sync_majors_and_criteria()
