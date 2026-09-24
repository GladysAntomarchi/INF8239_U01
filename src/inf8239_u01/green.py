import pandas as pd


def pareto_flags(
    df: pd.DataFrame,
    score: str = "f1_macro",
    cost: str = "fit_median_s",
) -> list[bool]:
    flags = []

    for _, row in df.iterrows():
        dominated = (
            (df[score] >= row[score])
            & (df[cost] <= row[cost])
            & (
                (df[score] > row[score])
                | (df[cost] < row[cost])
            )
        ).any()

        flags.append(not bool(dominated))

    return flags