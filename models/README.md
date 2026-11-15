# models/

The trained model of each level, one `.joblib` per level: `base`, `extras`, `questionnaire` and `full`. They are in git because the app needs them and its server cannot rebuild them without downloading NHANES.

Each file holds the fitted pipeline, the biological age reference, its columns and where it comes from (data fingerprint, code commit and library versions). Load them with `bioage.models.predict.load_bundle`, never with `joblib` directly: it fails if the installed versions differ from the saved ones.

They are trained on all of Gold, test included, so they are not valid for evaluation. Retrain only after committing the code, and commit the models separately.
