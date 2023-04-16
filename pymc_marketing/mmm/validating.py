from typing import Callable, List, Optional, Tuple, Union

import pandas as pd

__all__ = [
    "validation_method",
    "ValidateControlColumns",
    "ValidateTargetColumn",
    "ValidateDateColumn",
    "ValidateChannelColumns",
]


def validation_method(method: Callable) -> Callable:
    if not hasattr(method, "_tags"):
        method._tags = {}  # type: ignore
    method._tags["validation"] = True  # type: ignore
    return method


class ValidateTargetColumn:

    target_column: str

    @validation_method
    def validate_target(self, data: pd.DataFrame) -> None:
        if self.target_column not in data.columns:
            raise ValueError(f"target {self.target_column} not in data")


class ValidateDateColumn:

    date_column: str

    @validation_method
    def validate_date_col(self, data: pd.DataFrame) -> None:
        if self.date_column not in data.columns:
            raise ValueError(f"date_col {self.date_column} not in data")
        if not data[self.date_column].is_unique:
            raise ValueError(f"date_col {self.date_column} has repeated values")


class ValidateChannelColumns:

    channel_columns: Union[List[str], Tuple[str]]

    @validation_method
    def validate_channel_columns(self, data: pd.DataFrame) -> None:
        if not isinstance(self.channel_columns, (list, tuple)):
            raise ValueError("channel_columns must be a list or tuple")
        if len(self.channel_columns) == 0:
            raise ValueError("channel_columns must not be empty")
        if not set(self.channel_columns).issubset(data.columns):
            raise ValueError(f"channel_columns {self.channel_columns} not in data")
        if len(set(self.channel_columns)) != len(self.channel_columns):
            raise ValueError(
                f"channel_columns {self.channel_columns} contains duplicates"
            )
        if (data[self.channel_columns] < 0).any():
            raise ValueError(
                f"channel_columns {self.channel_columns} contains negative values"
            )


class ValidateControlColumns:

    control_columns: Optional[List[str]]

    @validation_method
    def validate_control_columns(self, data: pd.DataFrame) -> None:
        if self.control_columns is None:
            return None
        if not isinstance(self.control_columns, (list, tuple)):
            raise ValueError("control_columns must be None, a list or tuple")
        if len(self.control_columns) == 0:
            raise ValueError(
                "If control_columns is not None, then it must not be empty"
            )
        if not set(self.control_columns).issubset(data.columns):
            raise ValueError(f"control_columns {self.control_columns} not in data")
        if len(set(self.control_columns)) != len(self.control_columns):
            raise ValueError(
                f"control_columns {self.control_columns} contains duplicates"
            )
