## Sankofa Symptom Checker: Ethics and Model Audit

This audit reviews whether Sankofa behaves consistently with its intended purpose: educational triage support that suggests possible conditions from user-reported symptoms. It is not a diagnostic system, medical device, or substitute for a licensed clinician.

---

## 1. Intended Use and Scope

Sankofa accepts a list of user-reported symptoms and returns the top possible disease classes with probability scores from a trained Random Forest classifier. The output should be framed as "possible conditions consistent with these symptoms," not as a confirmed diagnosis.

Appropriate use:

- Supporting an educational AI project demonstration.
- Showing how symptom indicators can be mapped to possible disease classes.
- Encouraging users to seek professional medical advice when symptoms are serious, persistent, unclear, or worsening.

Out-of-scope use:

- Emergency triage or crisis response.
- Final diagnosis or treatment recommendation.
- Medication, dosage, or clinical management advice.
- Use with real patient data without consent, privacy safeguards, and clinical oversight.

---

## 2. Data and Training Summary

The model was trained using the cleaned symptom-disease dataset in `cleaned_diseases_symptoms.csv`.

From `notebooks/04_training.ipynb`:

- Loaded dataset shape: 101,485 rows and 377 columns.
- Loaded disease classes: 658 unique diseases.
- Diseases with fewer than 20 samples were filtered out before training.
- Filtered dataset shape: 99,926 rows and 377 columns.
- Final modeled disease classes: 512.
- Symptom feature columns: 376.
- Target column: `diseases`.

The model uses a stratified 60/20/20 train, validation, and test split:

- Train: 59,955 rows.
- Validation: 19,985 rows.
- Test: 19,986 rows.

The trained artifacts include:

- `random_forest.pkl`
- `label_encoder.pkl`
- `symptom_columns.pkl`

---

## 3. Model Summary

The selected model is a `RandomForestClassifier` with:

- `n_estimators=200`
- `max_depth=None`
- `min_samples_leaf=3`
- `min_samples_split=5`
- `max_features="sqrt"`
- `class_weight="balanced"`
- `random_state=42`
- `n_jobs=-1`

The model uses binary symptom indicators as features. Each input symptom is matched against the saved symptom column list. Recognized symptoms are set to 1 in the input vector. Unknown symptoms are ignored with a warning.

---

## 4. Performance Audit

From `notebooks/04_training.ipynb` and `notebooks/05_evaluation.ipynb`, the final model reports:

| Split      | Accuracy | Macro-F1 |
| ---------- | -------: | -------: |
| Train      |   89.17% |   86.92% |
| Validation |   84.02% |   81.29% |
| Test       |   83.69% |   80.84% |

The evaluation notebook also reports:

- Test weighted-F1: 84.31%.
- Majority-class baseline accuracy: 0.30%.
- Random Forest improvement over baseline: 83.39 percentage points.

Interpretation:

- The validation and test scores are close, which suggests reasonable generalization to held-out data.
- The train score is higher than validation/test scores, so some overfitting remains.
- Weighted-F1 is slightly higher than macro-F1, suggesting the model performs better on more common classes than on lower-support classes.
- Per-class results show that some diseases perform very well, while others still have weak F1-scores, especially where support is low or symptoms overlap with other conditions.

---

## 5. Inference Behavior Audit

From `src/models/predict.ipynb` and `src/models/predict.py`, the prediction flow is:

1. Load the trained Random Forest, label encoder, and symptom column list.
2. Create a zero-filled binary vector with one position per known symptom.
3. Normalize each user-provided symptom with `strip().lower()`.
4. Set recognized symptom positions to 1.
5. Ignore unknown symptoms and print a warning.
6. Convert the vector into a DataFrame with the same columns used in training.
7. Use `predict_proba()` to score disease classes.
8. Return the top N disease names and percentage scores.

The testing groups in `predict.ipynb` include respiratory, musculoskeletal, neurological, gastrointestinal, urinary, cardiac, skin, mental health, eye, and ENT examples. These examples are useful sanity checks because they confirm that common symptom groups are recognized and produce plausible top-five outputs.

**Key limitation**:

Unknown symptoms are currently ignored rather than mapped semantically or flagged as reducing confidence. This can make results look more certain than they should if the user enters symptoms that are phrased differently from the training feature names.

---

## 6. Safety and Ethical Risks

### Medical Harm Risk

Users may misunderstand the output as a diagnosis. This is especially risky for serious symptoms such as chest pain, shortness of breath, neurological weakness, severe abdominal pain, or mental health crises.

Mitigation:

- Always present results as possible conditions, not conclusions.
- Add a visible disclaimer that the tool is not a replacement for medical care.
- Include emergency guidance for severe or urgent symptoms.

### Class Imbalance and Rare Disease Risk

The model filters out diseases with fewer than 20 samples, and lower-support classes still perform worse in evaluation. Rare diseases may be underrepresented or excluded.

Mitigation:

- Report low confidence when inputs point toward historically weak or low-support classes.
- Continue tracking per-class precision, recall, F1-score, and support.
- Avoid claiming broad clinical coverage.

### Symptom Wording Risk

The inference pipeline requires symptoms to match known symptom columns exactly after lowercasing and trimming. Different wording may be ignored.

Mitigation:

- Display unknown symptoms to users.
- Add a symptom search/autocomplete layer that maps user wording to known symptom labels.
- Reduce confidence or request clarification when many symptoms are unknown.

### Probability Misinterpretation Risk

Random Forest probabilities are model confidence scores, not true medical likelihoods.

Mitigation:

- Describe scores as model-estimated confidence or ranking scores.
- Run calibration checks before presenting probabilities as likelihoods.
- Consider grouping outputs into confidence bands instead of precise percentages.

### Bias and Representation Risk

The source datasets may not represent all populations, regions, ages, sexes, languages, or healthcare contexts equally. A model trained on such data can reproduce those gaps.

Mitigation:

- Document dataset sources, licenses, update dates, and population coverage where available.
- Audit performance by demographic groups if demographic data is ever introduced.
- Avoid collecting demographic or health data unless it is necessary and consented to.

### Privacy Risk

Symptoms can be sensitive health information.

Mitigation:

- Do not store user symptoms by default.
- If logs are needed, remove personal identifiers and obtain explicit consent.
- Keep any collected data access-controlled and delete it when no longer needed.

---

## 7. Required User-Facing Disclosures

The app should clearly communicate:

- Sankofa is an educational AI symptom checker, not a doctor.
- Results are possible conditions, not diagnoses.
- The model may be wrong, especially for rare diseases or incomplete symptom descriptions.
- Serious, sudden, or worsening symptoms require urgent medical attention.
- Users should consult a licensed clinician for diagnosis and treatment.
- User symptom data should not be reused for training unless the user explicitly consents.

Suggested output wording:

> "These symptoms may be consistent with several possible conditions. This result is generated by an AI model and is not a medical diagnosis. Please consult a qualified health professional, especially if symptoms are severe, sudden, or worsening."

---

## 8. Audit Checklist

Completed:

- Training, validation, and test metrics reviewed.
- Majority-class baseline comparison reviewed.
- Per-class report reviewed.
- Confusion matrix generated for selected high-performing classes.
- Feature importance reviewed.
- Inference behavior reviewed from the prediction notebook and script.

Still needed:

- Probability calibration check.
- Duplicate-row and leakage audit across train/validation/test splits.
- Full confusion-matrix review beyond only the best-performing classes.
- Review of excluded diseases after the minimum-sample filter.
- Dataset source, license, and update-date verification.
- User-facing disclaimer review in the final frontend.
- End-to-end tests for high-risk symptom combinations.
- Privacy review once the final app data flow is confirmed.

---

## 9. Final Assessment

Sankofa shows strong performance compared with a majority-class baseline and reasonable generalization on the held-out test set. However, the system still has important ethical and technical limitations: it is not clinically validated, it relies on exact symptom matching, it performs unevenly across disease classes, and its probability scores should not be treated as real-world disease likelihoods without calibration.

The system is suitable as an educational AI project and prototype, provided its outputs are framed cautiously and paired with clear medical, uncertainty, and privacy disclosures.
