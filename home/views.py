from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from . import CF_recommender
from . import find_similar_item
from . import find_similar_menu
from . import find_recipe
from . import search_listup
import pandas as pd
from django.conf import settings
import pickle
import re
import numpy as np
# from . import find_recipe

# item_name = '해피트루 포스트 바이오틱스'

# 항시 실행되어있어야 하는 코드
df_item = pd.read_csv(settings.MEDIA_ROOT + '/03itemdf.csv', encoding='utf8', index_col=0)
df_recipe = pd.read_csv(settings.MEDIA_ROOT + '/merged_df.csv', encoding='utf8',index_col=0)
df_recipe_url = pd.read_csv(settings.MEDIA_ROOT + '/images_df.csv',encoding='utf8',index_col=0)
df_recipe_with_img = df_recipe.merge(df_recipe_url, how='left', on='요리명')
df_random_user = pd.read_csv(settings.MEDIA_ROOT + '/random_user_data.csv', encoding='utf8', index_col=0)
organs_df = pd.read_csv(settings.MEDIA_ROOT + '/01el_for_organ.csv',encoding='utf8',index_col=0)
# 코사인유사도 item 관련
count_product_category, tfidf_product_effect = find_similar_item.vectorize_item(df_item)
menu_cos_sim = find_similar_menu.cos_sim_dict()


def login_view(request):
    print('login request',request)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        # db에 일치하는 유저 존재 유무 체크
        if user is not None:
            print("success")
            login(request, user) 
            print("logged user",user)
            return redirect("home:index")
        else:
            print("fail")
    else:
        print("get request")
        return render(request,'home/index.html',{})


def logout_view(request):
    logout(request)
    return redirect("home:login")


def signup_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        nickname = request.POST["nickname"]
        disease = request.POST["disease"]
        organ = request.POST["organ"]
        
        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.nickname = nickname
        user.disease = disease
        user.organ = organ
        
        user.save()
        
        # 이후 수정
        # user = User.objects.get(username = username)
        # user.username = newusername
        # user.save()
        
        return redirect("home:login")
    
    return render(request, 'home/signup.html',{})


def index(request):
    print(request.user)
    context = {}        
    return render(request, 'home/index.html', context)
    
    # (1)-1. 협업필터링 for 건강기능식품 ++ 반복되는 코드 처리하기 
    # loaded_model_item = pickle.load(open(settings.MODEL_ROOT + '/CF_recommender_item.sav','rb'))
    # purchase_sparse_item = CF_recommender.update_user_item_matrix('/user_item_matrix.csv')
    # rec_items_list = CF_recommender.run_user_CF_recommenders(logged_user_id, purchase_sparse_item,loaded_model_item)
    # df_items_CF = df_item.loc[df_item['itemID'].isin(rec_items_list)]
    # zipped_df_items_CF = zip(df_items_CF['itemID'],df_items_CF['제품명'],df_items_CF['제조회사'],df_items_CF['heart'])

    # # (1)-2. 협업필터링 for 레시피
    # loaded_model_recipe = pickle.load(open(settings.MODEL_ROOT + '/CF_recommender_recipe.sav','rb'))
    # purchase_sparse_recipe = CF_recommender.update_user_item_matrix('/user_recipe_matrix.csv')
    # rec_recipe_list = CF_recommender.run_user_CF_recommenders(logged_user_id, purchase_sparse_recipe,loaded_model_recipe)
    # df_recipe_CF = df_recipe_with_img.loc[df_recipe_with_img['recipeID'].isin(rec_recipe_list)]
    # zipped_df_recipe_CF = zip(df_recipe_CF['recipeID'],df_recipe_CF['요리명'],df_recipe_CF['관련 질환'],df_recipe_CF['bookmark'],df_recipe_CF['썸네일'])
    
    # (2)-1 최근 북마크한 레시피
    # logged_user_data = df_random_user.loc[df_random_user['userID']==int(logged_user_id)]   
    # recent_recipes = eval(logged_user_data['레시피북마크기록'][int(logged_user_id)])[0:10]
    # df_recent_recipes = df_recipe_with_img.loc[df_recipe_with_img['recipeID'].isin(recent_recipes)]
    # zipped_df_recent_recipe = zip(df_recent_recipes['recipeID'],df_recent_recipes['요리명'],df_recent_recipes['관련 질환'],df_recent_recipes['bookmark'],df_recent_recipes['썸네일'])
    
    # # (2)-1 최근 좋아요누른 건강기능식품
    # recent_items = eval(logged_user_data['건강기능식품하트기록'][int(logged_user_id)])[0:10]
    # df_recent_items = df_item.loc[df_item['itemID'].isin(recent_items)]
    # zipped_df_recent_items = zip(df_recent_items['itemID'],df_recent_items['제품명'],df_recent_items['제조회사'],df_recent_items['heart'])
        
    # context = {
    #     'logged_user_id':logged_user_id,
    #     'zipped_df_items_CF':zipped_df_items_CF,
    #     'zipped_df_recipe_CF':zipped_df_recipe_CF,
    #     'zipped_df_recent_recipe':zipped_df_recent_recipe,
    #     'zipped_df_recent_items':zipped_df_recent_items,
    # }



# item | recipe detail 페이지에서 쓰일 함수
# def detail():
    # count_product_category, tfidf_product_effect = find_similar_item.vectorize_item(df_item)
    # similar_top5_items_index = find_similar_item.cosine_similarity_top5(count_product_category, tfidf_product_effect, item_name, df_item) #, 'similar_top5_items_index' : str(similar_top5_items_index)


def recipe_detail(request, recipeID):
    recipe_info = df_recipe_with_img.loc[df_recipe_with_img['recipeID']==int(recipeID)]
    recipe_steps = zip(re.split('[0-9]\.', recipe_info['레시피'].values[0].replace('\n',''))[1:],eval(recipe_info['조리 이미지'].values[0]))
    
    # 비슷한 재료를 쓰는 레시피 5개 추천
    dish_name = recipe_info['요리명'].values[0]
    similar_menus = find_similar_menu.find_similar_recipe(dish_name, menu_cos_sim) # menu_cos_sim 메뉴명과 함께 df 형태로 불러오기
    # similar_menus = zip(idx, recipes)
    
    context = { # 추후 레시피 csv파일 수정
        'name': recipe_info['요리명'].values[0],
        # 'recipe_id':similar_menus.keys(),
        'igd_ms': recipe_info['재료(계량 포함)'].values[0].replace('\n',''),
        'igd_recipe': recipe_info['재료'].values[0].replace('\n',''),
        'recipe': re.split('[0-9]\.', recipe_info['레시피'].values[0].replace('\n',''))[1:],
        'disease': recipe_info['관련 질환'].values[0],
        'igd_disease': recipe_info['질환별 추천 식재료'].values[0],
        'bookmark': recipe_info['bookmark'].values[0],
        # 'img_recipe': eval(recipe_info['조리 이미지'].values[0]),
        'thumbnail': recipe_info['썸네일'].values[0],
        'recipe_steps':recipe_steps,
        'similar_menus':similar_menus,
    }
    
    return render(request, 'home/recipe_detail.html',context)

def item_detail(request, itemID):
    item_info = df_item.loc[df_item['itemID']==int(itemID)]
    item_name = item_info['제품명'].values[0]
    organs = eval(item_info['신체기능'].values[0])
    organ = organs[0]
    row = organs_df.loc[organs_df['신체기능/기관']==organ] 
    try:
        qa = eval(row['Q&A'].values[0])
    except:
        qa=[]
    try:
        el = eval(row['개별인정형기능성원료'].values[0])
    except:
        el=[]

    # 유사한 아이템 뽑기
    result_idx_list = find_similar_item.cosine_similarity_top5(count_product_category, tfidf_product_effect, item_name, df_item)
    
    similar_items_df = df_item.loc[result_idx_list]
    zipped_similar_items = zip(similar_items_df['itemID'], similar_items_df['제품명'])
    
    
    context = {
        'name':item_name,
        'mfr':item_info['제조회사'].values[0],
        'like':item_info['heart'].values[0],
        'zipped_similar_items':zipped_similar_items,
        'organs':organs,
        'organ':organ,
        'qa':qa,
        'el':el,
        'effect':item_info['효능'].values[0].replace('\n',''),
        'guide':item_info['복용법'].values[0].replace('\n',''),
        'caution':item_info['주의사항'].values[0].replace('\n',''),   
    }
    
    return render(request, 'home/item_detail.html',context)


def search(request):
    organs_list = list(organs_df['신체기능/기관'])
    disease_list = ['고혈압', '뇌졸중', '당뇨병', '천식', '아토피성 피부염', '간염', '빈혈', '심근경색증', '협심증']
    
    context = {
        'organs_list':organs_list,
        'disease_list':disease_list,
    }
    
    if request.method == 'POST':
        search_keyword = request.POST['search_keyword'] # 유저가 검색한 keyword 저장
        
        df_dis_score = pd.read_csv(settings.MEDIA_ROOT + '/search_disease_recipe_score.csv',index_col="Unnamed: 0")
        df_organ_score = pd.read_csv(settings.MEDIA_ROOT + '/search_organ_item_score.csv',index_col="Unnamed: 0")
        
        zipped_top50_recipe = ""
        zipped_top50_item = ""
        
        try:        
            top50_recipe = search_listup.search_listTop50(df_dis_score,search_keyword) #recipeID, 요리명, bookmark
            zipped_top50_recipe = zip(top50_recipe['recipeID'],top50_recipe['요리명'],top50_recipe['bookmark'])
        except: 
            pass
        
        try:
            top50_item = search_listup.search_listTop50(df_organ_score,search_keyword) #itemID, 제품명, heart
            print(top50_item)
            zipped_top50_item = zip(top50_item['itemID'],top50_item['제품명'],top50_item['heart'])
        except:
            pass
        
        context = {
        'organs_list':organs_list,
        'disease_list':disease_list,
        'search_keyword':search_keyword,
        'zipped_top50_recipe':zipped_top50_recipe,
        'zipped_top50_item':zipped_top50_item,    
        }
    return render(request,'home/search.html',context)


def analyze(request):
    return render(request, 'home/analyze.html', {})


def comments(request):
    return render(request,'home/comments.html', {}) 


# analyze.html에서 모델이 예측한 음식명을 현 파일로 불러오는 함수입니다 
def pass_val(request):
    predicted_food_name=request.GET.get('value','')
    
    print('predicted_food_name : ',predicted_food_name)
    
    return render(request,'home/analyze.html',{}) # 반드시 analyze.html일 필요는 없습니다. 함수 실행하면서 render을 하지 않을 시 발생하는 에러 처리를 위해 해당 html을 렌더링해주었습니다 

