# UT Parking Analysis

We seek to answer the question: Can collective systems be used to predict the most likely place to find an empty parking spot on campus?

Along the way, we'll find the answewr to many other statistics like
 - **How many parking areas** do people typically check before finding a parking spot?
 - **How long** do people spend parking?
 - What are the **most used parking areas**?
 - What is the **best policy to follow** when finding parking? Park closest to the building you wish to be at? Go the the largest garage? random?
 - Does UT **have enough parking** to support it's buidling capacity?

## Setup

Run `pip install -e .` in the root of this repository. All data has already been parsed
and is included in its raw form just for transparency. 

## Repository structure

```
📦parking
 ┣ 📂data
 ┃ ┣ 📜BuildingList.csv         # building list with names, codes, and sqr feet from UTK FS
 ┃ ┣ 📜bsizes.json              # raw json response from 25live
 ┃ ┣ 📜map_data.json            # raw map data respons from maps.utk.edu
 ┃ ┣ 📜parsed.json              # building names, codes, and locations. parking lot names & locations
 ┃ ┣ 📜sizes.json               # parking lot space numbers and building occupancy limits
 ┃ ┣ 📜btwn_garages.npy         # distance matrix between garages (driving)
 ┃ ┣ 📜to_buildings.npy         # distance matrix from garages to buildings (walking)
 ┃ ┗ 📜to_garages.npy           # distance matrix from interstate to garages (driving)
 ┣ 📂scripts
 ┃ ┗ 📂data_gen                 # folder of scripts used to parse raw map and building size data
 ┣ 📂utparking                  # algo. code
 ┣ 📜.gitignore
 ┣ 📜README.md              # this file
 ┣ 📜assumptions.md         # list of our assumptions for the project
 ┣ 📜requirements.txt       # python requirements
 ┗ 📜setup.py               # setup script for the package
```

## Copyright
Copyright (C) 2023 Landon Harris, Coby White

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

