## AUDITS - Evaluates if the model works how it claims to work

**RF-model performance audit:** 
Standard ML metrics of checking accuracy , precision, and recall/F1 score for each diseases classes.

**Confusion matrix:** 
Checks which diseases got confused and which ones did not. Can be found in `notebooks/05_evaluation.ipynb`

**Feature importance review:**
Checks if the RF is relying heavily on proxy features in the datasets. 

**Train/test split integrity:** 
Confirms there are no leakages like duplicate rows and accidentally training on test data. 

**A calibration check:** 
Check if the RFs predicted probabilities correspond to the real likelihood or overfitting is occurring.

**Consistency audit:** 
Same symptoms that are framed differently should have the same result.

**End to End pipeline test:** 
Run dangerous cases through the full pipeline.

**Privacy and data audit:** 
To confirm actual data handling matches the stated privacy policy.

**Dataset audit:** 
Datasets should be traced back to its original source. Datasets license actually permits usage and when the datasets was created and last updated. 

*=================================================================================*

## ETHICS - How should it work

**1. Scope definition:** This is a triage support and predictions are made based on the Random Forest model not a full diagnosis.

**2. Uncertainty disclosure:** The model's output should reflect uncertainty. Eg: An output can be in the form " The symptoms are consistent with several diseases including malaria , typhoid etc". It should not be in the form " The symptoms mean you likely have malaria".

**3. Rare / Undertrained class disclosure:** Any disease with very few examples should be listed as low confidence.

**4. Non-affiliation disclaimer:** This project does not have medical backing. Users should still seek the knowledge of a licensed clinician. 

**5. Consent for data reuse:** Users must consent before their data is used for training.
