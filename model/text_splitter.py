from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


def get_text_spliter(texts: List[str]) -> Document:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 20,    # 청크 사이즈
        chunk_overlap = 10   # 텍스트 겹치는 부분  
    )
    text_document = text_splitter.create_documents(texts)
    return text_document



if __name__ == "__main__":
    text = "정말 맛있어서 왔었는데 진짜 생각이 계속 나서 성수 일부러 찾아왔어요. 정말 맛있는 파스타 많이 먹어봤지만 여기는 정말 맛있는데다가 가성비까지 좋고 분위기도 미쳐서 너무 생각이 나는 제 원픽 양식집인거 같아요 오늘은 전복리조또와 스파이시 크레비 시켰는데 역시 .. 기대 그 이상입니다 !!! 식전빵에 파스타에 리조또에 모든게 완벽 꼭 와보세요 후회 없습니다 강추 드려요 ~"
    text_document = get_text_spliter(texts=[text])
    print("#"*10 ,'\n', "text_document: ", text_document, '\n', "#"*10)