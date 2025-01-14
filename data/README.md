## data 전송 방법

1. 장소에 대한 정보를 받는다
   input = {"place": "잉꼬칼국수", "location": "구리"}
2. input을 토대로 구리 음식점 API에 접근하여 음식점을 찾는다.
   만약 없으면 Error : Not Found
3. 음식점 주소를 받아와서 이를 토대로 음식점을 검색한다.
4. 음식점 리뷰 데이터를 리턴한다.

### 구조 설명

assets
api_len.py - api 데이터의 페이지 길이를 적어둔 값
