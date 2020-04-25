# -*- coding: utf-8 -*-
"""
Created on Tue Apr  24 18:48:55 2020

@author: yasmen amr
"""
import os
import pandas as pd
from surprise import Dataset, KNNWithMeans, Reader

APP_PATH=os.path.dirname(os.path.abspath(__file__))

book_info = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "items_info.dat")),sep='\t',index_col=False)
book_ratings = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "book_ratings.dat")),sep='\t',index_col=False)



reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(book_ratings[['user', "item", "rating"]], reader)

# To use item-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": False,  # Compute  similarities between items
}
model = KNNWithMeans(sim_options=sim_options)

trainingSet = data.build_full_trainset()
model.fit(trainingSet)


book_ratings2=book_ratings.drop(['user'], axis=1)
book_ratings2=book_ratings2.groupby('item').mean()
book_ratings2['Book_ID']=book_ratings2.index

#join in ratio from the other table

book_info['rating']= None
book_info = book_info.join(book_ratings2.set_index(["Book_ID"])["rating"].to_frame("ratio2"), on=["Book_ID"])

# take ratio2 first, then the existing ratio value if ratio2 is null
book_info["rating"] = book_info["ratio2"].fillna(book_info["rating"])

# delete the ratio2 column
del book_info["ratio2"]
book_info['average_rating']=book_info['rating']
book_info=book_info.drop(['rating'],axis=1)

def top_5_recommendations(uid):
    books_rated_by_user = book_ratings.loc[book_ratings['user'] == uid, "item"].values

    other_books = book_info.loc[~book_info['Book_ID'].isin(books_rated_by_user)].sort_values(
        by='average_rating', ascending=False)

    # if the user exists or not
    if uid not in set(book_ratings['user']):
        return other_books[:5]

    other_books['user_rate'] = other_books['Book_ID'].apply(lambda x: model.predict(uid, x).est)

    return other_books.sort_values(by='user_rate', ascending=False).drop(['user_rate'],axis=1)