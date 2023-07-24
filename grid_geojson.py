#!/usr/bin/python3
# APL2.0, OE3DZW

# Python util to create geojson of Austrian Locators (6 digits)

from locator import *
import geojson
# noinspection PyUnresolvedReferences
from geojson import Polygon, Feature, FeatureCollection, dump

geojson.geometry.DEFAULT_PRECISION = 15

# create a 6 character locator GRID for Austria
# Boundary, with some margin:
# 46 - 50 Nord
# 8 - 18 East

long_west = 8
long_east = 18
lat_south = 46
lat_north = 50

length = 6

# get locator for boundary

# Point south-west: LJ37AX
sw = locator_from_location(46, 8, length)
rsw = location_from_locator(sw)
print(f"box: long: {rsw['long_west']} -> {rsw['long_east']}")
print(f"box: lat: {rsw['lat_south']} -> {rsw['lat_north']}")
print(f"Point south-west: {sw}")

# Point north-east: LK57AX
ne = locator_from_location(50, 18, length)
rne = location_from_locator(ne)
print(f"box: long: {rne['long_west']} -> {rne['long_east']}")
print(f"box: lat: {rne['lat_south']} -> {rne['lat_north']}")
print(f"Point north-east: {ne}")

cursor = None
features = []
count = 0
offset = 0.000000001
locator = sw
lat = lat_south
while lat < lat_north:
    long = long_west
    locator = locator_from_location(long, lat, length)
    while long < long_east:
        count += 1
        cursor = location_from_locator(locator)
        # print(f"count: {count} locator: {locator}: Long: {cursor['long_centroid']}, Lat: {cursor['lat_centroid']}")
        # x->long y->lat
        # noinspection PyTypeChecker
        polygon = geojson.Polygon([[
            (cursor['long_west'], cursor['lat_south']),
            (cursor['long_east'], cursor['lat_south']),
            (cursor['long_east'], cursor['lat_north']),
            (cursor['long_west'], cursor['lat_north']),
            (cursor['long_west'], cursor['lat_south']),
        ]])
        features.append(Feature(geometry=polygon, properties={"locator": locator}))
        # jump to the next locator
        long = cursor['long_east'] + offset
        lat = cursor['lat_centroid']
        locator = locator_from_location(long, lat, length)
    lat = cursor['lat_north'] + offset

feature_collection = FeatureCollection(features)

with open('locators_austria.geojson', 'w') as f:
    dump(feature_collection, f)

print(f"done, count: {count}")
