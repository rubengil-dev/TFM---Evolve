# pipeline/

One file per pipeline step, in order: `s1_download_bronze`, `s2_build_raw_silver`, `s3_build_clean_silver`, `s4_build_gold` and `s5_build_model`. Each one has a `run()` that `main.py` calls.

The `s` prefix is there because Python cannot import modules whose name starts with a number.
