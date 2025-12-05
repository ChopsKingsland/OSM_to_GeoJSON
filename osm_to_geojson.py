import osmium
import json

class FuelHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.features = []
        self.count = 0

    def add_feature(self, obj, lat, lon):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "id": obj.id,
                "name": obj.tags.get("name", "")
            }
        }
        self.features.append(feature)
        self.count += 1

    def node(self, n):
        if n.tags.get("amenity") == "fuel" and n.location.valid():
            self.add_feature(n, n.location.lat, n.location.lon)

    def way(self, w):
        if w.tags.get("amenity") == "fuel" and w.nodes:
            lats = [n.lat for n in w.nodes if n.location.valid()]
            lons = [n.lon for n in w.nodes if n.location.valid()]
            if lats and lons:
                lat = sum(lats) / len(lats)
                lon = sum(lons) / len(lons)
                self.add_feature(w, lat, lon)

# Run extraction
handler = FuelHandler()
handler.apply_file("uk-latest.osm.pbf", locations=True, idx="flex_mem")

# Create final GeoJSON FeatureCollection
geojson = {
    "type": "FeatureCollection",
    "features": handler.features
}

with open("fuel_all.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f)

print(f"Extracted {handler.count} fuel stations into fuel_all.geojson")
