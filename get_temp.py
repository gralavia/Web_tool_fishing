# -*- coding: utf-8 -*-
import requests
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote, quote
from datetime import datetime
import html


def get_temperature(time, city):
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=_yourAutho_&elementName=PoP12h,T,RH"
    params = {
        "time": time,
        "city": city
    }
    response = requests.get(url, params=params)
    temp_list = []

    if response.status_code == 200:
        data = response.json()
        all_locations = data["records"]["locations"][0]["location"]

        location_index = None

        for i, loc in enumerate(all_locations):
            if all_locations[i]["locationName"] == city:
                location_index = i
                break

        if location_index is not None:
            time_period = data["records"]["locations"][0]["location"][location_index]["weatherElement"][0]["time"]

            if len(time) == 10:
                Pop = all_locations[location_index]["weatherElement"][0]["time"][0]["elementValue"][0]["value"]
                T = all_locations[location_index]["weatherElement"][1]["time"][0]["elementValue"][0]["value"]
                RH = all_locations[location_index]["weatherElement"][2]["time"][0]["elementValue"][0]["value"]
                temp_list.append(Pop)
                temp_list.append(T)
                temp_list.append(RH)
                return temp_list

            else:
                provided_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                closest_time_diff = float("inf")
                closest_time_index = None

                for j, tm in enumerate(time_period):
                    forecast_time = datetime.strptime(time_period[j]["startTime"], "%Y-%m-%d %H:%M:%S")
                    time_diff = abs(provided_time - forecast_time).total_seconds()

                    if time_diff < closest_time_diff:
                        closest_time_diff = time_diff
                        closest_time_index = j

                if closest_time_index is not None:
                    Pop = \
                        all_locations[location_index]["weatherElement"][0]["time"][closest_time_index][
                            "elementValue"][0][
                            "value"]
                    T = \
                        all_locations[location_index]["weatherElement"][1]["time"][closest_time_index][
                            "elementValue"][0][
                            "value"]
                    RH = \
                        all_locations[location_index]["weatherElement"][2]["time"][closest_time_index][
                            "elementValue"][0][
                            "value"]
                    temp_list.append(Pop)
                    temp_list.append(T)
                    temp_list.append(RH)
                    return temp_list

                else:
                    print("No data")
                    exit()

