import streamlit as st
import os
from dotenv import load_dotenv
import logging
import requests

import pandas as pd


# pio.renderers.default = "svg" # this line must be commented if working on colab
import plotly.express as px


load_dotenv()


logging.basicConfig(
    filename="kayak.log",
    format="%(asctime)s-%(levelname)s-%(message)s",
    level=logging.INFO,
)

# liste des 35 sites d'intérêt (POI)
pois = [
    "Mont Saint Michel",
    "St Malo",
    "Bayeux",
    "Le Havre",
    "Rouen",
    "Paris",
    "Amiens",
    "Lille",
    "Strasbourg",
    "Chateau du Haut Koenigsbourg",
    "Colmar",
    "Eguisheim",
    "Besancon",
    "Dijon",
    "Annecy",
    "Grenoble",
    "Lyon",
    "Gorges du Verdon",
    "Bormes les Mimosas",
    "Cassis",
    "Marseille",
    "Aix en Provence",
    "Avignon",
    "Uzes",
    "Nimes",
    "Aigues Mortes",
    "Saintes Maries de la mer",
    "Collioure",
    "Carcassonne",
    "Ariege",
    "Toulouse",
    "Montauban",
    "Biarritz",
    "Bayonne",
    "La Rochelle",
]


class FRANCE(Exception):
    pass


one_week_in_list = []


def nice_weather(poi_weather) -> float:
    """
    fonction pour definir la note d'attractivité de la poi en fonction des
    valeurs journalières sur les 7 prochains jour de la météo.
    Il est bon de mettre en place une stratégie pour laisser le choix sur
    la méthode de calcul de l'indice d'attractivité.
    """
    return poi_weather["weather_code"].mean()


# iteration sur la liste des pois
# pour récupérer via l'API nominatim les latitudes et longitudes de ces lieux.
pois_dict = {}
poi_nom, poi_latitude, poi_longitude, poi_France, poi_id, poi_weather, poi_nice = (
    [],
    [],
    [],
    [],
    [],
    [],
    [],
)
for poi in pois:
    print(poi)
    poi_nom.append(poi)
    chaine = poi.strip()
    params = {}
    params["format"] = "json"
    params["q"] = chaine.replace(" ", "+") + ",fr"  #'gorges+du+verdon'
    # params['country']='FR' # il est nécessaire de restreindre la localisation pour éviter des surprises au niveau mondial.
    headers = {"Accept": "*/*", "User-Agent": "jedha/ds-ft-35"}
    response = requests.get(
        "https://nominatim.openstreetmap.org/search", params=params, headers=headers
    )  # ?q=gorges+du+verdon&format=json
    data = response.json()
    poi_id.append(int(data[0]["osm_id"]))
    try:
        latitude = float(data[0]["lat"])
        poi_latitude.append(latitude)
        longitude = float(data[0]["lon"])
        poi_longitude.append(longitude)
        france = (data[0]["display_name"]).find("France") > 0
        poi_France.append(france)
        if not france:
            raise (FRANCE())
    except FRANCE:
        print("le Point d'interêt n'est pas en France !")
    except OSError as err:
        print("OS error:", err)
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    params_meteo = {}
    params_meteo["latitude"] = latitude
    params_meteo["longitude"] = longitude
    params_meteo["daily"] = (
        "weather_code,apparent_temperature_max,apparent_temperature_min,precipitation_sum"
    )
    params_meteo["current"] = "weather_code"
    params_meteo["timezone"] = "Europe/Berlin"
    url_meteo = "https://api.open-meteo.com/v1/forecast"
    weather = requests.get(url_meteo, params=params_meteo)
    my_weather = weather.json()["daily"]
    my_weather["poi"] = poi
    df_meteo = pd.DataFrame(my_weather)
    poi_weather.append(df_meteo)
    poi_nice.append(nice_weather(df_meteo))
    print("_________________________________")
# pois_dict est un dictionnaire contenant les points d'intérêt avec leur nom, identifiant (osm) leur latitude et logitude
pois_dict["nom"] = poi_nom
pois_dict["id"] = poi_id
pois_dict["france"] = poi_France
pois_dict["latitude"] = poi_latitude
pois_dict["longitude"] = poi_longitude
pois_dict["weather"] = poi_weather
pois_dict["nice"] = poi_nice

df_pois = pd.DataFrame.from_dict(pois_dict)

df_hotel = pd.read_json("Data/kayak.json", orient="records")


fig = px.scatter_map(
    df_pois,
    lat="latitude",
    lon="longitude",
    color="nice",
    size="nice",
    hover_name="nom",
    hover_data={
        "nom": True,
        "latitude": False,
        "longitude": False,
        "nice": True,
    },
    zoom=6,
    map_style="open-street-map",
    title="indice nice : Niveau de météo sur les 7 jours à venir sur les 35 jours.",
)

fig.update_layout(
    width=1100,
    height=800,
    title_x=0.5,
    title_text="Indice nice sur les 7 prochains jours pour chaque point d'intérêt.",
)
# fig.show()
# Streamlit configuration
st.title("Projet BLOC 1 : KAYAK")


# Create a column with two rows
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.image("assets/kayak_francis_pradel_logo.png", width=200)
with col2:
    st.text(
        "Ci-dessous l'indicateur météo nice des 7 prochains jours pour les 35 sites d'intérêt touristique. "
    )
    st.plotly_chart(fig, use_container_width=True)
    poi = df_pois[["nom"]].iloc[df_pois["nice"].idxmax()].nom
    st.text(f"Site ayant la meilleure météo : {poi}")
    next_pois = df_hotel[df_hotel["ville"] == poi]

    def latitude_extract(ele):
        try:
            latitude = float(ele.split(",")[0])
            return latitude
        except:
            return 0.0

    def longitude_extract(ele):
        try:
            latitude = float(ele.split(",")[1])
            return latitude
        except:
            return 0.0

    next_pois["latitude"] = next_pois["coordinates"].apply(latitude_extract)
    next_pois["longitude"] = next_pois["coordinates"].apply(longitude_extract)
    next_pois["latitude"]
    next_pois["text"] = next_pois["ville"] + " nom : " + next_pois["nom"].astype(str)

    import plotly.graph_objects as go

    # create figure
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scattermap(
            lon=next_pois["longitude"],
            lat=next_pois["latitude"],
            text=next_pois["text"],
            mode="markers+text",
            marker=dict(size=10, symbol="lodging"),
        )
    )
    # Update and show figure
    fig1.update_layout(
        height=400,
        hovermode="closest",
        map=dict(
            bearing=0, center=go.layout.map.Center(lat=45.75, lon=4.85), pitch=0, zoom=5
        ),
        annotations=[
            dict(
                text="Hôtels", showarrow=False, x=0, y=1.085, yref="paper", align="left"
            )
        ],
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.text("liste des hôtels depuis bookiing pour ce site.")
    st.dataframe(next_pois[["nom", "url", "description"]])
