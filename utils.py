import os
import requests
import json
import logging

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
from types import SimpleNamespace
from cachetools import cached, TTLCache
from fastapi.responses import StreamingResponse

load_dotenv()

BASE_URL = os.getenv("POKE_API_BERRY_URL")
ONE_DAY = 60 * 60 * 24

def getAllBerriesStadistics():
    response = requests.get(BASE_URL)
    response = strToObject(response)
    payload = {"offset": 0, "limit": response.count}
    response = requests.get(BASE_URL, params=payload)
    response_obj = strToObject(response)
    berries_name = getBerriesName(response_obj)
    berries_growth_time = getBerriesTime(response.text)
    array = np.array(berries_growth_time)
    min_growth_time = min(berries_growth_time)
    max_growth_time = max(berries_growth_time)
    median_growth_time = median(array)
    variance_growth_time = variance(array)
    mean_growth_time = mean(array)
    frequency_growth_time = frequency(array)

    res = {
        "berries_names": berries_name,
        "min_growth_time": min_growth_time,
        "median_growth_time": median_growth_time,
        "max_growth_time": max_growth_time,
        "variance_growth_time": variance_growth_time,
        "mean_growth_time": mean_growth_time,
        "frequency_growth_time": frequency_growth_time
        }
    return res

@cached(cache=TTLCache(maxsize=1, ttl=ONE_DAY))
def getBerriesTime(data):
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    berries_growth_time = []
    for item in data.results:
        res = requests.get(item.url)
        res = strToObject(res)
        berries_growth_time.append(res.growth_time)
    return berries_growth_time

def strToObject(data):
    data = data.text
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

def getBerriesName(response):
    return [item.name for item in response.results]

def median(array):
    return round(np.median(array),2)

def variance(array):
    return round(np.var(array),2)

def mean(array):
    return round(np.mean(array),2)

def frequency(array):
    unique, counts = np.unique(array, return_counts=True)
    res = dict(zip(unique.tolist(), counts.tolist()))
    return res

def send_image(path):
    def iterfile():  # 
        with open(path, mode="rb") as file_like:  # 
            yield from file_like  # 
    return StreamingResponse(iterfile(), media_type="image/png")

async def generateHistogram():
    try:
        response = requests.get(BASE_URL)
        response = strToObject(response)
        payload = {"offset": 0, "limit": response.count}
        response = requests.get(BASE_URL, params=payload)
        berries_growth_time = getBerriesTime(response.text)
        array = np.array(berries_growth_time)
        plt.figure(figsize=(18,10))
        sns.histplot(data = array)
        plt.xlabel("Time", fontsize=18)
        plt.ylabel("Count", fontsize=18)
        plt.title("Frequency of Growth Time", fontsize=18)
        plt.savefig("./assets/histogram.png")
        return True
    except:
        logging.error("Something was wrong while generating histogram")
        return False