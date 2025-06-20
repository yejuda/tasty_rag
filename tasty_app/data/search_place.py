from typing import Dict, List
import requests

from assets.api_len import api_length_dict


def search_restaurant(place: str, city: str):   
    i = 1
    data = []
    
    while i <= api_length_dict[city]:
        data.append(get_restaurants_info(city, i))
        i += 1
    return data

def get_restaurants_info(city: str, page_index: int) -> List:
    BASE_URL = "https://openapi.gg.go.kr/GENRESTRT?Type=json"
    response = requests.get(f"{BASE_URL}&SIGUN_NM={city}&pIndex={page_index}")

    if response.status_code != 200:
        return []
    return response.json()['GENRESTRT'][1]["row"]

if __name__ == "__main__":
    data = search_restaurant("잉꼬칼국수", "구리시")
    print(data)
    # import pprint

    # if data:
    #     pprint.pprint(data)