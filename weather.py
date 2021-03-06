
# This code is to predict the weather next week in Heifei(or somewhere else)
# by getting data from Darksky API

import json
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# for local file, download json
def load_json_sample(path):
    with open(path, encoding='utf-8') as json_file:
        return json.load(json_file)
    

# for daily data ,find attributes and extract
def daily_data_of_attributes(json_dict, attributes):
    daily_attributes = {}
    for attr in attributes:
        daily_attributes[attr] = []
    daily_data = json_dict["daily"]["data"]
    try:
        for dict_data in daily_data:
            for attr in attributes:
                daily_attributes[attr].append(dict_data[attr])
    except KeyError:
        print("Key Not Found")
        return {}
    return daily_attributes


# get weather data from API
def request_data():
    # LA 37.8267,-122.4233 , beijing 39.904200, 116.407396 ,Hefei 31.83, 117.25 
    lat = 31.83
    long = 117.25 
    api_key = "62bf94de3c232f30f6f3ee5bb534c2f3"
    url = "https://api.darksky.net/forecast/%s/%s,%s?units=si" % (api_key, lat, long)
    response = requests.get(url)
    return json.loads(response.text)


# extrat data attributes
def get_daily_data(remote=False):
    if remote:
        json_obj = request_data()
    else:
        json_obj = load_json_sample('sample.json')
#    pretty_print_dict_of_list(json_obj)
    attributes = ['temperatureMin', 'temperatureMax', 'humidity','summary']
    daily_data = daily_data_of_attributes(json_obj, attributes)
    return daily_data


# print data if needed
def pretty_print_dict_of_list(d):
    indent = 4
    print("{")
    for k, l in d.items():
        print(indent * " " + k + ": ", end="")
        print(l)
    print("}")


# get fig for next_week_data
def next_week_weather():
    daily_dark_data = get_daily_data(True)
    df_dark = pd.DataFrame(daily_dark_data)
    df_dark_temperature = df_dark[["temperatureMin", "temperatureMax"]]
    df_dark_humidity = df_dark[["humidity"]]

    # Plot data
    plt.style.use('ggplot')
    _, axes = plt.subplots(nrows=2)
    df_dark_temperature.plot(ax=axes[0])
    df_dark_humidity.plot(ax=axes[1])
    #plt.show()
    plt.savefig('weather_nextweek.png')

