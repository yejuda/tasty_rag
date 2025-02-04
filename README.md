# Tasty RAG: 식당 및 카페 리뷰 분석 시스템
Tasty RAG는 식당 및 카페 리뷰를 자동으로 분석하여 사용자에게 종합적인 정보를 제공하는 시스템입니다.   
여러 리뷰를 일일이 살펴봐야 하는 불편함을 해소하고, 한 번의 검색으로 특정 식당이나 카페에 대한 전반적인 평가를 얻을 수 있습니다.

## 프로젝트 구조
```
tasty_rag/
├── data/                  # 데이터 관련 디렉토리
│   ├── __init__.py
│   ├── main.py            # JSON 형태로 데이터를 저장하고 받는 메인 파일
│   ├── crawling/          # 웹 크롤링 관련 모듈
│   │   ├── __init__.py
│   │   ├── crawling.py    # 크롤링을 시작하는 메인 스크립트
│   │   └── crawler/       # 크롤링 관련 기능을 담는 디렉토리
│   │       ├── __init__.py
│   │       ├── element_utils.py
│   │       ├── frame_utils.py
│   │       └── scraping_logic.py
│   ├── database/          # 데이터베이스 관련 모듈
│   │   ├── __init__.py
│   │   ├── db_crud.py     # CRUD 관련 함수
│   │   ├── models.py      # 모델 정의
│   │   └── sqlite_base.py # SQL Alchemy 설정
│   └── assets/            
│       ├── api_len.py     
│       └── restaurants.db # 레스토랑 정보 저장 DB
├── model/                 # LLM 관련 디렉토리
│   ├── __init__.py        # RAG 시스템 메인 모듈
│   ├── embedding.py       # 임베딩 생성 모듈
│   ├── text_splitter.py   # 텍스트 분할 처리기
│   ├── retriever.py       # 정보 검색 시스템
│   ├── prompt.py          # LLM 프롬프트 템플릿
│   └── ollama_test.py     # Ollama 모델 테스트 스크립트
└── main.py                # 프로그램 실행 스크립트
```

## 주요 기능
1. **데이터 수집 및 관리 (data/)**
    - 웹 크롤링을 통한 리뷰 데이터 수집
    - SQLite 데이터베이스를 이용한 데이터 저장 및 관리
    - 경기도 음식점 API 활용
2. **자연어 처리 및 분석 (model/)**
    - 텍스트 임베딩 생성
    - 텍스트 분할
    - 하이브리드 검색 시스템 (BM25 + 벡터 검색)
    - LLM을 이용한 리뷰 분석 및 요약

## 시스템 동작 과정
1. 사용자로부터 식당 이름 입력 받음
2. 데이터베이스에서 해당 식당 정보 검색
3. 정보가 없을 경우 API 및 웹 크롤링을 통해 데이터 수집
4. 수집된 리뷰 데이터를 LLM 모델에 전달하여 분석
5. 분석 결과 출력 (리뷰 요약, 핵심 키워드, 평점, 추천 여부)