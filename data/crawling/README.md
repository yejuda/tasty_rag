my_crawler/
    ├── __init__.py
    ├── main.py                # 크롤링을 시작하는 메인 스크립트
    ├── crawler/               # 크롤링 관련 기능을 담는 디렉토리
    │   ├── __init__.py
    │   ├── element_utils.py    # 요소를 찾는 기능
    │   ├── frame_utils.py      # 프레임 전환 기능
    │   └── scraping_logic.py    # 크롤링 로직
    └── data/                  # 크롤링한 데이터를 저장하는 디렉토리
        ├── __init__.py
        └── data_handler.py     # 데이터 처리 및 저장 기능