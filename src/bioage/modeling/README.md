# modeling/

One file per ML step, in order:

- `s1_split.py`         : ML Pipeline: Step 1 - Splitting Gold.
- `s2_preprocessing.py` : ML Pipeline: Step 2 - Preprocessing.
- `s3_algorithms.py`    : ML Pipeline: Step 3 - Building the model(s).
- `s4_biological_age.py`: ML Pipeline: Step 4 - Translating mortality risk to BioAge.
- `s5_evaluation.py`    : ML Pipeline: Step 5 - Model evaluation.

NOTE: Every model level follows the same process with different variables.
