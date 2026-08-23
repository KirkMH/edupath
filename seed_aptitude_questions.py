import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edupath.settings')
django.setup()

from customization.models import AptitudeQuestion

def populate_aptitude_questions():
    print("Deactivating all existing aptitude questions...")
    deactivated_count = AptitudeQuestion.objects.all().update(status=False)
    print(f"Deactivated {deactivated_count} existing aptitude question(s).\n")

    questions_data = [
        # ==========================================
        # 1. Numerical Reasoning (8 Questions)
        # ==========================================
        {
            "dimension": "Numerical Reasoning",
            "question_text": "If a shirt costs 500 PHP and is discounted by 20%, what is the final sale price?",
            "option_a": "350 PHP",
            "option_b": "400 PHP",
            "option_c": "420 PHP",
            "option_d": "450 PHP",
            "correct_answer": "B",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "What is the next number in the arithmetic sequence: 4, 8, 12, 16, ___?",
            "option_a": "18",
            "option_b": "20",
            "option_c": "22",
            "option_d": "24",
            "correct_answer": "B",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "A student scored 85, 90, and 95 on three consecutive quizzes. What is their average score?",
            "option_a": "88",
            "option_b": "90",
            "option_c": "92",
            "option_d": "93",
            "correct_answer": "B",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "If 5 notebooks cost 150 PHP, how much will 8 of the same notebooks cost?",
            "option_a": "200 PHP",
            "option_b": "220 PHP",
            "option_c": "240 PHP",
            "option_d": "250 PHP",
            "correct_answer": "C",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "What is 15% of 200?",
            "option_a": "25",
            "option_b": "30",
            "option_c": "35",
            "option_d": "40",
            "correct_answer": "B",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "A vehicle travels a total distance of 180 km in 3 hours at a constant speed. What is its speed in km/h?",
            "option_a": "50 km/h",
            "option_b": "60 km/h",
            "option_c": "70 km/h",
            "option_d": "80 km/h",
            "correct_answer": "B",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "What is the missing number in the geometric sequence: 3, 9, 27, 81, ___?",
            "option_a": "162",
            "option_b": "243",
            "option_c": "324",
            "option_d": "363",
            "correct_answer": "B",
        },
        {
            "dimension": "Numerical Reasoning",
            "question_text": "A class consists of 40 students. If 60% of them are female, how many female students are in the class?",
            "option_a": "20",
            "option_b": "22",
            "option_c": "24",
            "option_d": "26",
            "correct_answer": "C",
        },

        # ==========================================
        # 2. Logical Reasoning (8 Questions)
        # ==========================================
        {
            "dimension": "Logical Reasoning",
            "question_text": "Premise 1: All birds have wings. Premise 2: A robin is a bird. What conclusion logically follows?",
            "option_a": "All birds are robins.",
            "option_b": "A robin has wings.",
            "option_c": "Robins fly faster than other birds.",
            "option_d": "Robins do not have feathers.",
            "correct_answer": "B",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "Identify the next item in the repeating sequence: Red, Yellow, Blue, Red, Yellow, ___?",
            "option_a": "Green",
            "option_b": "Blue",
            "option_c": "Orange",
            "option_d": "Purple",
            "correct_answer": "B",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "If all cats love fish, and Whiskers is a cat, which statement MUST be true?",
            "option_a": "Whiskers loves fish.",
            "option_b": "Whiskers dislikes milk.",
            "option_c": "All animals love fish.",
            "option_d": "Whiskers is a dog.",
            "correct_answer": "A",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "Examine the letter pair pattern: AZ, BY, CX, DW, ___? Which pair comes next?",
            "option_a": "EV",
            "option_b": "EU",
            "option_c": "FV",
            "option_d": "EX",
            "correct_answer": "A",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "Some doctors are teachers. All teachers are readers. Which statement is logically valid?",
            "option_a": "All doctors are readers.",
            "option_b": "Some doctors are readers.",
            "option_c": "No doctors are readers.",
            "option_d": "All readers are teachers.",
            "correct_answer": "B",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "Which word does NOT belong in the group: Apple, Banana, Carrot, Mango?",
            "option_a": "Apple",
            "option_b": "Banana",
            "option_c": "Carrot",
            "option_d": "Mango",
            "correct_answer": "C",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "Complete the analogy: SOUTH is to NORTH as WEST is to ___.",
            "option_a": "EAST",
            "option_b": "SOUTH",
            "option_c": "NORTH",
            "option_d": "PACIFIC",
            "correct_answer": "A",
        },
        {
            "dimension": "Logical Reasoning",
            "question_text": "Whenever it rains, the ground gets wet. Today the ground is NOT wet. What can you logically deduce?",
            "option_a": "It is raining heavily.",
            "option_b": "It did not rain.",
            "option_c": "The ground is hot.",
            "option_d": "It will rain tomorrow.",
            "correct_answer": "B",
        },

        # ==========================================
        # 3. Problem-Solving (8 Questions)
        # ==========================================
        {
            "dimension": "Problem-Solving",
            "question_text": "You have a meeting scheduled at 2:30 PM. The journey takes 45 minutes. What is the latest time you should leave?",
            "option_a": "1:30 PM",
            "option_b": "1:45 PM",
            "option_c": "2:00 PM",
            "option_d": "2:15 PM",
            "correct_answer": "B",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "A team needs to complete 100 inventory tasks across 5 workdays. How many tasks per day must they average?",
            "option_a": "15 tasks",
            "option_b": "20 tasks",
            "option_c": "25 tasks",
            "option_d": "30 tasks",
            "correct_answer": "B",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "A office printer stops printing and displays a 'paper jam' error. What is the most appropriate first action?",
            "option_a": "Turn off the building power.",
            "option_b": "Open the access door and carefully clear jammed paper.",
            "option_c": "Order a new printer replacement.",
            "option_d": "Reinstall the computer software.",
            "correct_answer": "B",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "A project requires 3 technicians working for 4 hours each to complete. How many total labor-hours are required?",
            "option_a": "7 labor-hours",
            "option_b": "12 labor-hours",
            "option_c": "14 labor-hours",
            "option_d": "16 labor-hours",
            "correct_answer": "B",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "A promo offers 'Buy 2 Shirts, Get 1 Free' at 300 PHP per shirt. How much will a customer pay for 3 shirts total?",
            "option_a": "300 PHP",
            "option_b": "600 PHP",
            "option_c": "900 PHP",
            "option_d": "450 PHP",
            "correct_answer": "B",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "Box A is heavier than Box B. Box B is heavier than Box C. Box C is heavier than both Box D and Box E. Which box is the heaviest?",
            "option_a": "Box A",
            "option_b": "Box B",
            "option_c": "Box C",
            "option_d": "Box D",
            "correct_answer": "A",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "A shuttle bus departs every 20 minutes starting at 8:00 AM. At what time does the 4th bus depart?",
            "option_a": "8:40 AM",
            "option_b": "9:00 AM",
            "option_c": "9:20 AM",
            "option_d": "9:40 AM",
            "correct_answer": "B",
        },
        {
            "dimension": "Problem-Solving",
            "question_text": "A storage tank holds 500 liters of water. If it leaks at a steady rate of 10 liters per hour, how many hours will it take to lose 100 liters?",
            "option_a": "5 hours",
            "option_b": "10 hours",
            "option_c": "15 hours",
            "option_d": "50 hours",
            "correct_answer": "B",
        },

        # ==========================================
        # 4. Spatial Ability (8 Questions)
        # ==========================================
        {
            "dimension": "Spatial Ability",
            "question_text": "If a flat 2D square is pulled directly upwards into three dimensions, what 3D object is formed?",
            "option_a": "Sphere",
            "option_b": "Cylinder",
            "option_c": "Cube / Rectangular Prism",
            "option_d": "Cone",
            "correct_answer": "C",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "A square paper folded in half from left to right has a triangle cut out along its folded center line. When opened flat, what shape appears?",
            "option_a": "One single triangle",
            "option_b": "A diamond or double-triangle cutout",
            "option_c": "A perfect circle",
            "option_d": "No shape",
            "correct_answer": "B",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "If you rotate the letter 'L' 180 degrees in a plane, how will it appear?",
            "option_a": "Long line pointing down, short foot pointing left",
            "option_b": "Identical to original 'L'",
            "option_c": "Long line pointing right",
            "option_d": "Short foot pointing up",
            "correct_answer": "A",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "How many flat square faces are on a standard 3D cube?",
            "option_a": "4",
            "option_b": "6",
            "option_c": "8",
            "option_d": "12",
            "correct_answer": "B",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "Which regular polygon has exactly 3 lines of reflective symmetry?",
            "option_a": "Square",
            "option_b": "Equilateral Triangle",
            "option_c": "Regular Pentagon",
            "option_d": "Regular Hexagon",
            "correct_answer": "B",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "What 2D shape is observed when looking directly down at a cone from top view?",
            "option_a": "Triangle",
            "option_b": "Rectangle",
            "option_c": "Circle with a central apex point",
            "option_d": "Square",
            "correct_answer": "C",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "A card with a dark square on the top-left corner is flipped horizontally (mirror image). Where is the dark square located now?",
            "option_a": "Top-Right",
            "option_b": "Bottom-Left",
            "option_c": "Bottom-Right",
            "option_d": "Top-Left",
            "correct_answer": "A",
        },
        {
            "dimension": "Spatial Ability",
            "question_text": "How many interior right angles (90-degree angles) does a standard rectangle possess?",
            "option_a": "2",
            "option_b": "3",
            "option_c": "4",
            "option_d": "8",
            "correct_answer": "C",
        },

        # ==========================================
        # 5. Technical/Mechanical Reasoning (8 Questions)
        # ==========================================
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "Gear A rotates clockwise and directly meshes with Gear B. In which direction does Gear B rotate?",
            "option_a": "Clockwise",
            "option_b": "Counter-clockwise",
            "option_c": "Stays stationary",
            "option_d": "Vibrates back and forth",
            "correct_answer": "B",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "Which simple machine mechanism is fundamentally utilized in a playground seesaw?",
            "option_a": "Pulley",
            "option_b": "Lever",
            "option_c": "Wedge",
            "option_d": "Inclined Plane",
            "correct_answer": "B",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "To reduce the effort required to push a heavy box upward onto a truck platform, the loading ramp should be:",
            "option_a": "Shorter and steeper",
            "option_b": "Longer and less steep",
            "option_c": "Vertical",
            "option_d": "Curved inward",
            "correct_answer": "B",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "In a basic electrical circuit containing a battery and a light bulb, what happens when a switch opens the circuit?",
            "option_a": "The bulb glows brighter",
            "option_b": "The bulb turns off",
            "option_c": "Current flow increases",
            "option_d": "The wire heats up",
            "correct_answer": "B",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "Which hand tool is specifically designed for tightening or loosening hexagonal bolt heads?",
            "option_a": "Hammer",
            "option_b": "Wrench",
            "option_c": "Handsaw",
            "option_d": "Scissors",
            "correct_answer": "B",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "Two equal weights balance perfectly on a lever. How far should each weight be placed relative to the fulcrum (pivot)?",
            "option_a": "Equal distances from the fulcrum",
            "option_b": "One close to the pivot, one far away",
            "option_c": "Both on the left arm",
            "option_d": "Directly over the pivot point",
            "correct_answer": "A",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "Why does motor oil float when poured into a container of water?",
            "option_a": "Oil has higher density than water",
            "option_b": "Oil has lower density than water",
            "option_c": "Water is warmer than oil",
            "option_d": "Oil absorbs water",
            "correct_answer": "B",
        },
        {
            "dimension": "Technical/Mechanical Reasoning",
            "question_text": "What is the primary function of a single fixed pulley attached to a ceiling?",
            "option_a": "Reduces force by half",
            "option_b": "Changes the direction of the applied pulling force",
            "option_c": "Triples pulling speed",
            "option_d": "Eliminates object weight",
            "correct_answer": "B",
        },

        # ==========================================
        # 6. Verbal/Communication Ability (8 Questions)
        # ==========================================
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "Select the word that is most nearly SYNONYMOUS in meaning to 'ABUNDANT':",
            "option_a": "Scarce",
            "option_b": "Plentiful",
            "option_c": "Tiny",
            "option_d": "Deficient",
            "correct_answer": "B",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "Choose the correct verb form to complete: 'Neither of the applicants ___ ready for the interview yesterday.'",
            "option_a": "were",
            "option_b": "was",
            "option_c": "are",
            "option_d": "be",
            "correct_answer": "B",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "Select the word that is an ANTONYM of 'EXPAND':",
            "option_a": "Stretch",
            "option_b": "Contract",
            "option_c": "Grow",
            "option_d": "Extend",
            "correct_answer": "B",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "Which sentence is grammatically correct?",
            "option_a": "She don't like reading technical manuals.",
            "option_b": "She doesn't like reading technical manuals.",
            "option_c": "She not like reading technical manuals.",
            "option_d": "She isn't like reading technical manuals.",
            "correct_answer": "B",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "In the sentence 'The instructions were explicit,' what does the word 'EXPLICIT' mean?",
            "option_a": "Vague and confusing",
            "option_b": "Stated clearly and in detail",
            "option_c": "Hidden and implicit",
            "option_d": "Long and repetitive",
            "correct_answer": "B",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "Fill in the blank with the correct word: 'The team worked diligently to ___ the project ahead of schedule.'",
            "option_a": "complete",
            "option_b": "completely",
            "option_c": "completing",
            "option_d": "completion",
            "correct_answer": "A",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "Complete the analogy: Doctor is to Hospital as Teacher is to ___.",
            "option_a": "Office",
            "option_b": "School",
            "option_c": "Library",
            "option_d": "Courtroom",
            "correct_answer": "B",
        },
        {
            "dimension": "Verbal/Communication Ability",
            "question_text": "What is the meaning of the common idiomatic phrase 'break the ice'?",
            "option_a": "To freeze liquids quickly",
            "option_b": "To initiate conversation and relieve tension in a social setting",
            "option_c": "To end a partnership abruptly",
            "option_d": "To cause a disagreement",
            "correct_answer": "B",
        },
    ]

    created_questions = []
    for data in questions_data:
        q = AptitudeQuestion.objects.create(
            dimension=data["dimension"],
            question_text=data["question_text"],
            option_a=data["option_a"],
            option_b=data["option_b"],
            option_c=data["option_c"],
            option_d=data["option_d"],
            correct_answer=data["correct_answer"],
            status=True,
            for_validation=True
        )
        created_questions.append(q)

    print(f"Successfully created {len(created_questions)} new active aptitude questions (8 per domain across 6 domains):\n")
    
    # Count per domain
    domain_counts = {}
    for q in AptitudeQuestion.objects.filter(status=True):
        domain_counts[q.dimension] = domain_counts.get(q.dimension, 0) + 1

    for domain, count in domain_counts.items():
        print(f" - {domain}: {count} active question(s)")

if __name__ == '__main__':
    populate_aptitude_questions()
