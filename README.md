Tool to parse Open Street Maps data sets looking for tags, and then create a GeoJSON layer for use with tools such as QGIS

Requires Osmium - https://osmcode.org/osmium-tool/
OSM Tag list - https://wiki.openstreetmap.org/wiki/Tags#Finding_your_tag

- Place file alongside osm.pbf
- Update `"uk-latest.osm.pbf"` (line 40)  with your file name
- Update `tags.get("amenity") == "fuel"` (lines 26 & 30) with required OSM tag
- Update `"fuel_all.geojson"` (line 48) with output file name
- Run from command line as `osm_to_geojson.py`

Be aware, may take a large amount of time for bigger data sets
