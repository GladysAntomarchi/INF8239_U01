from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "online_shoppers_intention.csv"
)

TARGET = "Revenue"

REQUIRED_COLUMNS = {
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
    "Revenue",
}


def load_dataset() -> pd.DataFrame:
    assert DATA_PATH.exists(), (
        f"No se encontró el dataset en: {DATA_PATH}"
    )
    return pd.read_csv(DATA_PATH)


def test_dataset_is_not_empty_and_has_minimum_rows():
    df = load_dataset()

    assert not df.empty
    assert len(df) >= 500


def test_required_columns_are_present():
    df = load_dataset()

    assert REQUIRED_COLUMNS.issubset(df.columns)


def test_target_has_no_missing_values():
    df = load_dataset()

    assert df[TARGET].isna().sum() == 0


def test_target_has_at_least_two_classes():
    df = load_dataset()

    assert df[TARGET].nunique() >= 2