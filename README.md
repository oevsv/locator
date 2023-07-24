# Locator

This utility implements the IARU R1 VHF Locator as defined in the IARU R1 VHF Handbook.


## `location_from_locator(locator: str)`

This function decodes a locator. The locator can have variable length, e.g. JN18DU or JN18DU55IX.

It returns a dictionary with the following keys:
* `long_centroid`: Longitude of centroid
* `lat_centroid`: Latitude of centroid
* `long_west`: Western Longitude of boundary box ("squaroid") of locator
* `long_east`: Eastern Longitude of boundary box ("squaroid") of locator
* `lat_south`: Southern Latitude of boundary box ("squaroid") of locator
* `lat_north`: Northern Laiitude of boundary box ("squaroid") of locator

## `def locator_from_location(longitude: float, latitude: float, length)`

This function encodes locator, thus it returns a string with given length.
The parameters are:
* `longitude`: The longitude from -180 to 180. West is positive.
* `latitude`: The latitude from -90 to 90. North is positive.
* `length`: The length of the locator. Length must an even integer of six or more

The main code of locator.py implements these functions with some demo code.




