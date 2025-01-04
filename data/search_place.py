import requests

def get_restarnts_info(city: str, page_index: int):
    BASE_URL = "https://openapi.gg.go.kr/GENRESTRT?Type=json"
    response = requests.get(f"{BASE_URL}&SIGUN_NM={city}&pIndex={page_index}")

    if response.status_code != 200:
        return None

    return response.json()

if __name__ == "__main__":
    data = get_restarnts_info("구리시", 1)
    import pprint

    if data:
        pprint.pprint(data)