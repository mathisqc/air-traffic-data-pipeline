import pandas as pd


def clean_opensky_data(df):

    # copie données d'origine
    df_clean = df.copy()

    # Suppression colonnes entièrement vide
    empty_columns = df_clean.columns[df_clean.isna().all()].tolist()
    df_clean = df_clean.drop(columns=empty_columns)

    # Nettoyages des colonnes de type texte
    text_columns = ["icao24", "callsign", "origin_country", "squawk"]

    for column in text_columns:
        if column in df_clean.columns:
            df_clean[column] = df_clean[column].str.strip()

    # Conversion timestamps Unix (secondes depuis 1970) vers UTC
    df_clean["time_position"] = pd.to_datetime(
        df_clean["time_position"],
        unit="s",
        utc=True,
        errors="coerce"
    )

    df_clean["last_contact"] = pd.to_datetime(
        df_clean["last_contact"],
        unit="s",
        utc=True,
        errors="coerce"
    )

    # Suppression doublons
    df_clean = df_clean.drop_duplicates()

    # Suppression si pas de icao24 (info la plus importante)
    df_clean = df_clean.dropna(subset=["icao24"])

    # Fourchette normale des coordonnées
    valid_coordinates = (
        df_clean["latitude"].between(-90, 90)
        & df_clean["longitude"].between(-180, 180)
    )

    df_clean = df_clean[valid_coordinates].copy()

    # Vitesse négative supprimées
    df_clean.loc[df_clean["velocity"] < 0, "velocity"] = pd.NA

    # Vérification de la direction valide : 0 <= true_track < 360
    invalid_track = ~df_clean["true_track"].between(
        0, 360, inclusive="left"
    )

    df_clean.loc[invalid_track, "true_track"] = pd.NA

    # Repères valeurs suspectes
    df_clean["velocity_suspicious"] = (
        df_clean["velocity"] > 400
    )

    df_clean["baro_altitude_suspicious"] = (
        df_clean["baro_altitude"] > 14000
    )

    df_clean["geo_altitude_suspicious"] = (
        df_clean["geo_altitude"] > 14000
    )

    df_clean["vertical_rate_suspicious"] = (
        df_clean["vertical_rate"].abs() > 50
    )

    return df_clean