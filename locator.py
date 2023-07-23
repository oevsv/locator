
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
        print(f"Error: length invalid")
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
        if (charI % 2 == 0):
            # longitude
            long_factor = long_factor / base
            long_res += val * long_factor
        else:
            # latitude
            lat_factor = lat_factor / base
            lat_res += val * lat_factor

    # lower left corner of squaroid
    long_left = long_res * long_range - long_offset
    lat_bottom = lat_res * lat_range - lat_offset

    # upper right corner of squaroid
    long_right = (long_res + long_factor) * long_range - long_offset
    lat_top = (lat_res + lat_factor) * lat_range - lat_offset

    lat_centroid = (long_left + long_right) / 2
    long_centroid = (lat_bottom + lat_top) / 2

    result = {'long_centroid': long_centroid, 'lat_centroid': lat_centroid,
              'long_left': long_left, 'long_right': long_right,
              'lat_bottom': lat_bottom, 'lat_top': lat_top}
    return result

# location_from_locator("AA00AA00AA")
# location_from_locator("RR99XX99XX")
location = location_from_locator("JN18DU")
print(f"centroid: longitude: {location['long_centroid']} latitude {location['lat_centroid']}")
