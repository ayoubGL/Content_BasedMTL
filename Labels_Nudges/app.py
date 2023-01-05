from datetime import datetime
import csv


from collections import defaultdict
import os
import pandas as pd
import numpy as np


# Read data
recipes = pd.read_csv('./static/Data_csv/all_recipes_content.csv')
CosineSim = np.load('./static/Data_csv/RecipesCosineSim.npy')

# reverse mapping of recipes names and dataframe indices
indices = pd.Series(recipes.index, index=recipes.Name).drop_duplicates()

def get_top_recommendations(Name, L,cosinse_sim = CosineSim):
    
    # get indix of the recipes
    idx = indices[Name]
    # print('+++++++++++',idx)
    
    # get the pairwise sim
    sim_scores = list(enumerate(cosinse_sim[idx]))
    
    # Sort the recipes based on the similarity score
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    
    # get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:L+1]

    # get the recipe index
    recipes_idx = [i[0] for i in sim_scores]
    
    # return the top 10 similar
    return recipes['Name'].iloc[recipes_idx]




def similiarSet(Names):
    print('---+======**************************', Names)

    l = len(Names)
    match l:
        case 1:
            return list(get_top_recommendations(Names[0], 10))
        case 2:
            rec = []
            for i in Names:
                rec.append(list(get_top_recommendations(i, 5)))
            return rec
        case 3 : 
            rec = []
            for i in Names[:-1]:
                rec.append(list(get_top_recommendations(i,4)))
            rec.append(list(get_top_recommendations(Names[-1], 2)))
            return rec
        case 4:
            rec = []
            for i in Names[:-1]:
                rec.append(list(get_top_recommendations(i,3)))
            rec.append(list(get_top_recommendations(Names[-1], 1)))
            return rec
        case 5 :
            rec = []
            for i in Names:
                rec.append(list(get_top_recommendations(i,2)))
            return rec
        case 6:
            rec = []
            for i in Names[:-2]:
                rec.append(list(get_top_recommendations(i,2)))
            for i in Names[-2:]:
                rec.append(list(get_top_recommendations(i,1)))
            return rec
        case 7:
            rec = []
            for i in Names[:-4]:
                rec.append(list(get_top_recommendations(i,2)))
            for i in Names[-4:]:
                rec.append(list(get_top_recommendations(i,1)))
            return rec
        case 8:
            rec = []
            for i in Names[:-6]:
                rec.append(list(get_top_recommendations(i,2)))
            for i in Names[-6:]:
                rec.append(list(get_top_recommendations(i,1))) 
            return rec   
        case 9:
            rec = []
            for i in Names[:-8]:
                rec.append(list(get_top_recommendations(i,2)))
            for i in Names[-8:]:
                rec.append(list(get_top_recommendations(i,1))) 
            return rec   
        # case 10:
        #     rec = []
        #     for i in Names:
        #         rec.append(list(get_top_recommendations(i,1)))
        #     return rec
        case _:
            return 'No similar'    


