import os
import pickle
import scipy.sparse as sparse
import pandas as pd
import numpy as np
from django.conf import settings
os.environ['OPENBLAS_NUM_THREADS'] = '1'

def update_user_item_matrix(matrix_file): # 추후 업데이트되는 user item 추가할 것 
    user_item_matrix = pd.read_csv(settings.MEDIA_ROOT + matrix_file,index_col='Unnamed: 0') # user_item_matrix 계속 업데이트될 데이터 
    item_lookup = pd.DataFrame(user_item_matrix['itemID'].drop_duplicates())

    users = list(np.sort(user_item_matrix['userID'].unique()))
    items = list(user_item_matrix['itemID'].unique())
    quantity = list(user_item_matrix['eventStrength'])

    rows = user_item_matrix['userID'].astype('category').cat.codes
    cols = user_item_matrix['itemID'].astype('category').cat.codes
    purchase_sparse = sparse.csr_matrix((quantity, (rows, cols)), shape = (len(users),len(items)))
    return purchase_sparse


def run_user_CF_recommenders(user_ID, purchase_sparse, model):
    recs = model.recommend(int(user_ID), purchase_sparse, N=10)
    # 모델 생성 
    rec_items_list = [ele[0] for ele in recs]
    
    return rec_items_list