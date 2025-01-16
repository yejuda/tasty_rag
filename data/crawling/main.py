from typing import Dict, List

from crawler.scraping_logic import search_place


def process_data(text: List[str]) -> List[str]:
    reviews = []
    for t in text:
        if len(t) > 5:
            reviews.append(t)
    return reviews



def get_review_data(place: str) -> Dict[str, str]:
    try:
        texts = search_place(place)
        return {"name": place, "reviews": process_data(texts)}
    except Exception as e:
        print(e)
    return


if __name__ == "__main__":
    # print(get_review_data("잉꼬칼국수"))
    print(get_review_data("동대문엽기떡볶이"))