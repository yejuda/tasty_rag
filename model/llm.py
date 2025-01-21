import os
from langchain_text_splitters import RecursiveCharacterTextSplitter,  CharacterTextSplitter
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever, BM25Retriever


def review_rag(text):
    api_key = os.getenv('UPSTAGE_API_KEY')

    # 텍스트 분리
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 50,    # 청크 사이즈
        chunk_overlap = 10   # 텍스트 겹치는 부분  
    )

    text_document = text_splitter.create_documents([text])
    print("#"*10 ,'\n', "text_document: ", text_document, '\n', "#"*10)
    

    # 임베딩 모델
    embeddings = UpstageEmbeddings(model = 'embedding-query',  api_key=api_key)  # solar-embedding-1-large-passage

    # 분리된 텍스트 임베딩 및 벡터 스토어에 저장
    db = Chroma.from_documents(
        documents=text_document, 
        embedding=embeddings
    )

    #리트리버 검색기 1 
    # retriever = db.as_retriever()
    bm25_retriever = BM25Retriever.from_documents(text_document)
    bm25_retriever.k = 5
    
    # 리트리버 검색기 2 - Dense Retriever
    db_retriever = db.as_retriever(search_kwargs={'k':5})  # k는 반환할 문서 수

    # 리트리버 앙상블
    ensemble_retriever = EnsembleRetriever(
        retrievers = [bm25_retriever, db_retriever], weights = [0.5, 0.5]
    )
    
    #TODO 프롬프트 설정 -> 예시 추가하기!
    rag_prompt = ChatPromptTemplate.from_template(
        """
        당신은 식당 리뷰 분석 전문가 AI입니다.  
        아래 리뷰 데이터를 분석하여 다음 질문에 답하세요:

        1. **리뷰 요약**: 리뷰 내용을 간결하게 요약합니다. 
        2. **주요 키워드**: 리뷰에서 핵심 키워드를 3~5개 추출하세요.  
        3. **총 평가**: 리뷰가 전체적으로 긍정적인지 부정적인지 판단하고 이유를 간략히 설명합니다. 

        리뷰 데이터: {context}  
        질문: {question}

        **답변 형식**:  
        - 리뷰 요약: 
        
        - 주요 키워드: 
        
        - 총 평가:   
        
        """
    )


    # LLM 설정  
    # solar-pro (11/26 출시)
    llm = ChatUpstage(model="solar-pro", temperature=0)  # 같은 질문에 항상 같은 답변을 하도록 설정
     
    # RAG 체인 구성
    rag_chain = ({"context": ensemble_retriever, "question": RunnablePassthrough()}  # 질문과 문맥 전달
                 | rag_prompt
                 | llm
                 | StrOutputParser()
                 )
    
    # 사용자의 질문 전달
    result = rag_chain.invoke("이 리뷰 분석해줘. 리뷰를 보고 해당 식당을 갈지 말지 결정할거야.")
    
    return result
    

if __name__ == "__main__":
    
    text = "정말 맛있어서 왔었는데 진짜 생각이 계속 나서 성수 일부러 찾아왔어요. 정말 맛있는 파스타 많이 먹어봤지만 여기는 정말 맛있는데다가 가성비까지 좋고 분위기도 미쳐서 너무 생각이 나는 제 원픽 양식집인거 같아요 오늘은 전복리조또와 스파이시 크레비 시켰는데 역시 .. 기대 그 이상입니다 !!! 식전빵에 파스타에 리조또에 모든게 완벽 꼭 와보세요 후회 없습니다 강추 드려요 ~"
    
    # 함수 호출
    print(review_rag(text))