# models/

The trained model of each level (fitted pipeline, the biological age reference and its gold columns), one `.joblib` per level: `routine`, `extras`, `questionnaire` and `full`. 

Load them with `bioage.app.predict.load_bundle`, never with `joblib` directly: it fails if the installed versions differ from the saved ones.

NOTE: They are in git because the app needs them and its server cannot rebuild them without downloading NHANES.
