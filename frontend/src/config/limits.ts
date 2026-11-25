/** Numbers repeated from the backend config - tests/test_frontend_config.py checks they match. */

// Ages the app calculates for (app.py)
export const MIN_AGE = 16
export const MAX_AGE = 90

// Ages of the data (study.py)
export const DATA_MIN_AGE = 18
export const DATA_MAX_AGE = 79

// Lowest and highest answer (plausible_ranges.py)
export const WEIGHT = [30, 300]
export const HEIGHT = [120, 220]
export const SEDENTARY_HOURS = [0, 24]
export const SLEEP_HOURS = [2, 16]
