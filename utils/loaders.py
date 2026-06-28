import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv("ACB_TOKEN_NEW.env")

@st.cache_data
def load_standings():

    try:

        api_key = os.getenv("ACB_TOKEN_KEY_NEW")

        if api_key is None:
            raise ValueError("No se encontró la variable de entorno 'ACB_TOKEN_KEY_NEW'.")

        headers = {
            "X-Apikey": api_key
        }

        url = (
            "https://api2.acb.com/api/seasondata/"
            "Competition/standings?competitionId=1&editionId=90&roundId=5917"
        )


        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        data = r.json()

        df_teams = pd.DataFrame(data["teams"])
        df_standings = pd.DataFrame(data["standings"])

        df = df_standings.merge(
            df_teams,
            left_on="teamId",
            right_on="id",
            how="left"
        )

        return df, "api"

    except Exception:

        df = pd.read_csv("data/backup/standings.csv")

        return df, "csv"
    

@st.cache_data
def load_matches():

    try:

        api_key = os.getenv("ACB_TOKEN_KEY_NEW")

        if api_key is None:
            raise ValueError("No se encontró la variable de entorno 'ACB_TOKEN_KEY_NEW'.")

        headers = {
            "X-Apikey": api_key
        }

        url = (
            "https://api2.acb.com/api/seasondata/"
            "Competition/matches?competitionId=1&isRoundSelected=false"
        )

        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        data = r.json()

        df_teams = pd.DataFrame(data["teams"])
        df_matches = pd.DataFrame(data["matches"])

        # Equipo local
        home = (
            df_teams[
                ["id", "fullName", "abbreviatedName", "logo"]
            ]
            .rename(
                columns={
                    "id": "homeTeamId",
                    "fullName": "Local",
                    "abbreviatedName": "Local Abrev",
                    "logo": "Logo Local"
                }
            )
        )

        # Equipo visitante
        away = (
            df_teams[
                ["id", "fullName", "abbreviatedName", "logo"]
            ]
            .rename(
                columns={
                    "id": "awayTeamId",
                    "fullName": "Visitante",
                    "abbreviatedName": "Visitante Abrev",
                    "logo": "Logo Visitante"
                }
            )
        )

        df = (
            df_matches
            .merge(home, on="homeTeamId")
            .merge(away, on="awayTeamId")
        )

        return df, "api"

    except Exception:

        df = pd.read_csv("data/backup/matches.csv")

        return df, "csv"