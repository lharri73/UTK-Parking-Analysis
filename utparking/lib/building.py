from utparking.utils import unique


class Building:
    def __init__(self, name, lat, lon, cat, code=None):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.cat = cat
        self.code = code
        # 80: academic and administrative
        # 66: Commuter
        # 67: Non-Commuter
        # 73: Perimeter Commuter
        # 74: Perimeter Non-Commuter

    def __str__(self):
        return f"<Building: '{self.name}' at ({self.lat}, {self.lon})>"

    def __eq__(self, other):
        if isinstance(other, Building):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            raise RuntimeError("Unknown type to compare for equality")

    def to_json(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "cat": self.cat,
            "code": self.code,
        }

    @classmethod
    def parse_buildings(cls, data):
        # academic_buildings = []

        academic_buildings_map = map(lambda f: f["children"]["locations"], data)
        academic_buildings = []
        for b in academic_buildings_map:
            academic_buildings.extend(b)
        buildings = map(
            lambda x: cls(x["name"], x["lat"], x["lng"], x["catId"]), academic_buildings
        )
        building_ignores = [
            "Extension Eastern Region Office",
            "Burlington Building",
            "Middlebrook Building",
            "Richland Tower Transmitter Bldg",
        ]
        # buildings = filter(lambda x: x.name not in building_ignores, buildings)

        return list(buildings)

    def to_request(self):
        return dict(lat=self.lat, lng=self.lon)

    @classmethod
    def parse_parking(cls, data):
        commuter_data = data[66]["children"]["locations"]
        commuter = [
            cls(x["name"], x["lat"], x["lng"], x["catId"]) for x in commuter_data
        ]
        non_commuter_data = data[67]["children"]["locations"]
        non_commuter = [
            cls(x["name"], x["lat"], x["lng"], x["catId"]) for x in non_commuter_data
        ]
        perim_commuter_data = data[73]["children"]["locations"]
        perim_commuter = [
            cls(x["name"], x["lat"], x["lng"], x["catId"]) for x in perim_commuter_data
        ]
        perim_non_commuter_data = data[74]["children"]["locations"]
        perim_non_commuter = [
            cls(x["name"], x["lat"], x["lng"], x["catId"])
            for x in perim_non_commuter_data
        ]

        full = commuter + non_commuter + perim_commuter + perim_non_commuter
        parking = unique(full)
        return parking
