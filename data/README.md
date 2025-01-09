## data 전송 방법

1. 장소에 대한 정보를 받는다(init.py)
   - 만약 DB에 있는 경우
      - DB의 리뷰 데이터를 리턴한다
   - 없는 경우
      - 경기도 음식점 API에 접근하여 상세 주소를 리턴 받는다
      - 주소를 기반으로 크롤링을 진행한다

   input = {"place": "잉꼬칼국수", "location": "구리"}
2. input을 토대로  음식점을 찾는다.
   만약 없으면 Error : Not Found
3. 음식점 주소를 받아와서 이를 토대로 음식점을 검색한다.
4. 음식점 리뷰 데이터를 리턴한다.

```
my_package/
    __init__.py
    crawling/
        __init__.py
        address_search.py # 주소를 이용한 검색으로 크롤링
        direct_search.py  # 직접 검색을 통한 크롤링
    database/
        __init__.py
        db_crud.py  # CRUD 관련 함수
        models.py  # 모델 정의
        sqlite_base.py  # Sql Alchemy 설정
    assets/
        api_len.py
        restaurants.db  # 레스토랑 정보 저장 DB
```