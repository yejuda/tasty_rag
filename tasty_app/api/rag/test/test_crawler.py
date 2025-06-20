from utils.crawler import Crawler


if __name__ == "__main__":
    places = [
        '잉꼬칼국수',
        "부엉이산장",
        "카페베베",
        "리얼파스타",
        "청록미나리식당",
        '미성식당찌개',
        '대접육류',
        '구들장왕돌판삼겹살',
        '아쎄커 유쎄피카페',
        "로디어카페",
        "아띠카페카페"
    ]

    crawler = Crawler()
    result = []

    for place in places:
        print(crawler.get_review(place))
