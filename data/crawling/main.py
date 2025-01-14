from typing import Dict, List

from .crawler.direct_search import get_restaurant_directly
from .crawler.scraping_logic import get_restaurant_address


def process_data(text: str) -> List[str]:
    reviews = []
    tmp = []
    texts = list(text.split())
    is_review = False
    for t in texts:
        if is_review:
            tmp.append(t)
        if t == "팔로우":
            is_review = True
            tmp = []
        elif t == "개의":
            is_review = False
            reviews.append(" ".join(tmp))
    return reviews


#TODO 프랜차이즈와 같이 이름이 동일한 검색결과가 많이 나올경우 하나를 특정해서 알려주는 함수 필요
def get_review_ensemble(place: str) -> Dict[str, str]:
    try:
        texts = get_restaurant_directly(place)
        return {"name": place, "address": "구리", "reviews": process_data(texts)}
    except Exception as e:
        print(e)
    try:
        texts = get_restaurant_address(place)
        return {"name": place, "address": "구리", "reviews": process_data(texts)}
    except Exception as e:
        print(e)
    return
    


if __name__ == "__main__":
    print(get_review_ensemble("잉꼬칼국수"))
    # print(get_restaurant_crawling("동대문엽기떡볶이"))