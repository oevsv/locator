def location_from_locator(locator: str):
    # alphabet_c constant varchar := 'ABCDEFGHIJKLMNOPQRSTUVWX';
    # alphabet_n constant varchar := '0123456789';

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
        return None
    for charI in range(0, len(locator)):
        print(f"{charI} {locator[charI]}")
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
        # print(f"base {base} alphabet {alphabet} charI {charI}")
        try:
            val = alphabet[locator[charI]]
        except KeyError:
            print(f"Error: key '{locator[charI]}' invalid")
            return None
        # print (f" val = {val}")

        if (charI % 2 == 0):
            # longitude
            long_factor = long_factor / base
            long_res += val * long_factor
            print(f"long {long_res} val {val} base {base} factor {long_factor} ")
        else:
            # latitude
            lat_factor = lat_factor / base
            lat_res += val * lat_factor
            print(f"lat {lat_res} val {val} base {base} factor {lat_factor} ")

    # lower left corner of squaroid
    x1 = long_res * long_range - long_offset
    y1 = lat_res * lat_range - lat_offset

    # upper right corner of squaroid
    x2 = (long_res + long_factor) * long_range - long_offset
    y2 = (lat_res + lat_factor) * lat_range - lat_offset

    latitude = (x1 + x2) / 2
    longitude = (x1 + x2) / 2

    print(f"boundary: long {x1} lat {y1} long2 {x2} lat2 {y2}")
    print(f"long {longitude} lat {latitude}")

    filename = 'squaroid.geojson'

    with open(filename, 'a') as out:
        out.write(f"[[[{x1},{y1}],")
        out.write(f"[{x2},{y1}],")
        out.write(f"[{x2},{y2}],")
        out.write(f"[{x1},{y2}],")
        out.write(f"[{x1},{y1}]],")
    #
    # {"coordinates": [[[31, -5],
    #                  [32, -5],
    #                  [32, -4],
    #                  [31, -4],
    #                  [31, -5]]],
    # "type": "Polygon"}
    #
    return None


print("hi")
# location_from_locator("AA00AA00AA")
# location_from_locator("RR99XX99XX")
location_from_locator("JN18DU")
