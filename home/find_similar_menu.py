# 재료들의 cosine similarity 사용해서 비슷한 메뉴 top 5 추천
import json
import pandas as pd
# import pandas as pd
from django.conf import settings


# 각 음식의 ingredient-based cosine similarity는 dict형태로 저장되어 있음
def cos_sim_dict():
    with open(settings.MEDIA_ROOT + '/cos_sim.json', encoding='utf8') as f:
        cos_sim = json.load(f)
    return cos_sim


# cos_sim --> 각 음식의 cosine similarity가 들어 있는 dict
# dish_name --> 요리 이름 (str)
def find_similar_recipe(dish_name, cos_sim):
    
    # df = pd.read_csv(settings.MEDIA_ROOT + 'merged_df.csv', encoding='utf8', index_col=0)
    with open(settings.MEDIA_ROOT + '/recipe_idx.json', encoding='utf8') as f:
        recipe_idx = json.load(f)

    idx = []
    
    try:
        similar_recipes = list({k:v for k,v in sorted(cos_sim[dish_name].items(), key=lambda item:item[1], reverse=True)})[1:6]
        
        for similar_recipe in similar_recipes:
            # idx.append(find_recipe_idx(similar_recipe))
            # idx.append(df[df['요리명'] == similar_recipe]['recipeID'])
            idx.append(recipe_idx[similar_recipe])
        
        # similar['idx'] = idx
        # similar['idx'] = idx
        # similar['dish_name'] = similar_recipes
            
    except:
        # similar['idx'] = -1
        # similar['dish_name'] = '😢해당 레시피는 존재하지 않습니다. 다시 확인해주세요.😢'
        similar = ['😢해당 레시피는 존재하지 않습니다. 다시 확인해주세요.😢']
        idx = [-1]

    return zip(idx, similar_recipes)

# 요리명이 str으로 주어졌을때 레시피의 인덱스 찾기
def find_recipe_idx(dish_name):
    df = pd.read_csv(settings.MEDIA_ROOT + 'merged_df.csv', encoding='utf8', index_col=0)

    for i in range(len(df)):
        if (df['요리명'] == dish_name):
            return df['recipeID']
    # 아무 인덱스도 찾지 못했을때 return -1
    return -1