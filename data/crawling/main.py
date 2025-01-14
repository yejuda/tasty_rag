from typing import Dict, List

from crawler.scraping_logic import search_place


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



def get_review_data(place: str) -> Dict[str, str]:
    try:
        texts = search_place(place)
        return {"name": place, "reviews": process_data(texts)}
    except Exception as e:
        print(e)
    return
    


if __name__ == "__main__":
    print(get_review_data("잉꼬칼국수"))
    print(get_review_data("동대문엽기떡볶이"))