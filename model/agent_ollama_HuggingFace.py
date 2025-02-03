'''
사용자의 입력을 받아 에이전트가 리뷰를 분석
그 결과를 바탕으로 식당 방문 여부에 대한 추천을 제공
LangGraph를 통해 이 과정이 체계적으로 관리됨.
필요에 따라 워크플로우를 확장하거나 수정할 수 있음.
'''
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever, BM25Retriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub  # 내부적으로 API 호출을 처리함.
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from typing import List, TypedDict
from langchain.agents import AgentExecutor, Tool
from langchain.agents.openai_functions_agent.base import create_openai_functions_agent
from langgraph.graph import StateGraph, END


def review_rag(text):

    # 텍스트 분리
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,    # 청크 사이즈
        chunk_overlap = 20   # 텍스트 겹치는 부분  
    )

    text_document = text_splitter.create_documents([text])
    print("#"*10 ,'\n', "text_document: ", text_document, '\n', "#"*10)
    
    # 임베딩 모델
    embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")

    # 분리된 텍스트 임베딩 및 벡터 스토어에 저장
    db = Chroma.from_documents(
        documents=text_document, 
        embedding=embeddings
    )

    # 리트리버 설정 
    bm25_retriever = BM25Retriever.from_documents(text_document)    # 리트리버 검색기 1 - BM25
    bm25_retriever.k = 3
    db_retriever = db.as_retriever(search_kwargs={'k':3})           # 리트리버 검색기 2 - Dense Retriever   # k는 반환할 문서 수
    ensemble_retriever = EnsembleRetriever(                         # 리트리버 앙상블 
        retrievers = [bm25_retriever, db_retriever], weights = [0.5, 0.5]
    )
    
    # TODO 프롬프트 설정 -> 예시 추가하기!
    rag_prompt = ChatPromptTemplate.from_template(
        """
        당신은 식당 리뷰 분석 전문가 AI입니다.  
        아래 리뷰 데이터를 분석하여 다음 질문에 답하세요:

        1. 리뷰 요약: 리뷰 내용을 2-3문장으로 간결하게 요약합니다. 
        2. 주요 키워드: 리뷰에서 핵심 키워드를 3-5개 추출하세요.  
        3. 총 평가: 리뷰가 전체적으로 긍정적인지 부정적인지 5점 만점으로 평가하고 이유를 설명합니다.
        4. 추천 여부: 이 식당을 추천할지 여부를 결정하고 그 이유를 설명합니다.

        리뷰 데이터: {context}  
        질문: {question}

        답변 형식:  
        - 리뷰 요약: 
        - 주요 키워드: 
        - 총 평가: (/5)   
        - 추천 여부:
        """
    )

    # TODO 더 작은 모델로 바꿔서 진행하기
    # LLM 설정 (한국어에 특화)
    model_name = "beomi/KoAlpaca-Polyglot-5.8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    
    # RAG 체인 구성
    rag_chain = ({"context": ensemble_retriever, "question": RunnablePassthrough()}  # 질문과 문맥 전달
                 | rag_prompt
                 | llm
                 | StrOutputParser()
                 )
    
    # 도구 정의 -> 리뷰 분석 기능 제공
    tools = [
        Tool(
            name="Analyze_Review",  # 도구명
            func=lambda q: rag_chain.invoke(q),
            description="한국어 식당 리뷰를 분석하는 도구입니다."
            
        )
    ]
    
    # 에이전트 프롬프트 템플릿
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 한국어 식당 리뷰 분석 전문 AI 어시스턴트입니다. 제공된 도구를 사용하여 리뷰를 분석하고 추천을 제공하세요."),
        ("human", "{input}"),
        ("human", '이전 대화:\n{chat_history}'),
        ("human", "Human: {input}"),
        ("ai", "AI: 단계별로 접근해 보겠습니다."),
        ("human", "작업 메모: {agent_scratchpad}")
    ])
    
    # 에이전트 설정
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # LangGraph 상태 정의
    class AgentState(TypedDict):
        input: str                # 입력
        chat_history: List[str]   # 기록
        output: str               # 출력
        agent_scratchpad: str     # 에이전트 스크래치패드
        
    # LangGraph 노드 정의 -> 에이전트 작업 수행
    def agent_node(state):
        result = agent_executor.invoke(state)
        return {"output": result["output"],
                "chat_history": state["chat_history"] + [result["output"]],
                "agent_scratchpad": result.get("intermediate_steps", "")}
        
        
    # LangGraph 워크플로우 정의
    workflow = StateGraph(AgentState)         # 워크플로우 구성
    workflow.add_node("agent", agent_node)    # 노드 추가
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)           # 종료점
    
    
    # 컴파일 및 실행 -> 컴파일된 워크플로우를 실행하여 리뷰 분석 결과를 얻음
    app = workflow.compile()
    result = app.invoke({
        "input": "이 리뷰 분석해줘, 리뷰를 보고 해당 식당을 갈지 말지 결정할거야.", 
        "chat_history": [],
        "agent_scratchpad": ""
        })
    
    return result["output"]
    

if __name__ == "__main__":
    
    text = "정말 맛있어서 왔었는데 진짜 생각이 계속 나서 성수 일부러 찾아왔어요. 정말 맛있는 파스타 많이 먹어봤지만 여기는 정말 맛있는데다가 가성비까지 좋고 분위기도 미쳐서 너무 생각이 나는 제 원픽 양식집인거 같아요 오늘은 전복리조또와 스파이시 크레비 시켰는데 역시 .. 기대 그 이상입니다 !!! 식전빵에 파스타에 리조또에 모든게 완벽 꼭 와보세요 후회 없습니다 강추 드려요 ~"
    
    # 함수 호출
    print(review_rag(text))




### 올라마 ###

'''
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.agents import create_openai_tools_agent
from langchain.schema import ChatGeneration, AIMessage

from typing import List, TypedDict
from langchain.agents import AgentExecutor, Tool
from langgraph.graph import StateGraph, END

from langchain.schema import ChatGeneration, AIMessage

from langchain.agents import Agent, AgentExecutor, Tool
from langchain.agents import create_react_agent


def review_rag(text):
    # 텍스트 분리
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,    # 청크 사이즈
        chunk_overlap = 20   # 텍스트 겹치는 부분  
    )

    text_document = text_splitter.create_documents([text])
    print("#"*10 ,'\n', "text_document: ", text_document, '\n', "#"*10)
    
    # 임베딩 모델
    embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")

    # 분리된 텍스트 임베딩 및 벡터 스토어에 저장
    db = Chroma.from_documents(
        documents=text_document, 
        embedding=embeddings
    )

    # 리트리버 설정 
    bm25_retriever = BM25Retriever.from_documents(text_document)    # 리트리버 검색기 1 - BM25
    bm25_retriever.k = 3
    db_retriever = db.as_retriever(search_kwargs={'k':3})           # 리트리버 검색기 2 - Dense Retriever   # k는 반환할 문서 수
    ensemble_retriever = EnsembleRetriever(                         # 리트리버 앙상블 
        retrievers = [bm25_retriever, db_retriever], weights = [0.5, 0.5]
    )
    
    # TODO 프롬프트 설정 -> 예시 추가하기!
    rag_prompt = ChatPromptTemplate.from_template(
        """
        당신은 식당 리뷰 분석 전문가 AI입니다.  
        아래 리뷰 데이터를 분석하여 다음 질문에 답하세요:

        1. 리뷰 요약: 리뷰 내용을 2-3문장으로 간결하게 요약합니다. 
        2. 주요 키워드: 리뷰에서 핵심 키워드를 3-5개 추출하세요.  
        3. 총 평가: 리뷰가 전체적으로 긍정적인지 부정적인지 5점 만점으로 평가하고 이유를 설명합니다.
        4. 추천 여부: 이 식당을 추천할지 여부를 결정하고 그 이유를 설명합니다.

        리뷰 데이터: {context}  
        질문: {question}

        답변 형식:  
        - 리뷰 요약: 
        - 주요 키워드: 
        - 총 평가: (/5)   
        - 추천 여부:
        """
    )
#################
    class OllamaChatModel(Ollama):
        def generate(self, prompts, **kwargs):
            results = super().generate(prompts, **kwargs)
            return [ChatGeneration(message=AIMessage(content=result.generations[0].text)) 
                    for result in results]

        def invoke(self, input, config=None, **kwargs):
            result = super().invoke(input, config, **kwargs)
            return AIMessage(content=result)

    # Ollama LLM 설정
    llm = OllamaChatModel(model="orca-mini")
    
    # RAG 체인 구성
    rag_chain = ({"context": ensemble_retriever, "question": RunnablePassthrough()}  # 질문과 문맥 전달
                 | rag_prompt
                 | llm
                 | StrOutputParser()
                 )
    
    # 도구 정의 -> 리뷰 분석 기능 제공
    tools = [
        Tool(
            name="Analyze_Review",  # 도구명
            func=lambda q: rag_chain.invoke(q),
            description="한국어 식당 리뷰를 분석하는 도구입니다."
            
        )
    ]
    
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 한국어 식당 리뷰 분석 전문 AI 어시스턴트입니다. 다음 도구들을 사용할 수 있습니다: {tool_names}\n\n{tools}\n\n제공된 도구를 사용하여 리뷰를 분석하고 추천을 제공하세요."),
        ("human", "{input}"),
        ("human", "이전 대화:\n{chat_history}"),
        ("human", "Human: {input}"),
        ("ai", "AI: 단계별로 접근해 보겠습니다. 먼저 사용 가능한 도구를 확인하고, 적절한 도구를 선택하여 분석을 진행하겠습니다."),
        ("human", "작업 메모: {agent_scratchpad}")
    ])
        
    
    # 에이전트 설정
    agent = create_react_agent(llm=llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(
                                    agent=agent,
                                    tools=tools,
                                    verbose=True,
                                    handle_parsing_errors=True
                                )

    
    # LangGraph 상태 정의
    class AgentState(TypedDict):
        input: str                # 입력
        chat_history: List[str]   # 기록
        output: str               # 출력
        agent_scratchpad: str     # 에이전트 스크래치패드
        
    # LangGraph 노드 정의 -> 에이전트 작업 수행
    def agent_node(state):
        result = agent_executor.invoke(state)
        return {"output": result["output"],
                "chat_history": state["chat_history"] + [result["output"]],
                "agent_scratchpad": result.get("intermediate_steps", "")}
        
        
    # LangGraph 워크플로우 정의
    workflow = StateGraph(AgentState)         # 워크플로우 구성
    workflow.add_node("agent", agent_node)    # 노드 추가
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)           # 종료점
    
    
    # 컴파일 및 실행 -> 컴파일된 워크플로우를 실행하여 리뷰 분석 결과를 얻음
    app = workflow.compile()
    result = app.invoke({
        "input": "이 리뷰 분석해줘, 리뷰를 보고 해당 식당을 갈지 말지 결정할거야.", 
        "chat_history": [],
        "agent_scratchpad": ""
        })
    
    return result["output"]
    

if __name__ == "__main__":
    
    text = "정말 맛있어서 왔었는데 진짜 생각이 계속 나서 성수 일부러 찾아왔어요. 정말 맛있는 파스타 많이 먹어봤지만 여기는 정말 맛있는데다가 가성비까지 좋고 분위기도 미쳐서 너무 생각이 나는 제 원픽 양식집인거 같아요 오늘은 전복리조또와 스파이시 크레비 시켰는데 역시 .. 기대 그 이상입니다 !!! 식전빵에 파스타에 리조또에 모든게 완벽 꼭 와보세요 후회 없습니다 강추 드려요 ~"
    
    # 함수 호출
    print(review_rag(text))

'''