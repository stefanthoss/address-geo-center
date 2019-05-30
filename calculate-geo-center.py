import sys
import time

import geopy
import pandas as pd

DEFAULT_TIMEOUT = 20  # Default timeout when contacting OpenStreetMap in seconds
WAIT_BETWEEN_REQUESTS = 1.2  # Wait time between OpenStreetMap requests in seconds


def get_coordinates(geolocator, address):
    try:
        location = geolocator.geocode(address, timeout=DEFAULT_TIMEOUT)
        return location.latitude, location.longitude
    except geopy.exc.GeocoderTimedOut as e:
        sys.exit(
            f"Error, the address {address} couldn't be converted to coordinates because of {e.msg}."
        )


def calc_weighted_center(weighted_df):
    return (
        (weighted_df["lat"] * weighted_df["weight"]).sum() / weighted_df["weight"].sum(),
        (weighted_df["lng"] * weighted_df["weight"]).sum() / weighted_df["weight"].sum(),
    )


def main():
    geolocator = geopy.Nominatim(user_agent="weighted-geo-center")

    data = pd.DataFrame(columns=["address", "weight"])

    count = int(input("How many addresses do you want to enter? "))

    for i in range(0, count):
        data.at[i, "address"] = input(f"Enter address #{i + 1}: ")
        data.at[i, "weight"] = float(input(f"Enter weight for address #{i + 1}: "))

    print("\nData Input:\n", data)

    for i, row in data.iterrows():
        data.at[i, "lat"], data.at[i, "lng"] = get_coordinates(geolocator, row["address"])
        time.sleep(WAIT_BETWEEN_REQUESTS)

    print("\nData w/ Geo Coordinates:\n", data)

    geo_center = calc_weighted_center(data)

    print("")
    print(f"The weighted geographic center is: {geo_center}")
    print(f"Open in Google Maps: http://www.google.com/maps/place/{geo_center[0]},{geo_center[1]}")


main()
