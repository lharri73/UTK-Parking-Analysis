import os
import plotly.express as px
from utparking.lib.behavior_model import Runner
from utparking.lib.map_parser import Parser
import numpy as np
import matplotlib.pyplot as plt
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..","..","data")

def main():
    p = Parser(os.path.join(DATA_DIR, "parsed.json"))
    with open(os.path.join(DATA_DIR, 'sizes.json'), 'r') as f:
        sizes = json.load(f)
    
    building_array=np.empty((len(p.buildings),4))
    parking_lots_array=np.empty((len(p.parking),4))
    
    for i, building in enumerate(p.buildings):
        building_array[i,0] = building.lat
        building_array[i,1] = building.lon
        building_array[i,2] = sizes['buildings'][building.name]
        building_array[i,3] = 0
    print("building_array")
    print(building_array)
    
    for i, lots in enumerate(p.parking):
        parking_lots_array[i,0] = lots.lat
        parking_lots_array[i,1] = lots.lon
        parking_lots_array[i,2] = sizes['parking'][lots.name]
        parking_lots_array[i,3] = 1
    print("parking_lots_arr!ay")
    print(parking_lots_array) 
    draw_array = np.vstack((building_array, parking_lots_array))
    
    fig = px.scatter_mapbox(lat=draw_array[:,0], lon=draw_array[:,1], size=draw_array[:,2], color=draw_array[:,3], size_max=25, zoom=10, color_continuous_scale=px.colors.sequential.Jet)
    # fig.add_scattermapbox(lat=parking_lots_array[:,0],lon=parking_lots_array[:,1], size=parking_lots_array[:,2])
    #fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    
    
if __name__ == "__main__":
    main()