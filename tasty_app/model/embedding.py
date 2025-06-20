from langchain_huggingface import HuggingFaceEmbeddings
from typing import List


def get_embeddings(model_name: str) -> 'HuggingFaceEmbeddings':
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        # model_kwargs={'device': 'cuda'},
    )
    return embeddings


if __name__ == "__main__":
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    sentences = [
    "안녕하세요",
    "제 이름은 홍길동입니다.",
    "이름이 무엇인가요?",
    "랭체인은 유용합니다.",
    "홍길동 아버지의 이름은 홍상직입니다."
    ]

    hf = get_embeddings("jhgan/ko-sbert-nli")
    
    query = hf.embed_query("홍길동은 아버지를 아버지라 부르지 못하였습니다. 홍길동 아버지의 이름은 무엇입니까?")  # 유저 질문
    answer = hf.embed_query("홍길동의 아버지는 엄했습니다.")  # 가장 이상적인

    query_2 = np.array(query).reshape(1, -1)
    answer_2 = np.array(answer).reshape(1, -1)

    sim = round(cosine_similarity(query_2, answer_2)[0][0], 2)
    
    print("질문: 홍길동은 아버지를 아버지라 부르지 못하였습니다. 홍길동 아버지의 이름은 무엇입니까? \n", "-"*100)
    print(f"홍길동의 아버지는 엄했습니다. \t 문장 유사도: {sim}")

    # 특정 문장과의 유사도 비교
    for sentence in sentences:
        ko_embedding = hf.embed_query(sentence)
        answer_curr_2d = np.array(ko_embedding).reshape(1, -1)
        similarity = round(cosine_similarity(answer_2, answer_curr_2d)[0][0], 2)  # 2차원 배열로 변환
        print(f"{sentence} \t\t\t 문장 유사도: {similarity}")