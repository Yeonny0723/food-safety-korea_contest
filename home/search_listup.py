import pandas as pd
from django.conf import settings 

def search_listTop50(df,keyword):
    input_dise = keyword
    col_name = "Score_{}".format(input_dise)
    df_result = df.sort_values(by=col_name,ascending=False).iloc[:50] # top 50개 추출
    return df_result

# 좋아요순으로 정렬하기
def searchpage_inputDise_by_mark():
    df_result = searchpage_inputDise()
    df_result_by_mark = df_result.sort_values(by='bookmark',ascending=False)
    return df_result_by_mark