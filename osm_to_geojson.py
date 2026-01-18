
import osmium
import json



# Define extraction queries: key-value pairs and output filenames
EXTRACTION_QUERIES = {
    ("amenity", "fuel"): "fuel_all.geojson",
    ("shop", "*"): "shops_all.geojson",
}

PBF_PATH = "uk-latest.osm.pbf"

print("[INFO] ===============================")
print("[INFO] OSM to GeoJSON Extraction Script")
print("[INFO] ===============================")
print(f"[INFO] Using PBF file: {PBF_PATH}")
print("[INFO] Extraction queries:")
for (key, value), filename in EXTRACTION_QUERIES.items():
    print(f"  - {key}={value} -> {filename}")

class MultiTagHandler(osmium.SimpleHandler):
    def __init__(self, queries):
        super().__init__()
        # queries: dict of (key, value) -> output filename
        self.queries = queries
        self.features = {q: [] for q in queries}
        self.counts = {q: 0 for q in queries}
        self._last_update = 0

    def _print_progress(self):
        # Print in-place progress for each query
        msg = "[PROGRESS] Features extracted: "
        msg += ", ".join([f"{k[0]}={k[1]}: {self.counts[k]}" for k in self.queries])
        print(f"\r{msg}", end="", flush=True)

    def add_feature(self, obj, lat, lon, q):
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
        self.features[q].append(feature)
        self.counts[q] += 1
        # Update progress every 500 features
        total = sum(self.counts.values())
        if total - self._last_update >= 500:
            self._print_progress()
            self._last_update = total

    def node(self, n):
        for (key, value) in self.queries:
            if key in n.tags and n.location.valid():
                if value == "*" or n.tags.get(key) == value:
                    self.add_feature(n, n.location.lat, n.location.lon, (key, value))

    def way(self, w):
        for (key, value) in self.queries:
            if key in w.tags and w.nodes:
                if value == "*" or w.tags.get(key) == value:
                    lats = [n.lat for n in w.nodes if n.location.valid()]
                    lons = [n.lon for n in w.nodes if n.location.valid()]
                    if lats and lons:
                        lat = sum(lats) / len(lats)
                        lon = sum(lons) / len(lons)
                        self.add_feature(w, lat, lon, (key, value))


# Run extraction for all queries
print("[INFO] Starting OSM extraction ...")
handler = MultiTagHandler(EXTRACTION_QUERIES)
try:
    handler.apply_file(PBF_PATH, locations=True, idx="flex_mem")
    # Final progress update
    handler._print_progress()
    print("\n[  ✔  ] Extraction completed successfully.")
except Exception as e:
    print("\n[  ✗  ] Extraction failed:", e)
    exit(1)

# Write each result to its own GeoJSON file
for q, filename in EXTRACTION_QUERIES.items():
    print(f"[INFO] Saving results for {q[0]}={q[1]} ...")
    geojson = {
        "type": "FeatureCollection",
        "features": handler.features[q]
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(geojson, f)
        print(f"[  ✔  ] Saved {handler.counts[q]} features to {filename}")
    except Exception as e:
        print(f"[  ✗  ] Failed to save {filename}: {e}")
