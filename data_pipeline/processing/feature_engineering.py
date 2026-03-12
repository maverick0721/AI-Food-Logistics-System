def add_features(df):

    df["distance_traffic"] = df["distance"] * df["traffic"]

    df["prep_load"] = df["prep_time"] * df["driver_load"]

    return df