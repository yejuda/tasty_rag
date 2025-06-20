from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_core.documents import Document
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from kiwipiepy import Kiwi
from typing import List
from dotenv import load_dotenv

# prompt
from etc.prompt import rag_prompt 

load_dotenv()


class LLMModel:
    # 한번만 호출하면 좋은거, 전부 다 쓸 수 있는거
    def __init__(self, embedding_model_name="jhgan/ko-sroberta-multitask", llm_model_name="azure99/blossom-v6"):
        """초기화 메서드: 모델과 설정을 한번만 초기화"""
        # 임베딩 모델 설정
        self.embeddings = self._get_embeddings(embedding_model_name)

        # LLM 설정
        self.llm = Ollama(model=llm_model_name)

        # text splitter 설정
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 20,     # 청크 사이즈
            chunk_overlap = 10   # 텍스트 겹치는 부분  
        )

        # Kiwi 토크나이저 초기화
        self.kiwi = Kiwi()

    # 임베딩 생성
    def _get_embeddings(self, model_name: str) -> HuggingFaceEmbeddings:
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            # model_kwargs={'device': 'cuda'},
        )
        return embeddings

    # Kiwi 토크나이즈
    def _kiwi_toknize(self, text: str) -> List[str]:
        return [token.form for token in self.kiwi.tokenize(text)]


    # BM25 리트리버 생성
    def _get_bm25_retriever(self, text_document: List[Document], k: int) -> BM25Retriever:
        bm25_retriever = BM25Retriever.from_documents(
            documents=text_document,
            process_func=self._kiwi_toknize,
        )
        bm25_retriever.k = k
        return bm25_retriever

    # Chroma DB 리트리버 생성
    def _get_db_retriever(self, text_document: List[Document], k: int) -> Chroma:
        db = Chroma.from_documents(
            documents=text_document,
            embedding=self.embeddings
        )
        db_retriever = db.as_retriever(search_kwargs={'k':k})
        return db_retriever

    # 앙상블 리트리버 생성
    def _get_ensemble_retriever(self, text_document: List[Document], k: int = 20) -> EnsembleRetriever:  # k는 반환할 문서 수
        bm25 = self._get_bm25_retriever(text_document, k)
        db = self._get_db_retriever(text_document, k)
        ensemble_retriever = EnsembleRetriever(      # 리트리버 앙상블 
            retrievers = [bm25, db], 
            weights = [0.5, 0.5]
        )
        return ensemble_retriever
    
    # 텍스트 분할
    def _get_text_splitter(self, texts: List[str]) -> List[Document]:
        text_document = self.text_splitter.create_documents(texts)
        return text_document


    # RAG 체인 설정
    def review_rag(self, texts: List[str]) -> str:  # 여러 개의 리뷰가 리스트에 담겨져 있음
        """리뷰를 분석하고 결과를 반환"""

        # 텍스트 분할 리트리버 생성
        text_document = self._get_text_splitter(texts)
        ensemble_retriever = self._get_ensemble_retriever(text_document)
        
        # RAG 체인 구성
        rag_chain = (
            {"context": ensemble_retriever, "question": RunnablePassthrough()}  # 질문과 문맥 전달
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )
        
        # 질문 실행
        result = rag_chain.invoke("이 리뷰 분석해서 한국어로 이야기해줘. 리뷰를 보고 해당 식당을 갈지 말지 결정할거야.")
        return result

    def main(self, texts: List[str]) -> str:
        """메인 실행 메서드"""
        return self.review_rag(texts)
        


if __name__ == "__main__":
    # 모델 인스턴스 생성
    model = LLMModel()

    sample_reviews = [
        "음식이 너무 맛있어요! 서비스도 좋아요! 입안에서 음식이 춤을 춰요.",
        "위생이 별로였어요. 실망이에요ㅠㅠ",
        "가격대비 괜찮은 곳이에요!"
    ]

    result = model.main(sample_reviews)
    print(result)
