# import os
# import pyrebase
# from flask import Flask, request, jsonify, session, Response

# import pandas as pd
# import numpy as np
# from itertools import chain
# from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer('sentence-transformers/paraphrase-distilroberta-base-v1')


# # viet_li


# app = Flask(__name__)

# config = {
#   "apiKey": "AIzaSyAG6QwyEiDmFV4pWQHQn-1q5J4Y6mlJcEI",
#   "authDomain": "lav1ne-sample.firebaseapp.com",
#   "projectId": "lav1ne-sample",
#   "storageBucket": "lav1ne-sample.appspot.com",
#   "messagingSenderId": "374481316324",
#   "appId": "1:374481316324:web:169065ccd71cc6db733ff1",
#   "measurementId": "G-3DE8YQ5DBG",
#   "databaseURL": ""
# }


# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()

# app.secret_key='secret'


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


# @app.route('/category1', methods = ['POST'])
# def category1():
#     # if auth.current_user is None:
#     #     return {'message': 'No users signed in'}, 400

#     frydf = pd.read_csv('frydf.csv').copy()
#     heatdf = pd.read_csv('heatdf.csv').copy()
#     bakedf = pd.read_csv('bakedf.csv').copy()
#     stirfrydf = pd.read_csv('stirfrydf.csv').copy()
#     boildowndf = pd.read_csv('boildowndf.csv').copy()
#     griddledf = pd.read_csv('griddledf.csv').copy()
#     steamdf = pd.read_csv('steamdf.csv').copy()
#     seasondf = pd.read_csv('seasondf.csv').copy()
#     pickledf = pd.read_csv('pickledf.csv').copy()
#     rubdf = pd.read_csv('rubdf.csv').copy()
#     blanchdf = pd.read_csv('blanchdf.csv').copy()
#     boildf = pd.read_csv('boildf.csv').copy()
#     rawdf = pd.read_csv('rawdf.csv').copy()
#     otherdf = pd.read_csv('otherdf.csv').copy()
#     vietdf = pd.read_csv('vietdf.csv').copy()

#     recipe_list = [frydf,heatdf,bakedf,stirfrydf,boildowndf,griddledf,steamdf,seasondf,pickledf,rubdf,blanchdf,boildf,rawdf,otherdf,vietdf]

#     favDish= request.json.get('favDish')
#     dislikeIngredient = request.json.get('dislikeIngredient')
    
#     # drop foods that contains 'dislikeIngredient'
#     for i in recipe_list:
#         idx = i[i['CKG_MTRL_CN'].str.contains(dislikeIngredient)].index
#         i.drop(idx, inplace=True)
#         i.reset_index(inplace=True)

#     # select df that contains 'favDish' and variables declaration

#     for i in recipe_list:
#           if favDish in i['CKG_NM'].to_list():
#             train_data = i
#             doc_reci = train_data["CKG_MTRL_CN"].to_list()
#             doc_name = train_data["CKG_NM"].to_list()
#             embeddings = model.encode(doc_reci, convert_to_tensor=True)
#             cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)

#     # find orders of 'favDish'
#     for i in range(len(train_data['CKG_NM'])):
#         if train_data['CKG_NM'][i] == favDish:
#             org=i
    
#     # when 'org' is not defined
#     if 'org' not in locals():
#         org=0

#     temp=cosine_scores[org]
#     temp.argsort(descending=True)[0:10]
#     tmp_dishes_list =[]

#     for i in temp.argsort(descending=True)[0:10]:
#         tmp_dishes_list.append(doc_name[i])
#         print(f"{doc_name[i]}")

#     # for user_input in input_list:
#     #     recipes = find_simi_place(data, place_simi_cate_sorted_ind, user_input, 5)
#     #     tmp_dishes_list.append(recipes[0].astype(str).tolist())
    
#     # similar_dishes_list = list(chain.from_iterable(tmp_dishes_list))
#     # list(set(similar_dishes_list))
    
#     return jsonify({"dishes": tmp_dishes_list}), 200  
#     # return {"similar_dishes": "sth"}, 200  


# @app.route('/category2', methods = ['POST'])
# def category2():
#     # if auth.current_user is None:
#     #     return {'message': 'No users signed in'}, 400

#     vietdf = pd.read_csv('vietdf.csv').copy()

#     famCountry = request.json.get('famCountry')
#     curCountry = request.json.get('curCountry')
#     favDish= request.json.get('favDish')
#     dislikeIngredient = request.json.get('dislikeIngredient')
    
#     # drop foods that contains 'dislikeIngredient'
#     idx = vietdf[vietdf['CKG_MTRL_CN'].str.contains(dislikeIngredient)].index
#     vietdf.drop(idx, inplace=True)
#     vietdf.reset_index(inplace=True)

#     # variables declaration
#     doc_reci = vietdf["CKG_MTRL_CN"].to_list()
#     doc_name = vietdf["CKG_NM"].to_list()

#     # vector embedding(?), calculating cosine_similarities
#     embeddings = model.encode(doc_reci, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)    

#     # find orders of 'favDish'
#     for i in range(len(vietdf['CKG_NM'])):
#         if vietdf['CKG_NM'][i] == favDish:
#             org=i
#         elif favDish in vietdf['CKG_NM'][i]:
#             org=i
    
#     # when 'org' is not defined
#     if 'org' not in locals():
#         org=0

#     temp=cosine_scores[org]
#     temp.argsort(descending=True)[0:10]
#     tmp_dishes_list =[]

#     for i in temp.argsort(descending=True)[0:10]:
#         tmp_dishes_list.append(doc_name[i])
#         print(f"{doc_name[i]}")

#     # for user_input in input_list:
#     #     recipes = find_simi_place(data, place_simi_cate_sorted_ind, user_input, 5)
#     #     tmp_dishes_list.append(recipes[0].astype(str).tolist())
    
#     # similar_dishes_list = list(chain.from_iterable(tmp_dishes_list))
#     # list(set(similar_dishes_list))
    
#     return jsonify({"dishes": tmp_dishes_list}), 200  
#     # return {"similar_dishes": "sth"}, 200  


# @app.route('/category3', methods = ['POST'])
# def category3():
#     # if auth.current_user is None:
#     #     return {'message': 'No users signed in'}, 400
#     frydf = pd.read_csv('frydf.csv').copy()
#     heatdf = pd.read_csv('heatdf.csv').copy()
#     bakedf = pd.read_csv('bakedf.csv').copy()
#     stirfrydf = pd.read_csv('stirfrydf.csv').copy()
#     boildowndf = pd.read_csv('boildowndf.csv').copy()
#     griddledf = pd.read_csv('griddledf.csv').copy()
#     steamdf = pd.read_csv('steamdf.csv').copy()
#     seasondf = pd.read_csv('seasondf.csv').copy()
#     pickledf = pd.read_csv('pickledf.csv').copy()
#     rubdf = pd.read_csv('rubdf.csv').copy()
#     blanchdf = pd.read_csv('blanchdf.csv').copy()
#     boildf = pd.read_csv('boildf.csv').copy()
#     rawdf = pd.read_csv('rawdf.csv').copy()
#     otherdf = pd.read_csv('otherdf.csv').copy()
#     vietdf = pd.read_csv('vietdf.csv').copy()

#     recipe_list = [frydf,heatdf,bakedf,stirfrydf,boildowndf,griddledf,steamdf,seasondf,pickledf,rubdf,blanchdf,boildf,rawdf,otherdf,vietdf]

#     favDish= request.json.get('favDish')
#     dislikeIngredient = request.json.get('dislikeIngredient')
#     # drop foods that contains 'dislikeIngredient'
#     for i in recipe_list:
#         idx = i[i['CKG_MTRL_CN'].str.contains(dislikeIngredient)].index
#         i.drop(idx, inplace=True)
#         i.reset_index(inplace=True, drop=True)

#     # select df that contains 'favDish', insert that one row to 'vietdf' and variables declaration
#     for i in recipe_list:
#         if favDish in i['CKG_NM'].to_list():
#             train_data = i

#     for i in range(len(train_data['CKG_NM'])):
#         if favDish == train_data['CKG_NM'][i]:
#             food_indf = train_data.iloc[i:i+1]

#     if 'food_indf' not in locals():
#         for i in range(len(train_data['CKG_NM'])):
#             if favDish in train_data['CKG_NM'][i]:
#                 food_indf = train_data.iloc[i:i+1]
#     #food_indf.drop('index', axis=1, inplace=True)

#     # variables declaration
#     doc = pd.concat([food_indf, vietdf])
#     doc_reci = doc["CKG_MTRL_CN"].to_list()
#     doc_name = doc["CKG_NM"].to_list()

#     # vector embedding(?), calculating cosine_similarities
#     embeddings = model.encode(doc_reci, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)       

#     temp = cosine_scores[0]
#     temp.argsort(descending=True)[0:10]
#     tmp_dishes_list =[]
#     for i in temp.argsort(descending=True)[0:10]:
#         tmp_dishes_list.append(doc_name[i])
#         # print('here')
#         print(f"{doc_name[i]}")

#     # for user_input in input_list:
#     #     recipes = find_simi_place(data, place_simi_cate_sorted_ind, user_input, 5)
#     #     tmp_dishes_list.append(recipes[0].astype(str).tolist())
    
#     # similar_dishes_list = list(chain.from_iterable(tmp_dishes_list))
#     # list(set(similar_dishes_list))
    
#     return jsonify({"dishes": tmp_dishes_list}), 200  
#     # return {"similar_dishes": "sth"}, 200  


# @app.route('/category4', methods = ['POST'])
# def category4():
#     # if auth.current_user is None:
#     #     return {'message': 'No users signed in'}, 400
#     frydf = pd.read_csv('frydf.csv').copy()
#     heatdf = pd.read_csv('heatdf.csv').copy()
#     bakedf = pd.read_csv('bakedf.csv').copy()
#     stirfrydf = pd.read_csv('stirfrydf.csv').copy()
#     boildowndf = pd.read_csv('boildowndf.csv').copy()
#     griddledf = pd.read_csv('griddledf.csv').copy()
#     steamdf = pd.read_csv('steamdf.csv').copy()
#     seasondf = pd.read_csv('seasondf.csv').copy()
#     pickledf = pd.read_csv('pickledf.csv').copy()
#     rubdf = pd.read_csv('rubdf.csv').copy()
#     blanchdf = pd.read_csv('blanchdf.csv').copy()
#     boildf = pd.read_csv('boildf.csv').copy()
#     rawdf = pd.read_csv('rawdf.csv').copy()
#     otherdf = pd.read_csv('otherdf.csv').copy()
#     vietdf = pd.read_csv('vietdf.csv').copy()

#     recipe_list = [frydf,heatdf,bakedf,stirfrydf,boildowndf,griddledf,steamdf,seasondf,pickledf,rubdf,blanchdf,boildf,rawdf,otherdf,vietdf]

#     favDish= request.json.get('favDish')
#     dislikeIngredient = request.json.get('dislikeIngredient')
#     # drop foods that contains 'dislikeIngredient'
#     for i in recipe_list:
#         idx = i[i['CKG_MTRL_CN'].str.contains(dislikeIngredient)].index
#         i.drop(idx, inplace=True)
#         i.reset_index(inplace=True, drop=True)

#    # select df that contains 'favDish', insert that one row to 'vietdf' and variables declaration
#     for i in range(len(vietdf['CKG_NM'])):
#         if favDish == vietdf['CKG_NM'][i]:
#             food_indf = vietdf.iloc[i:i+1]

#     if 'food_indf' not in locals():
#         for i in range(len(vietdf['CKG_NM'])):
#             if favDish in vietdf['CKG_NM'][i]:
#                 food_indf = vietdf.iloc[i:i+1]

#     #food_indf.drop('index', axis=1, inplace=True)
#     otherdf['CKG_MTH_ACTO_NM']
#     # variables declaration

#     doc = pd.concat([food_indf, recipe_list[1]]) # we have to fill 'CKG_MTH_ACTO_NM' columns (vietdf)
#     doc_reci = doc["CKG_MTRL_CN"].to_list()
#     doc_name = doc["CKG_NM"].to_list()

#     # vector embedding(?), calculating cosine_similarities
#     embeddings = model.encode(doc_reci, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)       

#     temp = cosine_scores[0]
#     temp.argsort(descending=True)[0:10]
#     tmp_dishes_list =[]
#     for i in temp.argsort(descending=True)[0:10]:
#         tmp_dishes_list.append(doc_name[i])
#         # print('here')
#         print(f"{doc_name[i]}")

#     # for user_input in input_list:
#     #     recipes = find_simi_place(data, place_simi_cate_sorted_ind, user_input, 5)
#     #     tmp_dishes_list.append(recipes[0].astype(str).tolist())
    
#     # similar_dishes_list = list(chain.from_iterable(tmp_dishes_list))
#     # list(set(similar_dishes_list))
    
#     return jsonify({"dishes": tmp_dishes_list}), 200  
#     # return {"similar_dishes": "sth"}, 200  

# if __name__ == '__main__':
#     app.run(host = 'localhost', port = 5000)

import os
import pyrebase
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


firebase = pyrebase.initialize_app(config)
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




@app.route('/login', methods = ['POST'])
def signin():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return {"message": "Missing email or password"}, 400
    
    try: 
        user = auth.sign_in_with_email_and_password(email=email, password=password)
        print (email)
        user_id = auth.get_account_info(user['idToken'])
        session['user'] = user_id
        return {"message": f"User name: {user_id}"}, 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@app.route('/logout', methods = ['GET'])
def logout():
    # print (auth.current_user)
    current_user = auth.current_user
    if current_user is None:
        return {"message":"No users signed in"}, 400

    auth.current_user = None
    return {"message": f"{current_user['email']} signed out"}, 200


@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None or password is None:
            return {"message": "Missing email or password"}, 400

        try: 
            auth.create_user_with_email_and_password(email=email, password=password)
            return {"message": "Successfully registered"}, 200  
        except Exception as e:
            return f"An Error Occurred: {e}"


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
    app.run(host = '0.0.0.0', port = 5000)