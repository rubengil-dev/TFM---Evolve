# notebooks/

Analysis notebooks. Run them with `uv run jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb`, so the kernel is the one of the project environment.

- **Deliverable notebooks** have a numeric prefix (`01_`, `02_`) and import nothing from `src/`.
- **Working notebooks** have no prefix and import from the `bioage` package: correlations, one per model level, biological age, the PhenoAge comparison and the final evaluation on test.
