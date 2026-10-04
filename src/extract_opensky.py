import requests
import pandas as pd
import boto3

from datetime import datetime, timezone
from clean_opensky import clean_opensky_data


# URL API OpenSky
url = "https://opensky-network.org/api/states/all"

# Appel API
response = requests.get(url)
response.raise_for_status()

data = response.json()

# Heure de récupération de ce snapshot
snapshot_time = datetime.now(timezone.utc)


# Colonnes extraites d'OpenSky
columns = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source"
]


# Création du DataFrame brut
df_raw = pd.DataFrame(data["states"], columns=columns)

# Même snapshot_time pour toutes les observations
df_raw["snapshot_time"] = snapshot_time

print("Nombre d'observations RAW :", len(df_raw))


# Nettoyage Python
df_clean = clean_opensky_data(df_raw)

print("Nombre d'observations CLEAN :", len(df_clean))


# --------------------------------------------------
# ENVOI DES DONNÉES NETTOYÉES DANS AWS S3
# --------------------------------------------------

session = boto3.Session(profile_name="air-traffic-pipeline")
s3 = session.client("s3", region_name="eu-west-3")

bucket_name = "air-traffic-data-988277498718-eu-west-3-an"

# Conversion du DataFrame nettoyé en JSON
clean_json = df_clean.to_json(
    orient="records",
    date_format="iso"
)

# Nom unique basé sur l'heure du snapshot
timestamp_filename = snapshot_time.strftime("%Y%m%d_%H%M%S")

s3_key = f"processed/opensky_{timestamp_filename}.json"

# Envoi dans S3
s3.put_object(
    Bucket=bucket_name,
    Key=s3_key,
    Body=clean_json,
    ContentType="application/json"
)

print("Données CLEAN envoyées dans S3 :", s3_key)


# Aperçu
print("\nValeurs suspectes :")

print(
    df_clean[
        [
            "velocity_suspicious",
            "baro_altitude_suspicious",
            "geo_altitude_suspicious",
            "vertical_rate_suspicious"
        ]
    ].sum()
)

print("\nAperçu des données nettoyées :")

print(
    df_clean[
        [
            "icao24",
            "callsign",
            "origin_country",
            "latitude",
            "longitude",
            "baro_altitude",
            "velocity",
            "true_track",
            "snapshot_time"
        ]
    ].head(10)
)