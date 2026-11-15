# models/

The steps of the model, one file per step and not per model: `s1_split`, `s2_preprocessing`, `s3_algorithms`, `s4_biological_age` and `s5_evaluation`. The four levels are the same process with a different list of variables.

`predict.py` is what the app uses: it loads a saved model and computes the biological age without the training libraries.

Do not move or rename `s2_preprocessing.py` (or the package) without retraining: the saved models point to its import path.
