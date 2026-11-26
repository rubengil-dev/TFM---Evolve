"""What enters and leaves each endpoint of the app.

In order of use:
- `RequestModel` : Unknown fields are refused; base of `OddValue`, `Person` and `Habits`.
- `AppError`     : Reason why no age can be calculated, at any step.
- `Reading`      : What was read from the PDF: blood values, and sex and age if it has them.
- `OddValue`     : Each blood value outside its plausible range; comes back corrected.
- `Correction`   : Values corrected, and those still outside.
- `Person`       : What the calculation needs: blood values, sex, age, weight and height.
- `Habits`       : Answers of the habits questionnaire.
- `Result`       : Biological age, its margin and the years of each group.
"""

# Imports
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat
from pydantic.fields import FieldInfo

from bioage.config.app import BLOOD_GROUPS, HABIT_GROUPS, MODE_LEVELS, ErrorCode
from bioage.config.model_levels import LabVariable
from bioage.config.plausible_ranges import PLAUSIBLE_RANGES
from bioage.config.study import CATEGORICAL_LEVELS

# quick = blood test only; full = blood test + habits
Mode = Literal[*MODE_LEVELS]


class RequestModel(BaseModel):
    """Data from the browser: unknown fields are refused."""

    model_config = ConfigDict(extra="forbid")


class AppError(Exception):
    """No age can be calculated, for a reason the user has to know."""

    def __init__(self, code: ErrorCode) -> None:
        """Keep the code of the reason.

        Args:
            code: Code of the reason.
        """
        super().__init__(code)
        self.code = code


class OddValue(RequestModel):
    """A value outside its plausible range, as the PDF shows it or as the user corrects it."""

    variable: LabVariable
    text: str = Field(pattern=r"^\s*\d+([.,]\d+)?\s*$")  # as the lab writes it, e.g. "4,5"
    unit: str
    factor: FiniteFloat = Field(gt=0)  # lab unit → model unit; TODO: from the table of the parser


class Correction(BaseModel):
    """What was corrected, in model units, and what is still odd."""

    lab_values: dict[LabVariable, FiniteFloat]
    odd: list[OddValue]


class Reading(BaseModel):
    """What was read from a PDF, in model units; age or sex missing if the PDF lacks them."""

    lab_values: dict[LabVariable, FiniteFloat]
    sex: Literal[*CATEGORICAL_LEVELS["sex"]] | None
    age: int | None
    odd: list[OddValue]


def answer_range(variable: str) -> FieldInfo:
    """Limits of a numeric answer: the plausible range of its variable.

    Args:
        variable: Name of the variable.

    Returns:
        Field with those limits.
    """
    low, high = PLAUSIBLE_RANGES[variable][2]
    return Field(ge=low, le=high)


class Person(RequestModel):
    """Everything known about the user: PDF values, body measures and, in the full mode, habits."""

    lab_values: dict[LabVariable, FiniteFloat]
    sex: Literal[*CATEGORICAL_LEVELS["sex"]]
    age: int
    weight: Annotated[float, answer_range("weight")]
    height: Annotated[float, answer_range("height")]
    habits: "Habits | None" = None

    @property
    def mode(self) -> Mode:
        """Mode of the person: full if they answered the habits."""
        return "quick" if self.habits is None else "full"


class Habits(RequestModel):
    """Answers about habits, in the full mode."""

    smoking: Literal[*CATEGORICAL_LEVELS["smoking"]]
    physical_activity: Literal[*CATEGORICAL_LEVELS["physical_activity"]]
    sedentary_hours: Annotated[float, answer_range("sedentary_hours")]
    sleep_hours: Annotated[float, answer_range("sleep_hours")]


class Result(BaseModel):
    """Biological age, its margin and the years of each group (None = not in the blood test)."""

    age: int
    bio_age: float
    margin: float | None = None
    blood: dict[Literal[*BLOOD_GROUPS], float | None]
    habits: dict[Literal[*HABIT_GROUPS], float] | None = None
