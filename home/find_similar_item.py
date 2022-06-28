import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings 


def vectorize_item(df_item):
# 문구 dense 작업 진행 // 제품분류는 count로, 효능은 tf-idf로 진행
# 하기 내용은 고정이므로 추가 함수작업 없이 진행
    corpus_product_category = []
    corpus_product_effect = []

    for i in range(len(df_item)):
        doc_temp = ''
        doc_temp = df_item['제품분류'].iloc[i]
        corpus_product_category.append(doc_temp)


    for i in range(len(df_item)):
        doc_temp = ''
        doc_temp = df_item['효능'].iloc[i]
        corpus_product_effect.append(doc_temp)

    count_vectorizer = CountVectorizer()
    tfidf_vectorizer = TfidfVectorizer()
    
    count_product_category = count_vectorizer.fit_transform(corpus_product_category).todense()
    tfidf_product_effect = tfidf_vectorizer.fit_transform(corpus_product_category).todense()
    return count_product_category,tfidf_product_effect

# 코사인 유사도 진행

def cosine_similarity_top5(count_product_category,tfidf_product_effect, item_name,df_item):
    # get item index
    product_name_no = ''
    for i in range(len(df_item)):
        if item_name == df_item['제품명'].iloc[i]:
            product_name_no = i
    
    list_cos_product_category = []
    list_cos_product_category = cosine_similarity(count_product_category[product_name_no], count_product_category)
    
    list_cos_product_effect = []
    list_cos_product_effect = cosine_similarity(tfidf_product_effect[product_name_no], tfidf_product_effect)
    
    # 총점 구하기
    total_product_cos_score = []
    for i in range(len(list_cos_product_category[0])):
        total_score = ((list_cos_product_category[0][i]) + (list_cos_product_effect[0][i])) / 2
        total_product_cos_score.append(total_score)
    
    # 총점 구한 결과로 제품명과 함께 신규 dataframe 구축 // 작업 중 오류가 있어 list -> dict -> dataframe 으로 변환 작업 진행
    list_total_product_cos_score = np.array(total_product_cos_score).T.tolist()
    
    list_product = []
    for i in range(len(df_item)):
        list_product.append(df_item['제품명'].iloc[i])
    dict_temp = {'제품명' : list_product, '코사인 유사도' : list_total_product_cos_score}
    df_cos_score = pd.DataFrame(dict_temp)
    df_cos_score = df_cos_score.sort_values(by='코사인 유사도', ascending=False).reset_index()
    
    # Top 5 도출 // 첫 데이터프레임 위치, 제품명 출력
    items_top5_list = list(df_cos_score['index'][1:6])
    return items_top5_list
