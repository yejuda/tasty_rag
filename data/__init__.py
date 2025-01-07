from crawling_review import crawling_review
from data_processing import process_data

def get_review(place: str):
    return process_data(crawling_review(place=place))

if __name__ == "__main__":
    print(get_review("잉꼬칼국수"))
    