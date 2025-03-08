from data.main import get_review
from model import review_rag


place = input()
review_dict = get_review(place)
result = review_rag(review_dict['reviews'])
print(result)
