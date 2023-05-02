import json
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

from utparking.lib.behavior_model import Runner
from utparking.lib.map_parser import Parser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
pscale = lambda f: np.log(f) / f
bscale = lambda f: np.log(f) / f


def load_garage_data(pth):
    with open(pth, 'rb') as f:
        data = pickle.load(f)
    ret = []
    for run in data:
        _, _, garage_data = run
        ret.append(garage_data)
    return np.array(ret)


def main():
    p = Parser(os.path.join(DATA_DIR, "parsed.json"))
    with open(os.path.join(DATA_DIR, 'sizes.json'), 'r') as f:
        sizes = json.load(f)

    d = []

    for i, building in enumerate(p.buildings):
        d.append({
            'lat': building.lat,
            'lon': building.lon,
            'scale': 1,
            'type': 'Building'
        })

    for i, lots in enumerate(p.parking):
        d.append({
            'lat': lots.lat,
            'lon': lots.lon,
            'scale': 1,
            'type': 'Parking'
        })

    df = pd.DataFrame(d)

    fig = px.scatter_mapbox(lat=[lots.lat], lon=[lots.lon], opacity=0, zoom=15)
    fig.add_scattermapbox(df, )
    # df,
    # lat="lat",
    # lon="lon",
    # size="scale",
    # color="type",
    # size_max=15,
    # zoom=15,
    # labels={"type": "type"},
    # color_discrete_sequence=px.colors.qualitative.D3)

    mapbox_token = os.environ.get("MAPBOX_TOKEN", None)

    fig.update_layout(
        mapbox_style="dark" if mapbox_token is not None else "open-street-map",
        mapbox_accesstoken=mapbox_token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()


if __name__ == "__main__":
    main()
