import os
from typing import TypedDict, List, Tuple, Annotated
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever, BM25Retriever
from langgraph.graph import StateGraph, END

# 상태 정의
class State(TypedDict):
    query: str
    context: List[Document]
    review_summary: str
    keywords: List[str]
    overall_evaluation: str

# 노드 함수 정의
def retrieve(state: State) -> State:
    retrieved_docs = ensemble_retriever.get_relevant_documents(state["query"])
    state["context"] = retrieved_docs
    return state

def summarize(state: State) -> State:
    summary_prompt = ChatPromptTemplate.from_template("다음 리뷰를 요약해주세요: {context}")
    summary = llm(summary_prompt.format(context=state["context"][0].page_content))
    state["review_summary"] = summary.content
    return state

def extract_keywords(state: State) -> State:
    keyword_prompt = ChatPromptTemplate.from_template("다음 리뷰에서 주요 키워드를 3-5개 추출하세요: {context}")
    keywords = llm(keyword_prompt.format(context=state["context"][0].page_content))
    state["keywords"] = keywords.content.split(", ")
    return state

def evaluate(state: State) -> State:
    eval_prompt = ChatPromptTemplate.from_template("이 리뷰가 전체적으로 긍정적인지 부정적인지 평가하고 이유를 설명하세요: {context}")
    evaluation = llm(eval_prompt.format(context=state["context"][0].page_content))
    state["overall_evaluation"] = evaluation.content
    return state

def review_rag(text: str) -> str:
    # 초기 상태 설정
    initial_state = State(query=text, context=[], review_summary="", keywords=[], overall_evaluation="")
    
    # 그래프 실행
    result = graph.invoke(initial_state)
    
    # 결과 포맷팅
    formatted_result = f"""
리뷰 요약: {result['review_summary']}

주요 키워드: {', '.join(result['keywords'])}

총 평가: {result['overall_evaluation']}
    """
    return formatted_result

if __name__ == "__main__":
    api_key = os.getenv('UPSTAGE_API_KEY')

    # 텍스트 분리
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)

    # 임베딩 모델
    embeddings = UpstageEmbeddings(model='embedding-query', api_key=api_key)

    # LLM 설정
    llm = ChatUpstage(model="solar-pro", temperature=0, api_key=api_key)

    # 전역 변수로 설정 (노드 함수에서 사용)
    global ensemble_retriever

    def setup_retriever(text):
        text_document = text_splitter.create_documents([text])
        
        # 벡터 스토어 설정
        db = Chroma.from_documents(documents=text_document, embedding=embeddings)
        
        # BM25 리트리버 설정
        bm25_retriever = BM25Retriever.from_documents(text_document)
        bm25_retriever.k = 5
        
        # Dense 리트리버 설정
        db_retriever = db.as_retriever(search_kwargs={'k': 5})
        
        # 앙상블 리트리버 설정
        return EnsembleRetriever(retrievers=[bm25_retriever, db_retriever], weights=[0.5, 0.5])

    # 그래프 구성
    workflow = StateGraph(State)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("summarize", summarize)
    workflow.add_node("extract_keywords", extract_keywords)
    workflow.add_node("evaluate", evaluate)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "summarize")
    workflow.add_edge("summarize", "extract_keywords")
    workflow.add_edge("extract_keywords", "evaluate")
    workflow.add_edge("evaluate", END)

    graph = workflow.compile()

    # 테스트 실행
    test_text = "정말 맛있어서 왔었는데 진짜 생각이 계속 나서 성수 일부러 찾아왔어요. 정말 맛있는 파스타 많이 먹어봤지만 여기는 정말 맛있는데다가 가성비까지 좋고 분위기도 미쳐서 너무 생각이 나는 제 원픽 양식집인거 같아요 오늘은 전복리조또와 스파이시 크레비 시켰는데 역시 .. 기대 그 이상입니다 !!! 식전빵에 파스타에 리조또에 모든게 완벽 꼭 와보세요 후회 없습니다 강추 드려요 ~"
    
    ensemble_retriever = setup_retriever(test_text)
    result = review_rag(test_text)
    print(result)

