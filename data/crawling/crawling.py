from typing import Dict, List

from .crawler.scraping_logic import get_review


def process_data(text: List[str]) -> List[str]:
    reviews = []
    for t in text:
        if len(t) > 10:
            reviews.append(t)
    return reviews



def crawling_review(place: str) -> Dict[str, str]:
    try:
        reviews, address = get_review(place)
        return {"name": place, "address": address, "reviews": process_data(reviews)}
    except Exception as e:
        print(e)
    return


if __name__ == "__main__":
    places = [
        "부엉이산장",
        "카페베베",
        "리얼파스타",
        "청록미나리식당",
        '미성식당찌개',
        '대접육류',
        '구들장왕돌판삼겹살',
        '잉꼬칼국수',
        '아쎄커 유쎄피카페',
        "로디어카페",
        "아띠카페카페"
    ]
    result = []
    for place in places:
        result.append(crawling_review(place))
    print(result)