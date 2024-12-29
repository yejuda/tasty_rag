from crawling_review import crawling_review
import pandas as pd

#TODO 예약없이 이용대기와 같은 부분 덜어내고 해시태그도 따로 제공하는 기능 추가
def process_data(text: str):
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

if __name__ == "__main__":
    from text import text
    # text = crawling_review("잉꼬 칼국수")
    print(process_data(text))