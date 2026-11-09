# Assessment Analysis & Program Recommendation Algorithm Specification

This document defines the scoring models, step-by-step algorithms, data structures, and implementation rules used to evaluate student assessment profiles and generate academic program and major recommendations in the **EduPath Decision Support System**.

It describes the behavior implemented in `assessment/services.py` and `assessment/views.py`.

---

## 📐 Algorithm Overview

The recommendation engine evaluates students across **12 Dimensions**:
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

The evaluation process consists of six sequential phases:
```
[Phase 1: Score Calculation & Normalization] ➔ [Phase 2: Score Interpretation] ➔ [Phase 3: GWA Eligibility Gate]
  ➔ [Phase 4: Program Criteria Weighting] ➔ [Phase 5: Program Ranking] ➔ [Phase 6: Major Recommendation]
```

| Phase | Function |
| :--- | :--- |
| 1 (Aptitude) | `calculate_aptitude_dimension_scores()` |
| 1 (RIASEC) | `get_riasec_results()` |
| 2 | `lookup_score_interpretation()` |
| 3 – 5 | `calculate_program_recommendations()` |
| 6 | `calculate_major_recommendations()` |
| Persistence | `calculate_and_save_assessment_results()` |

---

## 🔢 Phase 1: Raw Score Calculation & Normalization

### 1. Formula
Raw scores are converted into a **Normalized Score** (percentage from 0% to 100%):

$$\text{Normalized Score} = \left( \frac{\text{Raw Score}}{\text{Maximum Possible Score}} \right) \times 100$$

### 2. Dimension Question Specs & Maximum Possible Scores

| Category | Dimension Count | Questions Per Dimension | Scoring Scheme | Max Possible Score Per Dimension |
| :--- | :---: | :---: | :--- | :---: |
| **Aptitude** | 6 | **8 Questions** (active questions in DB) | Binary: Correct = 1, Incorrect or unanswered = 0 | **Number of active questions** (8) |
| **Preference (RIASEC)** | 6 | **10 Questions** | 5-point Likert Scale (1 = Strongly Dislike to 5 = Strongly Like), scored as $(\text{Rating} - 1)$ | **40 Points** |

### 3. Aptitude Dimensions

- Only questions with `status = True` (Active) are presented and counted.
- The `for_validation` flag does **not** affect scoring; active questions are scored whether or not they are marked for validation.
- $\text{Raw Score}_{\text{aptitude}} = \sum \text{is\_correct}_i$ over the student's responses in that dimension.
- $\text{Max}_{\text{aptitude}} = $ number of active questions in that dimension. If a dimension has no active questions, 8 is used.
- $\text{Normalized Score}_{\text{aptitude}} = \text{round}\left( \frac{\text{Raw Score}_{\text{aptitude}}}{\text{Max}_{\text{aptitude}}} \times 100 \right)$, clamped to 0–100.
- Aptitude scores are stored and used as **whole-number percentages**.

### 4. Preference / RIASEC Dimensions

RIASEC raw scores (0–40 per area) are obtained in this order:

1. **Primary – O*NET Web Services**: the student's 60 ratings are sent, in `item_number` order, as a 60-character answer string to `mnm/interestprofiler/results`. The returned `score` per area is used as the raw score. An item the student did not rate is sent as `3`.
2. **Fallback – local calculation**: if the API call fails or returns no usable scores, the raw score is computed from the stored responses:
   - Points per item = $(\text{Rating} - 1)$, range 0 to 4.
   - $\text{Raw Score}_{\text{preference}} = \sum_{i=1}^{10} (\text{Rating}_i - 1) \quad (\text{range: } 0 \text{ to } 40)$
   - An item the student did not rate contributes 0 points.

Normalization (used for interpretation, weighting, and display):

$$\text{Normalized Score}_{\text{preference}} = \min\left(100, \frac{\text{Raw Score}_{\text{preference}}}{40} \times 100\right)$$

- The recommendation engine uses the unrounded value (multiples of 2.5%).
- The results page displays it rounded to a whole percent.

### 5. RIASEC Interest Code

- The three areas with the highest raw scores form the code, joined by hyphens (e.g. `R-I-A`).
- Ties are broken by the fixed order **R > I > A > S > E > C**.
- The first letter is the student's **primary RIASEC area**.

---

## 🏷️ Phase 2: Qualitative Score Interpretation

Each Normalized Score is mapped to a qualitative tier using the configurable `ScoreInterpretation` table. The first tier whose range satisfies $\text{min\_score} \le \text{score} \le \text{max\_score}$ is used.

### Score Interpretation Tiers (default configuration)

| Qualitative Tier Label | Minimum Normalized Score ($\%$) | Maximum Normalized Score ($\%$) | Qualitative Level Description |
| :--- | :---: | :---: | :--- |
| **Very High** | **80.00%** | **100.00%** | Exceptional strength/interest in this dimension |
| **High** | **60.00%** | **79.99%** | Strong competency/interest |
| **Moderate** | **40.00%** | **59.99%** | Average competency/interest |
| **Low** | **20.00%** | **39.99%** | Below average competency/interest |
| **Very Low** | **0.00%** | **19.99%** | Minimal competency/interest |

**Fallback**: if no configured tier matches (for example, a score between 79.99 and 80.00, or an empty table), these fixed thresholds are applied: $\ge 80$ Very High, $\ge 60$ High, $\ge 40$ Moderate, $\ge 20$ Low, otherwise Very Low.

### Threshold Order Hierarchy
$$\text{Very High} (5) > \text{High} (4) > \text{Moderate} (3) > \text{Low} (2) > \text{Very Low} (1) > \text{Not Applicable} (0)$$

---

## 🎓 Phase 3: GWA Eligibility Gate

Before scoring, each program is checked against its optional `Program.min_gwa` (Minimum GWA Cutoff):

- If `min_gwa` is empty or 0, the program is eligible.
- If $\text{student GWA} < \text{min\_gwa}$, the program is **disqualified**: it is not scored, ranked, or recommended.
- A student with no recorded GWA is treated as GWA 0, so they are disqualified from every program that has a cutoff.

The GWA gate applies to programs only. Majors have no GWA cutoff.

---

## ⚖️ Phase 4: Program Criteria Weighting & Threshold Evaluation

Each academic program ($P$) has one `ProgramCriteria` record per dimension (created automatically with weight 0 and `Not Applicable` when a program is saved), specifying:
1. `dimension_name`: One of the 12 evaluation dimensions.
2. `weight`: Decimal weight allocated to the dimension. Weights per program should sum to $1.00$.
3. `minimum_level`: Required tier (`Very High`, `High`, `Moderate`, `Low`, `Very Low`, or `Not Applicable`).

### Calculation Logic per Program ($P$)

$$S_P = \frac{\sum_{d} \left( \text{Normalized Score}_d \times \text{Weight}_{P,d} \times \text{Threshold Multiplier}_{P,d} \right)}{\sum_{d} \text{Weight}_{P,d}}$$

- Dividing by the total weight keeps $S_P$ on a 0–100 scale even if the weights do not sum to exactly 1.00. When they do sum to 1.00, the denominator has no effect.
- If the total weight is 0, the numerator is used as is (which is 0).
- A dimension with weight 0 has no effect on $S_P$, even if it has a `minimum_level`.

#### Threshold Validation Rule
For each dimension $d$:
- If `minimum_level` is **Not Applicable**: $\text{Threshold Multiplier} = 1.0$.
- If the student's tier rank $\ge$ the required tier rank: $\text{Threshold Multiplier} = 1.0$ (criterion met).
- If the student's tier rank $<$ the required tier rank: $\text{Threshold Multiplier} = 0.5$ (requirement penalty).

---

## 🏆 Phase 5: Program Ranking & Recommendation Selection

1. **Ranking**:
   - All eligible programs (every `Program` that passes the GWA gate; there is no separate active flag) are sorted in descending order of $S_P$.
   - The secondary sort key is the student's normalized score in their primary RIASEC area. This value is the same for every program, so it does not change the order. Programs with equal $S_P$ keep their database order.

2. **Top Recommendations Assignment**:
   - **Top 1st Recommendation**: Highest $S_P$ ($P_1 \to \text{top\_recommended\_program}$).
   - **Top 2nd Recommendation**: 2nd highest $S_P$ ($P_2 \to \text{second\_recommended\_program}$).
   - **Top 3rd Recommendation**: 3rd highest $S_P$ ($P_3 \to \text{third\_recommended\_program}$).
   - If fewer than three programs are eligible, the remaining recommendations are empty.

3. **Alignment Levels**:
   - Each of the top three programs gets its own alignment level by passing its $S_P$ through the Phase 2 tiers. The results page shows it with the match score, e.g. `11.2% (Very Low)`.
   - The **overall** `alignment_level` saved in `AssessmentResult` is the alignment level of $P_1$:
     - $80.00\% \le S_{P_1} \le 100.00\% \implies$ "Very High"
     - $60.00\% \le S_{P_1} < 80.00\% \implies$ "High"
     - $40.00\% \le S_{P_1} < 60.00\% \implies$ "Moderate"
     - $20.00\% \le S_{P_1} < 40.00\% \implies$ "Low"
     - $0.00\% \le S_{P_1} < 20.00\% \implies$ "Very Low"
   - Match scores are displayed rounded to one decimal place.

4. **Generated Explanation**:
   - With a top program: *"Based on your cognitive aptitude assessment and O\*NET RIASEC interest profile ({code}), your profile shows {alignment} alignment with {program name}."*
   - With no eligible program: *"Based on your assessment results, no academic programs currently match your criteria requirements."*

---

## 🧭 Phase 6: Major Recommendation

When a recommended program has majors, the student can open the major analysis for that program.

- Each `Major` under the program has one `MajorCriteria` record per dimension (created automatically, like program criteria), with the same `weight` and `minimum_level` fields.
- Each major's match score $S_M$ uses the **same formula and threshold rule as Phase 4**, with `MajorCriteria` in place of `ProgramCriteria`.
- No GWA gate is applied.
- All majors of the program are ranked by $S_M$ in descending order, with the same (non-distinguishing) RIASEC secondary key as Phase 5.
- Each major gets a rank, a match score (one decimal place), and an alignment level from the Phase 2 tiers.
- The page shows the top three majors as cards and every major in a ranking table.
- Major results are calculated on demand and are not saved.

---

## 💾 Data Persistence & Recalculation

`calculate_and_save_assessment_results()` runs after the preference assessment is submitted (from the loading page), and whenever a results page is opened without a saved result. It creates or updates one `AssessmentResult` per student with:

| Field(s) | Value |
| :--- | :--- |
| `numerical_score` … `verbal_score` | Aptitude Normalized Scores (whole-number %) |
| `r_score` … `c_score` | RIASEC **raw** scores (0–40), not percentages |
| `riasec_code` | Top three RIASEC areas, e.g. `R-I-A` |
| `top_recommended_program`, `second_…`, `third_…` | $P_1$, $P_2$, $P_3$ |
| `alignment_level` | Alignment level of $P_1$ |
| `generated_explanation` | Phase 5 explanation text |

Not saved:
- Per-program match scores and per-program alignment levels.
- Major rankings.

The results page **recalculates** the program ranking from the saved dimension scores each time it is viewed, using the current `ProgramCriteria`, `min_gwa`, and `ScoreInterpretation` settings. If an admin changes these after the assessment, the program cards can differ from the saved top three, which the dashboard shows.

**Retake**: resetting the assessment deletes the student's aptitude responses, interest responses, and `AssessmentResult`.

---

## 📌 Key Notes for Implementation

1. **Aptitude Question Count**: The denominator per dimension is the number of active questions in the DB; 8 is used only when a dimension has none.
2. **Preference Rating Scale**: 10 questions per RIASEC area, 40 points max ($10 \times 4$), normalized as $\frac{\text{Raw Score}}{40} \times 100$.
3. **Score Interpretation Configuration**: Configurable via the `ScoreInterpretation` Django Admin panel; fixed fallback thresholds apply when no tier matches.
4. **Criteria Configuration**: Program and major weights and minimum levels are configured in the Django Admin panel. Weights per program or major should sum to 1.00.
5. **Known limitation – tie-breaking**: The intended RIASEC tie-breaker uses a value that is the same for every program or major, so tied scores fall back to database order.
6. **Known limitation – unanswered interest items**: The O*NET path treats an unrated item as a rating of 3, while the local fallback gives it 0 points, so the same incomplete set of answers can produce different RIASEC scores depending on whether the API is reachable.
