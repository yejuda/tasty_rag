from typing import Dict, List

from sqlite_base import SessionLocal, init_db
from models import Restaurant, Review


init_db()
db_session = SessionLocal()


def search_restaurant(name: str) -> bool:
    if db_session.query(Restaurant.name == name).first():
        return True
    return False


def add_restaurant(name: str, address: str, reviews: List[str]):
    if not search_restaurant(name):
        res = Restaurant(name=name, address=address)
        db_session.add(res)
        db_session.commit()
        
        res_id = res.id

        for review in reviews:
            db_session.add(Review(restaurant_id=res_id, context=review))
        db_session.commit()


def remove_restaurant(name: str):
    target = db_session.query(Restaurant).filter(Restaurant.name == name).first()
    if target:
        db_session.delete(target)
        db_session.commit()

def get_restaurant_db(name: str) -> Dict[str, List[str]]:
    target = db_session.query(Restaurant).filter(Restaurant.name == name).first()
    if target:
        review_arr = []
        for review in target.reviews:
            review_arr.append(review.context)
        return {"name": target.name, "address": target.address, "reviews": review_arr}
    return {}

def show_restaurant() -> List[Dict[str, str]]:
    lists = db_session.query(Restaurant).all()
    result = []
    for li in lists:
        result.append({
            "name": li.name,
            "address": li.address,
            "reviews": [r.context for r in li.reviews],
        })
    return result


if __name__ == "__main__":
    add_restaurant("의현", "남양주시", ["맛있어요"])
    print(get_restaurant_db("의현"))
    print(show_restaurant())
    remove_restaurant("의현")
    print(show_restaurant())