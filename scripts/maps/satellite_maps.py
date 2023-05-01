import os
import plotly.express as px
from utparking.lib.behavior_model import Runner
from utparking.lib.map_parser import Parser
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..","..","data")
pscale = lambda f: np.log(f)/f
bscale = lambda f: np.log(f)/f

def main():
    p = Parser(os.path.join(DATA_DIR, "parsed.json"))
    with open(os.path.join(DATA_DIR, 'sizes.json'), 'r') as f:
        sizes = json.load(f)
    
    # building_array=np.empty((len(p.buildings),4))
    # parking_lots_array=np.empty((len(p.parking),4))
    d = []

    for i, building in enumerate(p.buildings):
        d.append({
            'lat': building.lat,
            'lon': building.lon,
            'scale': 1,
            'type': 'Building'
        })
        # building_array[i,0] = building.lat
        # building_array[i,1] = building.lon
        # building_array[i,2] = 1# pscale(sizes['buildings'][building.name])
        # building_array[i,3] = 0
    
    for i, lots in enumerate(p.parking):
        d.append({
            'lat': lots.lat,
            'lon': lots.lon,
            'scale': 1,
            'type': 'Parking'
        })
        # parking_lots_array[i,0] = lots.lat
        # parking_lots_array[i,1] = lots.lon
        # parking_lots_array[i,2] = 1# pscale(sizes['parking'][lots.name])
        # parking_lots_array[i,3] = 1
    # draw_array = np.vstack((building_array, parking_lots_array))

    df = pd.DataFrame(d)
    # df.set_i
    
    fig = px.scatter_mapbox(
        df, 
        lat="lat", 
        lon="lon", 
        size="scale", 
        color="type", 
        size_max=15, 
        zoom=15, 
        labels={"type": "type"}, 
        color_discrete_sequence=px.colors.qualitative.D3)
    #fig.update_layout(mapbox_style="open-street-map")
    mapbox_token = os.environ.get("MAPBOX_TOKEN", None)
    
    fig.update_layout(
        mapbox_style="dark" if mapbox_token is not None else "open-street-map",
        mapbox_accesstoken=mapbox_token
        # mapbox_layers=[
        #     {
        #         "below": 'traces',
        #         "sourcetype": "raster",
        #         "sourceattribution": "United States Geological Survey",
        #         "source": [
        #             "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
        #         ]
        #     }
        # ]
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    
    
if __name__ == "__main__":
    main()
