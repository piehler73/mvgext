import requests
import asyncio
from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor
from mvgapi import MvgApi, TransportType

START_TIME = default_timer()


def request(session, i):
    """ 
    Generic function for API-Request 
    :param name: session, i 
    :return: data for processing the requests
    """
    url = "https://jsonplaceholder.typicode.com/photos"
    with session.get(url) as response:
        data = response.text

        if response.status_code != 200:
            print("FAILURE::{0}".format(url))

        elapsed_time = default_timer() - START_TIME
        completed_at = "{:5.2f}s".format(elapsed_time)
        print("{0:<30} {1:>20}".format(i, completed_at))
        return data


async def start_async_process() -> any:
    """ 
    Generic function for API-Request 
    :param name: session, i 
    """

    # Validate Station IDs
    print("validating Stations IDs...\n")
    print("Fürstenried West: ")
    print(MvgApi.valid_station_id("de:09162:1500"), "\n")
    print("Planegg: ")
    print(MvgApi.valid_station_id("de:09184:2600"), "\n")
    print("Laubenweg: ")
    print(MvgApi.valid_station_id("de:09184:2549"), "\n")    

    # Check Fürstenried West and get departures
    print("Checking Fürstenried West... \n")
    station = await MvgApi.station_async('Fürstenried West')
    if station:
        print(station, "\n")
        departures = MvgApi.departures_async(station['id'])
        print(await departures, "\n")
        print("Station ID:")
        print(station['id'], "\n")
        print("Fürstenried West: ")
        print(MvgApi.valid_station_id("de:09162:1500"), "\n")

    # Crosscheck departures with direct call by station id
    print("Crosscheck Departures for Fürstenried West:\n")
    departures = MvgApi.departures_async("de:09162:1500")
    print(await departures, "\n")

    print("Departures for Fürstenried West (with Offset):\n")
    departures = MvgApi.departures_async("de:09162:1500",
                                         5, 15,
                                         transport_types=[TransportType.UBAHN])
    print(await departures, "\n")

    # Check Planegg and get departures
    print("Checking Planegg... \n")
    station = await MvgApi.station_async('Planegg')
    if station:
        print(station, "\n")
        departures = MvgApi.departures_async(station['id'])
        print(await departures, "\n")
        print("Station ID:")
        print(station['id'], "\n")
        print("Planegg: ")
        print(MvgApi.valid_station_id("de:09184:2600"), "\n")

        # Crosscheck departures with direct call by station id
        print("Departures for Planegg (with Offset):\n")
        departures = MvgApi.departures_async("de:09184:2600",
                                                5, 15,
                                                transport_types=[TransportType.SBAHN])
        print(await departures, "\n")

    # Check Laubenweg and get departures
    print("Checking Laubenweg... \n")
    station = await MvgApi.station_async('Laubenweg')
    if station:
        print(station, "\n")
        departures = MvgApi.departures_async(station['id'])
        print(await departures, "\n")
        print("Station ID:")
        print(station['id'], "\n")
        print("Laubenweg: ")
        print(MvgApi.valid_station_id("de:09184:2549"), "\n")
 
    print("Departures for Laubenweg (with Offset):\n")
    departures = MvgApi.departures_async("de:09184:2549", 5, 15)
    print(await departures, "\n")

    print("Departures2 for Laubenweg (with Offset):\n")
    departures = MvgApi.departures2_async("de:09184:2549")
    print(await departures, "\n")

    print("{0:<30} {1:>20}".format("No", "Completed at"))
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    request,
                    *(session, i)
                )
                for i in range(15)
            ]
            for response in await asyncio.gather(*tasks):
                pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
