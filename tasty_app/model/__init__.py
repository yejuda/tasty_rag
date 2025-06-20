from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

from .embedding import get_embeddings
from .prompt import rag_prompt 
from .text_splitter import get_text_spliter
from .retriever import get_ensemble_retriever

from typing import List
from dotenv import load_dotenv
load_dotenv()


def review_rag(texts: List[str]):  # 여러 개의 리뷰가 리스트에 담겨져 있음
    ensemble_retriever = get_ensemble_retriever(get_text_spliter(texts), get_embeddings(model_name="jhgan/ko-sroberta-multitask"))

    # Ollama LLM 설정
    llm = Ollama(model="azure99/blossom-v6")
    
    # RAG 체인 구성
    rag_chain = ({"context": ensemble_retriever, "question": RunnablePassthrough()}  # 질문과 문맥 전달
                 | rag_prompt
                 | llm
                 | StrOutputParser()
                 )
    
    result = rag_chain.invoke("이 리뷰 분석해서 한국어로 이야기해줘. 리뷰를 보고 해당 식당을 갈지 말지 결정할거야.")

    return result
    

if __name__ == "__main__":
    text = "정말 맛있어서 왔었는데 진짜 생각이 계속 나서 성수 일부러 찾아왔어요. 정말 맛있는 파스타 많이 먹어봤지만 여기는 정말 맛있는데다가 가성비까지 좋고 분위기도 미쳐서 너무 생각이 나는 제 원픽 양식집인거 같아요 오늘은 전복리조또와 스파이시 크레비 시켰는데 역시 .. 기대 그 이상입니다 !!! 식전빵에 파스타에 리조또에 모든게 완벽 꼭 와보세요 후회 없습니다 강추 드려요 ~"
    print(review_rag([text]))