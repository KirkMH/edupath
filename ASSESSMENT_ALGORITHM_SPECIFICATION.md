# Assessment Analysis & Program Recommendation Algorithm Specification

This document defines the mathematical models, step-by-step algorithms, data structures, and implementation guidelines for evaluating student assessment profiles and generating academic program recommendations in the **EduPath Decision Support System**.

---

## 📐 Algorithm Overview

The recommendation engine evaluates student performance across **12 Dimensions**:
1. **6 Aptitude Dimensions (Cognitive Abilities)**:
   - Numerical Reasoning
   - Logical Reasoning
   - Problem-Solving
   - Spatial Ability
   - Technical/Mechanical Reasoning
   - Verbal/Communication Ability
2. **6 Preference Dimensions (O*NET RIASEC Interest Areas)**:
   - Realistic (R)
   - Investigative (I)
   - Artistic (A)
   - Social (S)
   - Enterprising (E)
   - Conventional (C)

The evaluation process consists of four sequential phases:
```
[Phase 1: Score Normalization] ➔ [Phase 2: Score Interpretation] ➔ [Phase 3: Program Criteria Weighting] ➔ [Phase 4: Program Ranking]
```

---

## 🔢 Phase 1: Raw Score Calculation & Normalization

### 1. Formula
Raw scores from both Aptitude and Preference assessments are converted into a standardized **Normalized Score** (percentage from 0.00% to 100.00%) using the formula:

$$\text{Normalized Score} = \left( \frac{\text{Raw Score}}{\text{Maximum Possible Score}} \right) \times 100$$

### 2. Dimension Question Specs & Maximum Possible Scores

| Category | Dimension Count | Questions Per Dimension | Scoring Scheme | Max Possible Score Per Dimension |
| :--- | :---: | :---: | :--- | :---: |
| **Aptitude** | 6 | **8 Questions** | Binary: Correct = 1, Incorrect = 0 | **8 Points** |
| **Preference (RIASEC)** | 6 | **10 Questions** | 5-point Likert Scale (1 = Strongly Dislike to 5 = Strongly Like) | **40 Points** *(or 50 Points)* |

#### Detailed Normalization Rules:

1. **Aptitude Dimensions (8 Questions per Dimension)**:
   - $\text{Raw Score}_{\text{aptitude}} = \sum_{i=1}^{8} \text{is\_correct}_i \quad (\text{range: } 0 \text{ to } 8)$
   - $\text{Normalized Score}_{\text{aptitude}} = \left( \frac{\text{Raw Score}_{\text{aptitude}}}{8} \right) \times 100$

2. **Preference / RIASEC Dimensions (10 Questions per Dimension)**:
   - *O*NET Short Form Scale*: Ratings are 1 to 5.
   - Points per item = $(\text{Rating} - 1)$ (range 0 to 4 points per question).
   - $\text{Raw Score}_{\text{preference}} = \sum_{i=1}^{10} (\text{Rating}_i - 1) \quad (\text{range: } 0 \text{ to } 40)$
   - $\text{Normalized Score}_{\text{preference}} = \left( \frac{\text{Raw Score}_{\text{preference}}}{40} \right) \times 100$
   - *(Note: If using direct 1–5 rating sum without subtracting 1, Raw Score range is 10 to 50, and $\text{Normalized Score} = \frac{\text{Raw Score}}{50} \times 100$)*.

---

## 🏷️ Phase 2: Qualitative Score Interpretation

Each calculated **Normalized Score** (0.00% – 100.00%) is mapped to a qualitative performance tier band using the configurable `ScoreInterpretation` table.

### Score Interpretation Tiers

| Qualitative Tier Label | Minimum Normalized Score ($\%$) | Maximum Normalized Score ($\%$) | Qualitative Level Description |
| :--- | :---: | :---: | :--- |
| **Very High** | **80.00%** | **100.00%** | Exceptional strength/interest in this dimension |
| **High** | **60.00%** | **79.99%** | Strong competency/interest |
| **Moderate** | **40.00%** | **59.99%** | Average competency/interest |
| **Low** | **20.00%** | **39.99%** | Below average competency/interest |
| **Very Low** | **0.00%** | **19.99%** | Minimal competency/interest |

### Threshold Order Hierarchy
$$\text{Very High} (5) > \text{High} (4) > \text{Moderate} (3) > \text{Low} (2) > \text{Very Low} (1)$$

---

## ⚖️ Phase 3: Program Criteria Weighting & Threshold Evaluation

Each academic program ($P$) has a defined set of `ProgramCriteria` records specifying:
1. `dimension_name`: One of the 12 evaluation dimensions.
2. `weight`: Decimal weight allocated to the dimension (sum of weights per program = $1.00$).
3. `minimum_level`: Required threshold (`Very High`, `High`, `Moderate`, `Low`, `Very Low`, or `Not Applicable`).

### Calculation Logic per Program ($P$):

For each program $P$, calculate the **Total Match Score** ($S_P$) and **Weighted Accumulated Points** ($W_P$):

$$S_P = \sum_{d \in \text{Dimensions}} \left( \text{Normalized Score}_d \times \text{Weight}_{P, d} \right) \times \text{Threshold Multiplier}_{P, d}$$

#### Threshold Validation Rule:
For each dimension $d$:
- If `minimum_level` is **Not Applicable**: $\text{Threshold Multiplier} = 1.0$.
- If student's qualitative level $\ge$ program's `minimum_level`: $\text{Threshold Multiplier} = 1.0$ (criterion met).
- If student's qualitative level $<$ program's `minimum_level`: $\text{Threshold Multiplier} = 0.5$ (requirement penalty).

---

## 🏆 Phase 4: Program Ranking & Recommendation Selection

1. **Ranking**:
   - Sort all active academic programs in descending order of their calculated **Total Match Score** ($S_P$).
   - In case of a tie in total score, tie-breaker priority is given to the program with higher match in the student's top RIASEC primary interest code.

2. **Top Recommendations Assignment**:
   - **Top 1st Recommendation**: Program with the highest total match score ($P_1 \to \text{top\_recommended\_program}$).
   - **Top 2nd Recommendation**: Program with the 2nd highest total match score ($P_2 \to \text{second\_recommended\_program}$).
   - **Top 3rd Recommendation**: Program with the 3rd highest total match score ($P_3 \to \text{third\_recommended\_program}$).

3. **Overall Alignment Level Determination**:
   - The calculated match score of the top recommended program ($S_{P_1}$) is passed directly through the `ScoreInterpretation` model tiers to determine the `alignment_level`:
     - $80.00\% \le S_{P_1} \le 100.00\% \implies \text{alignment\_level} = \text{"Very High"}$
     - $60.00\% \le S_{P_1} < 80.00\% \implies \text{alignment\_level} = \text{"High"}$
     - $40.00\% \le S_{P_1} < 60.00\% \implies \text{alignment\_level} = \text{"Moderate"}$
     - $20.00\% \le S_{P_1} < 40.00\% \implies \text{alignment\_level} = \text{"Low"}$
     - $0.00\% \le S_{P_1} < 20.00\% \implies \text{alignment\_level} = \text{"Very Low"}$

---

## 📌 Key Notes for Implementation

1. **Aptitude Question Count Guard**: If a dimension has fewer or more than 8 questions in the DB, the formula $\frac{\text{Correct Count}}{\text{Total Questions in DB}} \times 100$ should be used dynamically as a fallback.
2. **Preference Rating Scale**: 10 questions per RIASEC area, 40 points max ($10 \times 4$), yielding $\frac{\text{Raw Score}}{40} \times 100$.
3. **Score Interpretation Configuration**: Configurable via the `ScoreInterpretation` Django Admin panel.
4. **Data Persistence**: All normalized scores and top 3 recommendations are saved in `AssessmentResult`.

