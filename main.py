from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
import joblib
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
import uuid
import time
import psutil
from fastapi.responses import HTMLResponse
from HTMLProjet6 import accueil

if os.path.exists("/.dockerenv"):
    load_dotenv("docker.env")
else:
    load_dotenv("local.env")

URLBDD = os.getenv("URLBDD")
model_trained = joblib.load("model_trained")
app = FastAPI()
engine = create_engine(URLBDD)

@app.get("/", response_class=HTMLResponse)
def home():
    return accueil()

@app.post("/Predict")
def Predict(SK_ID_CURR):
    dico_metric = {}
    start_latence = time.perf_counter()
    start_1 = time.perf_counter()
    with engine.connect() as conn:
        result = conn.execute(
            text('SELECT * FROM "employes" WHERE "SK_ID_CURR" = :id'),
            {"id": SK_ID_CURR}
        )
        row = result.fetchone()
    df_row = pd.DataFrame([row])
    df_features = pd.DataFrame([row])
    df_features = df_features.drop(columns=['SK_ID_CURR','TARGET'])

    df_row.to_sql(
    "predictions_inputs",
    con=engine,
    if_exists="append",
    index=False
    )
    stop_1 = time.perf_counter()
    diff_1 = stop_1 - start_1
    print(f"Temps engine : {diff_1}")
    dico_metric["Temps engine"] = diff_1
    start_2 = time.perf_counter()
    stop_2 = time.perf_counter()
    diff_2 = stop_2 - start_2
    print(f"Temps DF : {diff_2}")
    dico_metric["Temps DF "] = diff_2
    cpu_avant = psutil.cpu_percent(interval=None)
    start_4 = time.perf_counter()
    y_test_pred = model_trained.predict_proba(df_features)
    stop_4 = time.perf_counter()
    diff_4 = stop_4 - start_4
    print(f"Temps Inférence : {diff_4}")
    dico_metric["Temps Inférence"] = diff_4
    start_3 = time.perf_counter()
    cpu_apres = psutil.cpu_percent(interval=None)
    print(f"Usage CPU : {cpu_apres}%")
    dico_metric["Usage CPU"] = cpu_apres
    for i in y_test_pred:
        output = i
    credit_accept = output[0]*100
    credit_decline = output[1]*100
    df_outputs = {}
    df_outputs["ID"] = SK_ID_CURR
    df_outputs["TARGET"] = df_row["TARGET"][0]
    df_outputs["credit_accept"] = output[0]*100
    df_outputs["credit_decline"] = output[1]*100
    df_outputs = pd.DataFrame([df_outputs])
    
    df_outputs.to_sql(
    "predictions_outputs",
    con=engine,
    if_exists="append",
    index=False
    )
    stop_latence = time.perf_counter()
    latence = stop_latence - start_latence
    stop_3 = time.perf_counter()
    diff_3 = stop_3 - start_3
    print(f"Temps Calcul output : {diff_3}")
    dico_metric["Temps Calcul output"] = diff_3
    print(f"Latence Requête : {latence}")
    dico_metric["Latence Requête"] = latence
    df_metric = pd.DataFrame([dico_metric])

    df_metric.to_sql(
        "Metrics",
        con=engine,
        if_exists="append",
        index=False
    )
    print(f"Crédit Accordé : {output[0]*100:.2f}%, Crédit Refusé : {output[1]*100:.2f}%")

    return f"Crédit Accordé : {credit_accept:.2f}%, Crédit Refusé : {credit_decline:.2f}%", credit_accept, credit_decline