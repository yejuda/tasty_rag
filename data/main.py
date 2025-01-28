from database.db_crud import get_restaurant_db, add_restaurant
from crawling.crawling import crawling_review


def get_review(place: str):
    '''DB에 있으면 리뷰를 그대로 가져오고 아니면 크롤링'''
    place_data = get_restaurant_db(place)
    if not place_data:
        try:
            place_data = crawling_review(place)
            add_restaurant(name=place_data['name'], address=place_data["address"], reviews=place_data["reviews"])
        except Exception as e:
            print(f"리뷰를 가져오는 중 오류 발생: {e}")
    return place_data


if __name__ == "__main__":
    places = [
        "부엉이산장",
        "카페베베",
        "리얼파스타",
    ]
    result = []
    for place in places:
        result.append(get_review(place))
    print(result)