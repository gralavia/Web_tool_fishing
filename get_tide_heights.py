# -*- coding: utf-8 -*-
import requests
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote, quote
from datetime import datetime
import html



def get_tide_heights(time, location):
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-A0021-001?Authorization=yourAutho&limit=100&WeatherElement=,LunarDate,TideRange,Tide,TideHeights"
    params = {
        "time": time,
        "location": location
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        all_locations = data["records"]["TideForecasts"]
        location_index = None
        daily_index = None

        for i, loc in enumerate(all_locations):
            if loc["Location"]["LocationName"] == location:
                location_index = i
                break

        if location_index is not None:
            daily_forecasts = data["records"]["TideForecasts"][location_index]["Location"]["TimePeriods"]["Daily"]

            for i, daily_forecast in enumerate(daily_forecasts):
                if daily_forecast["Date"] == time[:10]:
                    daily_index = i
                    break

            if daily_index is not None:
                time_forecasts = daily_forecasts[daily_index]["Time"]

                if len(time) == 10:
                    tide_heights = time_forecasts[0]["TideHeights"]
                else:
                    provided_time = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
                    closest_time_diff = float("inf")
                    closest_time_index = None

                    for i, time_forecast in enumerate(time_forecasts):
                        forecast_time = datetime.strptime(time_forecast["DateTime"], "%Y-%m-%d %H:%M:%S")
                        time_diff = abs(provided_time - forecast_time).total_seconds()

                        if time_diff < closest_time_diff:
                            closest_time_diff = time_diff
                            closest_time_index = i

                    if closest_time_index is not None:
                        tide_heights = time_forecasts[closest_time_index]["TideHeights"]

                    else:
                        print("No data")
                        exit()

                safe_tide_heights = tide_heights["AboveChartDatum"]


                return safe_tide_heights

            else:
                print("No data")
        else:
            print("No data")
    else:
        print("API failed:", response.status_code)
