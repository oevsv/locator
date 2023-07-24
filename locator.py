#!/usr/bin/python3
# APL2.0, OE3DZW

def location_from_locator(locator: str):
    long_offset = float(180)
    long_range = float(360)

    lat_offset = float(90)
    lat_range = float(180)

    long_res = float(0)
    lat_res = float(0)

    long_factor = float(1)
    lat_factor = float(1)

    letter_ar = dict()
    for i in range(0, 18):
        letter_ar = letter_ar | {chr(ord('A') + i): i}
    letter_ax = dict()
    for i in range(0, 24):
        letter_ax = letter_ax | {chr(ord('A') + i): i}
    number_09 = dict()
    for i in range(0, 10):
        number_09 = number_09 | {chr(ord('0') + i): i}

    if len(locator) % 2 == 1 or len(locator) < 4 or len(locator) > 20:
        # invalid length
        print("Error: length invalid")
        return None
    for charI in range(0, len(locator)):
        if charI < 2:
            # letters A-R
            base = float(18)
            alphabet = letter_ar
        else:
            if int(charI / 2) % 2 == 0:
                # letters A-X
                base = float(24)
                alphabet = letter_ax
            else:
                # digits 0-9
                base = float(10)
                alphabet = number_09
        try:
            val = alphabet[locator[charI]]
        except KeyError:
            print(f"Error: key '{locator[charI]}' invalid")
            return None
        if charI % 2 == 0:
            # longitude
            long_factor = long_factor / base
            long_res += val * long_factor
        else:
            # latitude
            lat_factor = lat_factor / base
            lat_res += val * lat_factor

    # lower left corner of squaroid
    long_west = long_res * long_range - long_offset
    lat_south = lat_res * lat_range - lat_offset

    # upper right corner of squaroid
    long_east = (long_res + long_factor) * long_range - long_offset
    lat_north = (lat_res + lat_factor) * lat_range - lat_offset

    long_centroid = (long_west + long_east) / 2
    lat_centroid = (lat_south + lat_north) / 2

    result = {'long_centroid': long_centroid, 'lat_centroid': lat_centroid,
              'long_west': long_west, 'long_east': long_east,
              'lat_south': lat_south, 'lat_north': lat_north}
    return result


def locator_from_location(longitude: float, latitude: float, length):
    print()

    long_offset = float(180)
    long_range = float(360)
    long_rem = float()

    lat_offset = float(90)
    lat_range = float(180)
    lat_rem = float()

    digit_n = int()
    base = int()
    c = str()
    #  minimum length of locator (e.g. JN68UB)
    length_min = int(3)
    #  maximum length of locator
    length_max = int(10)
    loc = str()

    #  e.g. Lat 48.07823  Long 13.730722 Locator: JN68UB78QS
    #  longitude: -180..+180, east is positive
    #  latitude: -90..+90, north is positive

    # range check parameters
    if (latitude > 90 or latitude < -90 or
            longitude > 180 or longitude < -180):
        print("Error: invalid longitude or latitude")
        return None

    if (length < length_min or length > length_max or
            length % 2 == 1):
        print("Error: invalid length")
        return None

    long_rem = (longitude + long_offset) / long_range
    lat_rem = (latitude + lat_offset) / lat_range

    #  long 180 and -180 are the same place, thus should have the same locator
    if long_rem == 1:
        long_rem = 0

    pairs = int(length / 2)

    for counter in range(0, pairs):

        #  determine base
        if counter == 0:
            #  first pair is A-R
            #  18 zones of longitude of 20° each
            #  18 zones of latitude 10° each
            base = 18
        else:
            if counter % 2 == 0:
                #  odd pair is A-X
                base = 24
            else:
                #  even pair is 0-9
                base = 10

        #  longitude first in pair
        #  longitude is singlar at poles, IARU R1 defines to use the first character
        if latitude == 90 or latitude == -90:
            digit_n = 0
        else:
            digit_n = int(long_rem * base)

        if digit_n > base - 1:
            digit_n = base - 1
        long_rem = (long_rem * base - digit_n)

        if counter % 2 == 0:
            c = chr(ord('A') + digit_n)
        else:
            c = chr(ord('0') + digit_n)

        loc = loc + c
        #  latitude second in pair
        digit_n = int(lat_rem * base)

        if digit_n > base - 1:
            digit_n = base - 1
        lat_rem = (lat_rem * base - digit_n)

        if counter % 2 == 0:
            c = chr(ord('A') + digit_n)
        else:
            c = chr(ord('0') + digit_n)

        loc = loc + c

    return loc


# test locations
# AA00AA00AA
# RR99XX99XX
# BB00AA00AA
# JN18DU

# Some demo code, first find locator

location = 'JN18DU55IX'

print(f"Get location for {location}")

location = location_from_locator("JN18DU55IX")

print(f"centroid: longitude: {location['long_centroid']} latitude {location['lat_centroid']}")
print(f"box: long: {location['long_west']} -> {location['long_east']}")
print(f"box: lat: {location['lat_south']} -> {location['lat_north']}")
print()

# Next find locator for some location

long = 2.29461805555556
lat = 48.858246527777766
print(f"Get locator for longitude {long} and latitude {lat}")
locator = locator_from_location(long, lat, 10)
print(f"locator: {locator}")

