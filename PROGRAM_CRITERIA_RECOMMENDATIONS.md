# Recommended Program Criteria Guidelines

This document outlines the recommended scoring weights and minimum requirement levels for the academic degree programs evaluated by the **EduPath Decision Support System**. 

The evaluation framework evaluates student profiles across **12 Core Evaluation Dimensions** combined with an optional **Program Minimum GWA Cutoff**:
1. **Aptitude Dimensions (6 Cognitive Domains)**: Numerical Reasoning, Logical Reasoning, Problem-Solving, Spatial Ability, Technical/Mechanical Reasoning, Verbal/Communication Ability.
2. **Preference Dimensions (6 O*NET RIASEC Interest Areas)**: Realistic (R), Investigative (I), Artistic (A), Social (S), Enterprising (E), Conventional (C).
3. **Academic Prerequisite (Program `min_gwa`)**: Optional minimum General Weighted Average configured directly on each `Program`. If a student's GWA falls below a program's `min_gwa`, they are strictly disqualified from receiving that program as a recommendation.

---

## 📊 Overview of Evaluation Framework

Each program defines scoring weights totaling **1.00 (100%)** distributed across the 12 evaluation dimensions, coupled with minimum threshold levels (`Very High`, `High`, `Moderate`, `Low`, `Very Low`, or `Not Applicable`), plus an optional `min_gwa` cutoff on the Program:

- **Minimum GWA Cutoff (`Program.min_gwa`)**: Optional numeric cutoff (e.g., `85.00`). Students with a GWA lower than this value are strictly disqualified and cannot be recommended for the program.
- **Aptitude Component (70% - 75% Total Weight)**: Evaluates cognitive capabilities and problem-solving skills necessary for academic success.
- **Preference Component (25% - 30% Total Weight)**: Evaluates student interest alignment based on Holland's RIASEC theory.

---

## 🎓 Program Criteria Specifications

### 1. Bachelor of Science in Civil Engineering (BSCE)
*Focus: Structural analysis, construction engineering, mechanics, physics, and infrastructure design.*

| Category | Dimension | Weight | Minimum Level | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Aptitude** | Numerical Reasoning | **0.20** | **High** | Essential for advanced calculus, structural mechanics, and load calculations. |
| **Aptitude** | Spatial Ability | **0.15** | **High** | Critical for visualizing 3D structural frameworks, blueprints, and CAD models. |
| **Aptitude** | Problem-Solving | **0.15** | **High** | Essential for addressing structural failures, environmental hazards, and site issues. |
| **Aptitude** | Logical Reasoning | **0.10** | **Moderate** | Important for engineering logic, structural stress analysis, and physics modeling. |
| **Aptitude** | Technical/Mechanical Reasoning | **0.10** | **Moderate** | Required to understand heavy machinery, construction materials, and physics. |
| **Aptitude** | Verbal/Communication Ability | **0.05** | **Moderate** | Necessary for project management reports, team coordination, and site safety protocols. |
| **Preference** | Realistic (R) | **0.10** | **High** | Direct alignment with outdoor construction sites, physical structures, and machinery. |
| **Preference** | Investigative (I) | **0.10** | **High** | Strong alignment with scientific inquiry, materials testing, and structural research. |
| **Preference** | Conventional (C) | **0.05** | **Moderate** | Required for working with building codes, cost estimations, and structural standards. |
| **Preference** | Artistic (A) | **0.00** | *Not Applicable* | Minor impact on core civil engineering duties. |
| **Preference** | Social (S) | **0.00** | *Not Applicable* | Minor impact on structural analysis. |
| **Preference** | Enterprising (E) | **0.00** | *Not Applicable* | Secondary to technical and structural engineering competency. |
| **Total** | | **1.00** | | |

---

### 2. Bachelor of Science in Information Technology (BS InfoTech)
*Focus: Software development, database administration, networking, web systems, and IT support.*

| Category | Dimension | Weight | Minimum Level | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Aptitude** | Logical Reasoning | **0.20** | **High** | Core requirement for programming logic, control structures, and algorithm design. |
| **Aptitude** | Problem-Solving | **0.15** | **High** | Critical for software debugging, system troubleshooting, and network diagnostics. |
| **Aptitude** | Numerical Reasoning | **0.10** | **Moderate** | Necessary for data analysis, discrete mathematics, cryptography, and algorithms. |
| **Aptitude** | Technical/Mechanical Reasoning | **0.10** | **Moderate** | Essential for hardware configuration, network infrastructure, and system administration. |
| **Aptitude** | Verbal/Communication Ability | **0.10** | **Moderate** | Important for technical documentation, client requirement gathering, and support. |
| **Aptitude** | Spatial Ability | **0.05** | **Low** | Useful for UI/UX visual layout design and database entity mapping. |
| **Preference** | Investigative (I) | **0.10** | **High** | Strong interest in technology research, complex code analysis, and system architecture. |
| **Preference** | Conventional (C) | **0.10** | **High** | High alignment with structured data, coding conventions, and database management. |
| **Preference** | Realistic (R) | **0.05** | **Moderate** | Hands-on interaction with physical servers, network cabling, and hardware gear. |
| **Preference** | Artistic (A) | **0.05** | *Not Applicable* | Beneficial for UI/UX design and frontend visual aesthetics. |
| **Preference** | Social (S) | **0.00** | *Not Applicable* | Secondary to technical problem-solving. |
| **Preference** | Enterprising (E) | **0.00** | *Not Applicable* | Secondary to software and systems development skills. |
| **Total** | | **1.00** | | |

---

### 3. Bachelor of Science in Industrial Technology (BSIT)
*Focus: Industrial manufacturing, equipment operation, shop floor maintenance, fabrication, and quality control.*

| Category | Dimension | Weight | Minimum Level | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Aptitude** | Technical/Mechanical Reasoning | **0.25** | **High** | Primary aptitude for operating, repairing, and understanding industrial machinery. |
| **Aptitude** | Problem-Solving | **0.15** | **High** | Essential for machine repair, production line troubleshooting, and process optimization. |
| **Aptitude** | Spatial Ability | **0.10** | **Moderate** | Needed for interpreting technical drawings, blueprints, and assembly diagrams. |
| **Aptitude** | Numerical Reasoning | **0.10** | **Moderate** | Needed for production measurements, quality assurance metrics, and calibration. |
| **Aptitude** | Logical Reasoning | **0.05** | **Moderate** | Important for sequential manufacturing workflows and safety compliance logic. |
| **Aptitude** | Verbal/Communication Ability | **0.05** | **Moderate** | Required for workshop safety reporting, equipment logs, and shop supervision. |
| **Preference** | Realistic (R) | **0.15** | **Very High** | Strongest preference match; hands-on trade skills, tools, fabrication, and machinery. |
| **Preference** | Conventional (C) | **0.10** | **High** | Alignment with quality assurance standards, safety regulations, and maintenance logs. |
| **Preference** | Enterprising (E) | **0.05** | **Moderate** | Helpful for shop floor supervision, team leading, and production management. |
| **Preference** | Investigative (I) | **0.00** | *Not Applicable* | Secondary to practical, hands-on industrial execution. |
| **Preference** | Artistic (A) | **0.00** | *Not Applicable* | Minor relevance to core industrial production. |
| **Preference** | Social (S) | **0.00** | *Not Applicable* | Secondary to technical machinery operation. |
| **Total** | | **1.00** | | |

---

### 4. Bachelor of Science in Hospitality Management (BSHM)
*Focus: Hotel and restaurant operations, culinary arts, customer service, event management, and tourism.*

| Category | Dimension | Weight | Minimum Level | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Aptitude** | Verbal/Communication Ability | **0.25** | **High** | Primary aptitude for guest relations, service delivery, and team management. |
| **Aptitude** | Problem-Solving | **0.15** | **High** | Crucial for resolving guest complaints, handling service crises, and event changes. |
| **Aptitude** | Logical Reasoning | **0.10** | **Moderate** | Required for scheduling, resource allocation, and operational decision-making. |
| **Aptitude** | Numerical Reasoning | **0.10** | **Moderate** | Necessary for POS billing, basic accounting, cost control, and inventory auditing. |
| **Aptitude** | Spatial Ability | **0.05** | **Low** | Useful for dining room layout design, banquet arrangements, and event decor. |
| **Aptitude** | Technical/Mechanical Reasoning | **0.05** | **Low** | Basic familiarity with commercial kitchen appliances and property management systems. |
| **Preference** | Social (S) | **0.15** | **Very High** | Essential preference match; passion for helping guests, service, and hospitality. |
| **Preference** | Enterprising (E) | **0.10** | **High** | Strong match for hotel management, marketing, event hosting, and resort sales. |
| **Preference** | Conventional (C) | **0.05** | **Moderate** | Needed for reservation logs, accounting records, and standard operating procedures. |
| **Preference** | Realistic (R) | **0.00** | *Not Applicable* | Secondary to service and management competencies. |
| **Preference** | Investigative (I) | **0.00** | *Not Applicable* | Secondary to interpersonal customer service. |
| **Preference** | Artistic (A) | **0.00** | *Not Applicable* | Minor relevance outside of culinary styling. |
| **Total** | | **1.00** | | |

---

### 5. Bachelor of Technical Vocational Teacher Education (BTVTed)
*Focus: Pedagogy, technical-vocational instruction, shop teaching, student assessment, and TVET curriculum delivery.*

| Category | Dimension | Weight | Minimum Level | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Aptitude** | Verbal/Communication Ability | **0.25** | **High** | Primary aptitude for classroom teaching, lecturing, lesson delivery, and mentoring. |
| **Aptitude** | Technical/Mechanical Reasoning | **0.15** | **High** | Essential for demonstrating trade skills, shop work, and technical specialization. |
| **Aptitude** | Problem-Solving | **0.15** | **High** | Critical for classroom management, student learning adaptation, and workshop safety. |
| **Aptitude** | Logical Reasoning | **0.05** | **Moderate** | Important for lesson planning, instructional sequencing, and fair grading logic. |
| **Aptitude** | Spatial Ability | **0.05** | **Low** | Useful for creating visual aids, shop floor layouts, and technical demonstrations. |
| **Aptitude** | Numerical Reasoning | **0.05** | **Low** | Needed for grade computations, scoring rubrics, and shop materials budgeting. |
| **Preference** | Social (S) | **0.15** | **Very High** | Strongest match; deep interest in teaching, helping learners grow, and community education. |
| **Preference** | Realistic (R) | **0.10** | **High** | Essential for hands-on shop work, practical trade skills, and vocational tools. |
| **Preference** | Conventional (C) | **0.05** | **Moderate** | Required for grading records, curriculum standards compliance, and school reporting. |
| **Preference** | Enterprising (E) | **0.00** | *Not Applicable* | Secondary to teaching and mentoring. |
| **Preference** | Investigative (I) | **0.00** | *Not Applicable* | Secondary to practical TVET instruction. |
| **Preference** | Artistic (A) | **0.00** | *Not Applicable* | Minor impact on vocational instruction. |
| **Total** | | **1.00** | | |

---

### 6. Bachelor of Science in Architecture (BSA)
*Focus: Spatial layout, architectural drafting, visual design, building construction technology, and environmental design.*

| Category | Dimension | Weight | Minimum Level | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Aptitude** | Spatial Ability | **0.25** | **Very High** | Primary cognitive requirement for 3D spatial visualization, drafting, and scale design. |
| **Aptitude** | Problem-Solving | **0.15** | **High** | Essential for balancing structural constraints, client requirements, and aesthetic function. |
| **Aptitude** | Numerical Reasoning | **0.10** | **High** | Required for structural geometry, scale calculations, trigonometry, and estimates. |
| **Aptitude** | Logical Reasoning | **0.10** | **Moderate** | Needed for functional building circulation, code compliance logic, and spatial flow. |
| **Aptitude** | Technical/Mechanical Reasoning | **0.05** | **Moderate** | Needed to understand building materials, construction assemblies, and structural systems. |
| **Aptitude** | Verbal/Communication Ability | **0.05** | **Moderate** | Needed for presenting design concepts, defending architectural proposals, and client meetings. |
| **Preference** | Artistic (A) | **0.15** | **Very High** | Primary interest match; creative design, visual aesthetics, drawing, and form expression. |
| **Preference** | Realistic (R) | **0.05** | **Moderate** | Alignment with physical scale modeling, construction materials, and site inspections. |
| **Preference** | Investigative (I) | **0.05** | **Moderate** | Interest in architectural history, site context analysis, and environmental research. |
| **Preference** | Conventional (C) | **0.05** | **Moderate** | Alignment with blueprint drafting standards, building code rules, and regulatory filing. |
| **Preference** | Enterprising (E) | **0.00** | *Not Applicable* | Secondary to design and drafting competency. |
| **Preference** | Social (S) | **0.00** | *Not Applicable* | Secondary to spatial design work. |
| **Total** | | **1.00** | | |

---

## 📈 Summary Comparison Matrix

The table below summarizes the recommended weight distribution across all 6 programs and 12 evaluation dimensions:

| Dimension | Category | BSCE | BS InfoTech | BSIT | BSHM | BTVTed | BSA |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Numerical Reasoning** | Aptitude | **0.20** | 0.10 | 0.10 | 0.10 | 0.05 | 0.10 |
| **Logical Reasoning** | Aptitude | 0.10 | **0.20** | 0.05 | 0.10 | 0.05 | 0.10 |
| **Problem-Solving** | Aptitude | **0.15** | **0.15** | **0.15** | **0.15** | **0.15** | **0.15** |
| **Spatial Ability** | Aptitude | **0.15** | 0.05 | 0.10 | 0.05 | 0.05 | **0.25** |
| **Technical/Mechanical** | Aptitude | 0.10 | 0.10 | **0.25** | 0.05 | **0.15** | 0.05 |
| **Verbal/Communication** | Aptitude | 0.05 | 0.10 | 0.05 | **0.25** | **0.25** | 0.05 |
| **Realistic (R)** | Preference | 0.10 | 0.05 | **0.15** | 0.00 | 0.10 | 0.05 |
| **Investigative (I)** | Preference | 0.10 | 0.10 | 0.00 | 0.00 | 0.00 | 0.05 |
| **Artistic (A)** | Preference | 0.00 | 0.05 | 0.00 | 0.00 | 0.00 | **0.15** |
| **Social (S)** | Preference | 0.00 | 0.00 | 0.00 | **0.15** | **0.15** | 0.00 |
| **Enterprising (E)** | Preference | 0.00 | 0.00 | 0.05 | 0.10 | 0.00 | 0.00 |
| **Conventional (C)** | Preference | 0.05 | 0.10 | 0.10 | 0.05 | 0.05 | 0.05 |
| **Total Weight** | | **1.00** | **1.00** | **1.00** | **1.00** | **1.00** | **1.00** |

---

## 🛠️ Automated Database Seeding Script

To quickly apply these recommended criteria to your Django database, run the seed script below or execute python manage.py shell with the script logic:

```python
# seed_program_criteria.py
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
    for abbrev, criteria_dict in PROGRAM_CRITERIA_MAP.items():
        try:
            program = Program.objects.get(abbreviation__iexact=abbrev)
            for dim_name, (weight, min_lvl) in criteria_dict.items():
                ProgramCriteria.objects.update_or_create(
                    program=program,
                    dimension_name=dim_name,
                    defaults={
                        'weight': weight,
                        'minimum_level': min_lvl
                    }
                )
            print(f"Updated criteria for program: {program.abbreviation} - {program.program_name}")
        except Program.DoesNotExist:
            print(f"Program with abbreviation '{abbrev}' not found in database.")

if __name__ == '__main__':
    sync_program_criteria()
```
