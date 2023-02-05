# import pyrebase
from flask import Flask, request, jsonify, session, Response

import pandas as pd
import numpy as np
from itertools import chain
# from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import CountVectorizer  # 피체 벡터화
from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도

path = ""
path += 'https://raw.githubusercontent.com/SKKUxHCMUT-Team3/food-suggestion-app-backend/main/'

vidata = pd.read_csv(path + 'vidata.csv',sep=',')
kodata = pd.read_csv(path + 'kodata.csv',sep=',')

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyAG6QwyEiDmFV4pWQHQn-1q5J4Y6mlJcEI",
  "authDomain": "lav1ne-sample.firebaseapp.com",
  "projectId": "lav1ne-sample",
  "storageBucket": "lav1ne-sample.appspot.com",
  "messagingSenderId": "374481316324",
  "appId": "1:374481316324:web:169065ccd71cc6db733ff1",
  "measurementId": "G-3DE8YQ5DBG",
  "databaseURL": ""
}


# firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key='secret'

def find_simi_place(df, sorted_ind, place_name, top_n=10):
    
    place_title = df[0:1]
    
    place_index = place_title.index.values
    similar_indexes = sorted_ind[place_index, 1:(top_n)+1]
    similar_indexes = similar_indexes.reshape(-1)
    List = pd.DataFrame(df.iloc[similar_indexes].food).values.tolist()
    # Hi = pd.DataFrame(df.iloc[similar_indexes].food)

    for i in range(len(List)):
        List[i] = List[i][0]

    return List




# @app.route('/login', methods = ['POST'])
# def signin():
#     email = request.json.get('email')
#     password = request.json.get('password')
#     if email is None or password is None:
#         return {"message": "Missing email or password"}, 400
    
#     try: 
#         user = auth.sign_in_with_email_and_password(email=email, password=password)
#         print (email)
#         user_id = auth.get_account_info(user['idToken'])
#         session['user'] = user_id
#         return {"message": f"User name: {user_id}"}, 200
#     except Exception as e:
#         return f"An Error Occurred: {e}"


# @app.route('/logout', methods = ['GET'])
# def logout():
#     # print (auth.current_user)
#     current_user = auth.current_user
#     if current_user is None:
#         return {"message":"No users signed in"}, 400

#     auth.current_user = None
#     return {"message": f"{current_user['email']} signed out"}, 200


# @app.route('/register', methods = ['GET','POST'])
# def register():
#     if request.method == 'POST':
#         email = request.json.get('email')
#         password = request.json.get('password')
#         if email is None or password is None:
#             return {"message": "Missing email or password"}, 400

#         try: 
#             auth.create_user_with_email_and_password(email=email, password=password)
#             return {"message": "Successfully registered"}, 200  
#         except Exception as e:
#             return f"An Error Occurred: {e}"


@app.route('/category1', methods = ['POST']) #ko -> ko
def category1():
    fdata = kodata.copy()
    cdata = kodata.copy()

    favDish= request.json.get('favDish')
    dislikeIngredient = request.json.get('dislikeIngredient')

    idx = cdata[cdata['ingredient'].str.contains(dislikeIngredient)].index
    cdata.drop(idx, inplace=True)
    cdata.reset_index(inplace=True, drop=True)

    # select df that contains 'food_input', insert that one row to 'vietdf' and variables declaration
    food_indf = 0

    for i in range(len(fdata['food'])):
        if favDish == fdata['food'][i].lower():
            food_indf = fdata.iloc[i:i+1]

    if food_indf == 0 :    #not in locals():
        for i in range(len(fdata['food'])):
            if favDish in fdata['food'][i].lower():
                food_indf = fdata.iloc[i:i+1]
                print(2)
#if 'food_indf' not in locals(): 근영아 여기란다! 아직도 0이면 어떻게 처리해야하는지!

# variables declaration
    doc = pd.concat([food_indf, cdata])
    doc.reset_index(drop=True, inplace=True)

    count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2))
    place_category = count_vect_category.fit_transform(doc['ingredient']) 
    place_simi_cate = cosine_similarity(place_category, place_category) 
    place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]

    tmp_dishes_list = find_simi_place(doc, place_simi_cate_sorted_ind, favDish, 5)
    return {"similar_dishes": tmp_dishes_list}, 200    


@app.route('/category2', methods = ['POST']) #vi -> vi
def category2():
    fdata = vidata.copy()
    cdata = vidata.copy()

    favDish= request.json.get('favDish')
    dislikeIngredient = request.json.get('dislikeIngredient')

    idx = cdata[cdata['ingredient'].str.contains(dislikeIngredient)].index
    cdata.drop(idx, inplace=True)
    cdata.reset_index(inplace=True, drop=True)

    # select df that contains 'food_input', insert that one row to 'vietdf' and variables declaration
    food_indf = 0

    for i in range(len(fdata['food'])):
        if favDish == fdata['food'][i].lower():
            food_indf = fdata.iloc[i:i+1]

    if food_indf == 0 :    #not in locals():
        for i in range(len(fdata['food'])):
            if favDish in fdata['food'][i].lower():
                food_indf = fdata.iloc[i:i+1]
                print(2)
#if 'food_indf' not in locals(): 근영아 여기란다! 아직도 0이면 어떻게 처리해야하는지!

# variables declaration
    doc = pd.concat([food_indf, cdata])
    doc.reset_index(drop=True, inplace=True)

    count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2))
    place_category = count_vect_category.fit_transform(doc['ingredient']) 
    place_simi_cate = cosine_similarity(place_category, place_category) 
    place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]

    tmp_dishes_list = find_simi_place(doc, place_simi_cate_sorted_ind, favDish, 5)
    return {"similar_dishes": tmp_dishes_list}, 200    


@app.route('/category3', methods = ['POST']) #vi -> ko
def category3():
    fdata = vidata.copy()
    cdata = kodata.copy()

    favDish= request.json.get('favDish')
    dislikeIngredient = request.json.get('dislikeIngredient')

    idx = cdata[cdata['ingredient'].str.contains(dislikeIngredient)].index
    cdata.drop(idx, inplace=True)
    cdata.reset_index(inplace=True, drop=True)

    # select df that contains 'food_input', insert that one row to 'vietdf' and variables declaration
    food_indf = 0

    for i in range(len(fdata['food'])):
        if favDish == fdata['food'][i].lower():
            food_indf = fdata.iloc[i:i+1]

    if food_indf == 0 :    #not in locals():
        for i in range(len(fdata['food'])):
            if favDish in fdata['food'][i].lower():
                food_indf = fdata.iloc[i:i+1]
                print(2)
#if 'food_indf' not in locals(): 근영아 여기란다! 아직도 0이면 어떻게 처리해야하는지!

# variables declaration
    doc = pd.concat([food_indf, cdata])
    doc.reset_index(drop=True, inplace=True)

    count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2))
    place_category = count_vect_category.fit_transform(doc['ingredient']) 
    place_simi_cate = cosine_similarity(place_category, place_category) 
    place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]

    tmp_dishes_list = find_simi_place(doc, place_simi_cate_sorted_ind, favDish, 5)
    return {"similar_dishes": tmp_dishes_list}, 200    

@app.route('/category4', methods = ['POST']) #ko -> vi
def category4():
    fdata = kodata.copy()
    cdata = vidata.copy()

    favDish= request.json.get('favDish')
    dislikeIngredient = request.json.get('dislikeIngredient')

    idx = cdata[cdata['ingredient'].str.contains(dislikeIngredient)].index
    cdata.drop(idx, inplace=True)
    cdata.reset_index(inplace=True, drop=True)

    # select df that contains 'food_input', insert that one row to 'vietdf' and variables declaration
    food_indf = 0

    for i in range(len(fdata['food'])):
        if favDish == fdata['food'][i].lower():
            food_indf = fdata.iloc[i:i+1]

    if food_indf == 0 :    #not in locals():
        for i in range(len(fdata['food'])):
            if favDish in fdata['food'][i].lower():
                food_indf = fdata.iloc[i:i+1]
                print(2)
#if 'food_indf' not in locals(): 근영아 여기란다! 아직도 0이면 어떻게 처리해야하는지!

# variables declaration
    doc = pd.concat([food_indf, cdata])
    doc.reset_index(drop=True, inplace=True)

    count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2))
    place_category = count_vect_category.fit_transform(doc['ingredient']) 
    place_simi_cate = cosine_similarity(place_category, place_category) 
    place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]

    tmp_dishes_list = find_simi_place(doc, place_simi_cate_sorted_ind, favDish, 5)
    return {"similar_dishes": tmp_dishes_list}, 200    

if __name__ == '__main__':
    app.run()