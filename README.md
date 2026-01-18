Tool to parse Open Street Maps data sets looking for tags, and then create a GeoJSON layer for use with tools such as QGIS

Requires Osmium - https://osmcode.org/osmium-tool/
OSM Tag list - https://wiki.openstreetmap.org/wiki/Tags#Finding_your_tag

- Place file alongside osm.pbf
- Update `PBF_PATH` (line 13)  with your file path
- Update `EXTRACTION_QUERIES` (starting line 8) with required OSM tags - the key (tuple) is the tag and its value to extract, the value (string) is the file path for that tag. Each filename must be unique
- Run from command line as `osm_to_geojson.py`

Be aware, may take a large amount of time for bigger data sets
