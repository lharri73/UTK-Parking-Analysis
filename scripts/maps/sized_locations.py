import json
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
# from plotly.graph_objects.bar.marker import ColorBar

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

    g_data = load_garage_data('results/multirun_closest.pkl')
    g_data = np.mean(g_data, axis=0).T
    print(g_data.shape)

    d = []

    for i, lots in enumerate(p.parking):
        d.append({
            'lat': lots.lat,
            'lon': lots.lon,
            'scale': 1,
            'type': 'Parking',
            'sizes': sizes['parking'][lots.name],
            'rate': g_data[i]
        })

    df = pd.DataFrame(d)

    fig = px.scatter_mapbox(lat=[lots.lat], lon=[lots.lon], opacity=0, zoom=15)
    # cb = ColorBar()
    fig.add_scattermapbox(
        lat=df.lat, 
        lon=df.lon, 
        marker={
            "size": np.log(df.sizes.to_numpy())*5,
            "color": df.rate,
            "colorscale": [[0, 'rgb(255,255,255)'], [1, 'rgb(255,130,0)']],
            "opacity": 1,
            "sizemin": 5,
            "sizemode": 'diameter',
            "colorbar": dict(thickness=20, outlinewidth=0)
            },
        name="Parking Areas",
        showlegend=False
    )
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
