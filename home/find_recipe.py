import pandas as pd
from django.conf import settings

# csv 파일의 이름이 string으로 주어졌을때 csv파일을 열어서 dataframe으로 리턴
def open_df(csv_name):
    df = pd.read_csv(settings.MEDIA_ROOT + csv_name + '.csv', encoding='utf8')
    return df


# 질환명이 str으로 주어졌을때 질환에 맞는 레시피 이름 리스트 리턴
def find_appr_diet(disease_name):
    df = open_df('merged_df')
    appr_diet_df = pd.DataFrame()
    
    for i in range(len(df)):
        curr_row = df.iloc[i]
        related_disease = curr_row['관련 질환']
        if (related_disease == disease_name):
            appr_diet_df.append(curr_row)
    
    return appr_diet_df['요리명']