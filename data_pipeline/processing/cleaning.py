import pandas as pd


def clean(df):

    df = df.dropna()

    df = df[df["distance"] > 0]

    return df