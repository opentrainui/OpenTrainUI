from json import loads
from urllib.request import urlopen

PARENT_URL = r'https://otrain.org/api/v1/'


def path_info(start_date: str, end_date: str, origin_num: int, dest_num: int):
    # date format: D/M/Y
    url = PARENT_URL + \
          fr'stats/path-info-full/?' \
              fr'destination={dest_num}' \
              fr'&from_date={start_date}' \
              fr'&origin={origin_num}' \
              fr'&to_date={end_date}'
    with urlopen(url) as request:
        return loads(request.read().decode())
