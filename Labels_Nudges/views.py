from select import select
from django.forms import formset_factory
from django.db.models import Count
import datetime
# from datetime import datetime
import pandas as pd
from random import choice, sample
import random
from sys import prefix
from django import forms
from django.db import reset_queries
from django.forms.models import ModelForm
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from pandas.core.indexes import category
import itertools

from Labels_Nudges.app import get_top_recommendations
from .forms import Personal_infoForm, FoodCategory, FoodCategoryForm,ChoiceEvaluationForm
# from django.forms import formset_factory, modelformset_factory
from .models import  Personal_info, Recipes , SelectedRecipe,EvaluateChoices, Recommendations, SelectedContent
from .app import *
# Create your views here.
# person_id = 0
import string
import random
import re
#def home(request):
#   request.session['person_id'] = 0
#  return render(request, 'Labels_Nudges/homes.html', context={})

def home(request):
    request.session['person_id'] = 0
    #prolific_id = , msg)
    #prolific_id = str(prolific_id.group(1))
    full_url = request.get_full_path()
    #request.GET['PROLIFIC_PID']
    print('Full',request.get_full_path())
    #print(full_url)
    if 'PROLIFIC_PID' in full_url:
        prolific_id = re.search("PROLIFIC_PID=(.*?)&STUDY_ID",full_url)
        request.session['prolific_id'] = str(prolific_id.group(1))
        #print("----------",prolific_id.group(1))
    else:
        request.session['prolific_id'] = '000'
    return render(request, 'Labels_Nudges/homes.html')


def personal_info(request):
    user_selected = Personal_info.objects.filter(id = request.session['person_id'])
    if user_selected:
        Personal_info.objects.filter(id=request.session['person_id']).delete()
    if request.method == 'POST':
        personl_info = Personal_infoForm(request.POST)
        if personl_info.is_valid():
            answer = personl_info.save(commit=False)
            
            rd_str =''.join(random.choice(string.ascii_lowercase) for _ in range(5))
            time_now = datetime.now().strftime('%H%M%S')
            gene_session = 'dars'+time_now +'_'+str(answer.id)+rd_str
            personl_info.instance.session_id = gene_session

            answer = personl_info.save(commit=True)
            
            request.session['person_id'] = answer.id
            gene_session = 'dars'+time_now +'_'+str(answer.id)+rd_str
            personl_info.instance.session_id = request.session['prolific_id']
            
            request.session['session_id'] = gene_session
            answer = personl_info.save(commit=True)

            request.session['person_id'] = answer.id
            return redirect('Labels_Nudges:selectRecipe')
    else:
        personl_info = Personal_infoForm()
    return render(request, 'Labels_Nudges/personal_info.html', context={'form': personl_info})

def ghs_fk(request):
    user_selected = Ghs_fk.objects.filter(id = request.session['person_id'])
    if user_selected:
        ghs_fk.objects.filter(id=request.session['person_id']).delete()
    if request.method == 'POST':
        ghs_fk_form = Ghs_fkForm(request.POST)
        #print('------- Here')
        if ghs_fk_form.is_valid():
            answer = ghs_fk_form.save(commit=False)

            rd_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
            time_now = datetime.now().strftime('%H%M%S')
            gene_session = 'dars' +  time_now + '_' + str(answer.id) + rd_str
            ghs_fk_form.instance.session_id = gene_session
            ghs_fk_form.instance.person_id = request.session['person_id']
            #print(';;;;;;;;;;;here')
            answer = ghs_fk_form.save(commit = True)

            #request.session['person_id'] = answer.id
            return redirect('Labels_Nudges:selectRecipe')
    else:
        ghs_fk_form = Ghs_fkForm()
    return render(request, 'Labels_Nudges/healthy_knowledge.html', context={'form':ghs_fk_form})

def random_recipes():

    h_recipes = sample(list(Recipes.objects.filter(Fsa_new__lte = 8).values_list('id', flat=True)), 5)
    uh_recipes = sample(list(Recipes.objects.filter(Fsa_new__gte = 9).values_list('id',flat=True)),5)
    
    return h_recipes, uh_recipes




def selectRecipe(request):
    user_selected = SelectedContent.objects.filter(id = request.session['person_id'])
    if user_selected:
        SelectedContent.objects.filter(id=request.session['person_id']).delete()
    if request.method == "POST":
        selectedContentM = SelectedContent()
        recipe_id = request.POST.getlist('recipe_id')
        
        # print("------****------",recipe_id)
        
        
        # selectedContent.session_id = gene_session,
        selectedContentM.person_id = request.session['person_id']
        selectedContentM.contentIDs = recipe_id
        selectedContentM.save()
        
        request.session['selectedRecipes'] = recipe_id
        
        return redirect('Labels_Nudges:recipe_recommendations')
    else:
        
        #     categoryForm = FoodCategoryForm()
        recipes, un_recipes = random_recipes()
        # print(recipes, un_recipes)
            # extract 5 healthy recipes
        h_0_recipe =  Recipes.objects.get(id=recipes[0])
        h_1_recipe = Recipes.objects.get(id=recipes[1])
        h_2_recipe = Recipes.objects.get(id=recipes[2])
        h_3_recipe = Recipes.objects.get(id=recipes[3])
        h_4_recipe = Recipes.objects.get(id=recipes[4])
        # extract 5 unhhealthy recipes
        unh_0_recipe = Recipes.objects.get(id=un_recipes[0])
        unh_1_recipe = Recipes.objects.get(id=un_recipes[1])
        unh_2_recipe = Recipes.objects.get(id=un_recipes[2])
        unh_3_recipe = Recipes.objects.get(id=un_recipes[3])
        unh_4_recipe = Recipes.objects.get(id=un_recipes[4])
        # print('-----------', h_0_recipe.salt_count)
        # print('-------',h_0_recipe.content)
        
        h_0 = [h_0_recipe.Name, recipes[0], 'healthy', h_0_recipe.image_link, int(float(h_0_recipe.calories_kCal)),
                                    int(float(h_0_recipe.Servings)),int(float(h_0_recipe.size_g) // float(h_0_recipe.Servings)), h_0_recipe.salt_g,h_0_recipe.sugar_g,h_0_recipe.fat_g,h_0_recipe.saturate_g, h_0_recipe.content]
        # print('%%%%%%%%%%%%%%', h_0)
        h_0_ing = h_0_recipe.content.capitalize()
        
        
        h_1 = [h_1_recipe.Name, recipes[1], 'healthy', h_1_recipe.image_link, int(float(h_1_recipe.calories_kCal)),
                                    int(float(h_1_recipe.Servings)),int(float(h_1_recipe.size_g) // float(h_1_recipe.Servings)), h_1_recipe.salt_g,h_1_recipe.sugar_g,h_1_recipe.fat_g,h_1_recipe.saturate_g, h_0_recipe, h_1_recipe.content.capitalize()]
        h_1_ing = h_1_recipe.content.capitalize()
        
        h_2 = [h_2_recipe.Name, recipes[2], 'healthy', h_2_recipe.image_link, int(float(h_2_recipe.calories_kCal)), 
                                int(float(h_2_recipe.Servings)),int(float(h_2_recipe.size_g) // float(h_2_recipe.Servings)), h_2_recipe.salt_g,h_2_recipe.sugar_g,h_2_recipe.fat_g,h_2_recipe.saturate_g, h_2_recipe.content.capitalize()]
        h_2_ing = h_2_recipe.content.capitalize()
        
        h_3 = [h_3_recipe.Name, recipes[3], 'healthy', h_3_recipe.image_link, int(float(h_3_recipe.calories_kCal)),
                                    int(float(h_3_recipe.Servings)),int(float(h_3_recipe.size_g) // float(h_3_recipe.Servings)), h_3_recipe.salt_g,h_3_recipe.sugar_g,h_3_recipe.fat_g,h_3_recipe.saturate_g, h_3_recipe.content.capitalize()]
        h_3_ing = h_3_recipe.content.capitalize()
        
        h_4 = [h_4_recipe.Name, recipes[4], 'healthy', h_4_recipe.image_link, int(float(h_4_recipe.calories_kCal)), 
                                int(float(h_4_recipe.Servings)),int(float(h_4_recipe.size_g) // float(h_4_recipe.Servings)), h_4_recipe.salt_g,h_4_recipe.sugar_g,h_4_recipe.fat_g,h_4_recipe.saturate_g, h_4_recipe.content.capitalize()]
        
        h_4_ing = h_4_recipe.content.capitalize()
        
        
        unh_0 = [unh_0_recipe.Name, un_recipes[0], 'unhealthy', unh_0_recipe.image_link, int(float(unh_0_recipe.calories_kCal)), int(float(unh_0_recipe.Servings)),int(float(unh_0_recipe.size_g) // float(unh_0_recipe.Servings)),unh_0_recipe.salt_g,unh_0_recipe.sugar_g,unh_0_recipe.fat_g,unh_0_recipe.saturate_g, unh_0_recipe.content.capitalize()]
        
        unh_0_ing = unh_0_recipe.content.capitalize()
        
        
        unh_1 = [unh_1_recipe.Name, un_recipes[1], 'unhealthy', unh_1_recipe.image_link, int(float(unh_1_recipe.calories_kCal)),int(float(unh_1_recipe.Servings)),int(float(unh_1_recipe.size_g) // float(unh_1_recipe.Servings)),unh_1_recipe.salt_g,unh_1_recipe.sugar_g,unh_1_recipe.fat_g,unh_1_recipe.saturate_g,unh_1_recipe.content.capitalize() ]
        
        unh_1_ing = unh_1_recipe.content.capitalize()
        
        
        unh_2 = [unh_2_recipe.Name, un_recipes[2], 'unhealthy', unh_2_recipe.image_link, int(float(unh_2_recipe.calories_kCal)), int(float(unh_2_recipe.Servings)),int(float(unh_3_recipe.size_g) // float(unh_3_recipe.Servings)),unh_2_recipe.salt_g,unh_2_recipe.sugar_g,unh_2_recipe.fat_g,unh_2_recipe.saturate_g, unh_2_recipe.content.capitalize()]
        
        unh_2_ing = unh_2_recipe.content.capitalize()
        
        unh_3 = [unh_3_recipe.Name, un_recipes[3], 'unhealthy', unh_3_recipe.image_link, int(float(unh_3_recipe.calories_kCal)), int(float(unh_3_recipe.Servings)),int(float(unh_3_recipe.size_g) // float(unh_3_recipe.Servings)),unh_3_recipe.salt_g,unh_3_recipe.sugar_g,unh_3_recipe.fat_g,unh_3_recipe.saturate_g, unh_3_recipe.content.capitalize()]
        
        unh_3_ing = unh_3_recipe.content.capitalize()
        
        unh_4 = [unh_4_recipe.Name, un_recipes[4], 'unhealthy', unh_4_recipe.image_link, int(float(unh_4_recipe.calories_kCal)), int(float(unh_4_recipe.Servings)),int(float(unh_4_recipe.size_g) // float(unh_4_recipe.Servings)),unh_4_recipe.salt_g,unh_4_recipe.sugar_g,unh_4_recipe.fat_g,unh_4_recipe.saturate_g, unh_4_recipe.content.capitalize()]
        
        unh_4_ing = unh_4_recipe.content.capitalize()
        print('............>',h_0)
    # h_0 = [h_0_recipe.Name, recipes[0], 'healthy', h_0_recipe.image_link, int(float(h_0_recipe.calories_kCal)),
    #                                 int(float(h_0_recipe.Servings)),int(float(h_0_recipe.size_g) // float(h_0_recipe.Servings)), h_0_recipe.salt_g,h_0_recipe.sugar_g,h_0_recipe.fat_g,h_0_recipe.saturate_g]    
    return render(request, 'Labels_Nudges/SelectRecipes.html', context={
                                                'h_0':h_0,
                                                'h_1':h_1,
                                                'h_2':h_2,
                                                'h_3':h_3,
                                                'h_4':h_4,
                                                'unh_0':unh_0,
                                                'unh_1':unh_1,
                                                'unh_2':unh_2,
                                                'unh_3':unh_3,
                                                'unh_4':unh_4,
                                                'h0Ing':h_0_ing,
                                                'h1Ing':h_1_ing,
                                                'h2Ing':h_2_ing,
                                                'h3Ing':h_3_ing,
                                                'h4Ing':h_4_ing,
                                                'unh0Ing':unh_0_ing,
                                                'unh1Ing':unh_1_ing,
                                                'unh2Ing':unh_2_ing,
                                                'unh3Ing':unh_3_ing,
                                                'unh4Ing':unh_4_ing,
                                                })


# --- Boost presentation -------
def nutrition_labels(request): 
    if request.method == "POST":
            return redirect('Labels_Nudges:recipe_recommendations')
    else:        
            return render(request, 'Labels_Nudges/boost.html')



def mtl_color(cnt):
    colors = ['green','orange','red']
    level = ['Low','Medium','High']
            # 5 salts (color, level)
    return [ (colors[cnt[0]-1], level[cnt[0]-1]), (colors[cnt[1]-1], level[cnt[1]-1]), (colors[cnt[2]-1], level[cnt[2]-1]), (colors[cnt[3]-1], level[cnt[3]-1]), (colors[cnt[4]-1], level[cnt[4]-1])    ]


def recipe_recommendations(request):

    person = request.session['person_id']


    real_user_input = request.session['selectedRecipes']
    print('----------->',len(real_user_input), real_user_input)

    recommendations__ =  similiarSet(real_user_input)
    
    if len(real_user_input) != 1 and len(real_user_input) != 10:
        recommendations__ = list(itertools.chain.from_iterable(similiarSet(real_user_input)))

    
    

    # get recommendation

    top_5_rec = recommendations__[:5]
    
    top_l5_rec  = recommendations__[-5:]
 
    

    print("top healthy recommendation------",top_5_rec)
    print("top unhealthy recommendation-------", top_l5_rec)

#  Extract recipes


    # extract 5 healthy recipes
    h_0_recipe = Recipes.objects.get(Name=top_5_rec[0])
    h_1_recipe = Recipes.objects.get(Name=top_5_rec[1])
    h_2_recipe = Recipes.objects.get(Name=top_5_rec[2])
    h_3_recipe = Recipes.objects.get(Name=top_5_rec[3])
    h_4_recipe = Recipes.objects.get(Name=top_5_rec[4])
    # extract 5 unhhealthy recipes
    unh_0_recipe = Recipes.objects.get(Name=top_l5_rec[0])
    unh_1_recipe = Recipes.objects.get(Name=top_l5_rec[1])
    unh_2_recipe = Recipes.objects.get(Name=top_l5_rec[2])
    unh_3_recipe = Recipes.objects.get(Name=top_l5_rec[3])
    unh_4_recipe = Recipes.objects.get(Name=top_l5_rec[4])
    
    # selected recipe model
    selected_recipe = SelectedRecipe() 

    # initialise healthy forms with extracted data
    if request.method == "POST":
                # if the user already select a recipe
        person = request.session['person_id']
        user_selected = SelectedRecipe.objects.filter(person_id = person)
        if user_selected:
            SelectedRecipe.objects.filter(person_id=person).delete()

        user_selected = Recommendations.objects.filter(person_id = request.session['person_id'])
        if user_selected:
            Recommendations.objects.filter(person_id=request.session['person_id']).delete()


        # print('Request POST------------',request.POST)
        recipe_name = request.POST.get('recipe_name')
        recipe_id = request.POST.get('recipe_id')
        recipe_h  = request.POST.get('healthiness')

       
        nutri__fsa = Recipes.objects.filter(id=recipe_id).values_list('Nutri_score','Fsa_new')

        selected_recipe.Nutri_score = nutri__fsa[0][0]
        selected_recipe.fsa_score = nutri__fsa[0][1]
        selected_recipe.person_id= person
        selected_recipe.recipe_name = recipe_name
        selected_recipe.recipe_id = recipe_id
        selected_recipe.healthiness = recipe_h
        selected_recipe.session_id = request.session['session_id']
        selected_recipe.save()

             # save recommendations
        h_recommendations = Recommendations()
      
        h_recommendations.person_id = person
        h_recommendations.recommended_recipes = [h_0_recipe.id,h_1_recipe.id,h_2_recipe.id,h_3_recipe.id,h_4_recipe.id,
                                                 unh_0_recipe.id,unh_1_recipe.id,unh_2_recipe.id,unh_3_recipe.id,unh_4_recipe.id,]
        # h_recommendations.healthiness = 'Healthy'
        h_recommendations.save()

        # unh_recommendations = Recommendations()
        
        # unh_recommendations.person_id = person
        # unh_recommendations.recommended_recipes = [unh_0_recipe.id,unh_1_recipe.id,unh_2_recipe.id,unh_3_recipe.id,unh_4_recipe.id]
        # # unh_recommendations.healthiness = 'Unhealthy'
        # unh_recommendations.save()

        return redirect('Labels_Nudges:choice_evaluation')
    else:
      
        
        h_0 = [h_0_recipe.Name, h_0_recipe.id, h_0_recipe.healthiness, h_0_recipe.image_link, int(float(h_0_recipe.calories_kCal)),
                                 int(float(h_0_recipe.Servings)),int(float(h_0_recipe.size_g) // float(h_0_recipe.Servings)), h_0_recipe.salt_g,h_0_recipe.sugar_g,h_0_recipe.fat_g,h_0_recipe.saturate_g, h_0_recipe.content.capitalize()]
        
        h_1 = [h_1_recipe.Name, h_1_recipe.id, h_1_recipe.healthiness, h_1_recipe.image_link, int(float(h_1_recipe.calories_kCal)),
                                 int(float(h_1_recipe.Servings)),int(float(h_1_recipe.size_g) // float(h_1_recipe.Servings)), h_1_recipe.salt_g,h_1_recipe.sugar_g,h_1_recipe.fat_g,h_1_recipe.saturate_g, h_1_recipe.content]
        
        h_2 = [h_2_recipe.Name, h_2_recipe.id, h_2_recipe.healthiness, h_2_recipe.image_link, int(float(h_2_recipe.calories_kCal)), 
                               int(float(h_2_recipe.Servings)),int(float(h_2_recipe.size_g) // float(h_2_recipe.Servings)), h_2_recipe.salt_g,h_2_recipe.sugar_g,h_2_recipe.fat_g,h_2_recipe.saturate_g,
                               h_2_recipe.content]
        
        h_3 = [h_3_recipe.Name, h_3_recipe.id, h_3_recipe.healthiness, h_3_recipe.image_link, int(float(h_3_recipe.calories_kCal)),
                                 int(float(h_3_recipe.Servings)),int(float(h_3_recipe.size_g) // float(h_3_recipe.Servings)), h_3_recipe.salt_g,h_3_recipe.sugar_g,h_3_recipe.fat_g,h_3_recipe.saturate_g, h_3_recipe.content]
        
        h_4 = [h_4_recipe.Name, h_4_recipe.id, h_4_recipe.healthiness, h_4_recipe.image_link, int(float(h_4_recipe.calories_kCal)), 
                                int(float(h_4_recipe.Servings)),int(float(h_4_recipe.size_g) // float(h_4_recipe.Servings)), h_4_recipe.salt_g,h_4_recipe.sugar_g,h_4_recipe.fat_g,h_4_recipe.saturate_g,
                                h_4_recipe.content]
        
        
     
        

        h_salt =[int(float(h_0_recipe.salt_count)),int(float(h_1_recipe.salt_count)),int(float(h_2_recipe.salt_count)),int(float(h_3_recipe.salt_count)),int(float(h_4_recipe.salt_count))]
        
        h_sugar = [int(float(h_0_recipe.sugar_count)),int(float(h_1_recipe.sugar_count)),int(float(h_2_recipe.sugar_count)), int(float(h_3_recipe.sugar_count)), int(float(h_4_recipe.sugar_count))]
        
        h_fat =[int(float(h_0_recipe.fat_count)), int(float(h_1_recipe.fat_count)), int(float(h_2_recipe.fat_count)),int(float(h_3_recipe.fat_count)),int(float(h_4_recipe.fat_count))]
        
        h_satfat =[ int(float(h_0_recipe.satfat_count)),int(float(h_1_recipe.satfat_count)),int(float(h_2_recipe.satfat_count)),int(float(h_3_recipe.satfat_count)), int(float(h_4_recipe.satfat_count))]


        salt_h = [mtl_color(h_salt),h_0[7], h_1[7], h_2[7], h_3[7], h_4[7]] 
        
        sugar_h = [ mtl_color(h_sugar),h_0[8],h_1[8], h_2[8], h_3[8], h_4[8]] 
        
        fat_h = [mtl_color(h_fat),h_0[9], h_1[9], h_2[9], h_3[9], h_4[9]] 
        
        satfat_h = [ mtl_color(h_satfat),h_0[10], h_1[10], h_2[10], h_3[10], h_4[10]]



        unh_0 = [unh_0_recipe.Name, unh_0_recipe.id,unh_0_recipe.healthiness, unh_0_recipe.image_link, int(float(unh_0_recipe.calories_kCal)), int(float(unh_0_recipe.Servings)),int(float(unh_0_recipe.size_g) // float(unh_0_recipe.Servings)),unh_0_recipe.salt_g,unh_0_recipe.sugar_g,unh_0_recipe.fat_g,unh_0_recipe.saturate_g, unh_0_recipe.content]
       
        unh_1 = [unh_1_recipe.Name, unh_0_recipe.id,unh_1_recipe.healthiness, unh_1_recipe.image_link, int(float(unh_1_recipe.calories_kCal)),int(float(unh_1_recipe.Servings)),int(float(unh_1_recipe.size_g) // float(unh_1_recipe.Servings)),unh_1_recipe.salt_g,unh_1_recipe.sugar_g,unh_1_recipe.fat_g,unh_1_recipe.saturate_g, unh_1_recipe.content]
       
        unh_2 = [unh_2_recipe.Name, unh_0_recipe.id,unh_2_recipe.healthiness, unh_2_recipe.image_link, int(float(unh_2_recipe.calories_kCal)), int(float(unh_2_recipe.Servings)),int(float(unh_3_recipe.size_g) // float(unh_3_recipe.Servings)),unh_2_recipe.salt_g,unh_2_recipe.sugar_g,unh_2_recipe.fat_g,unh_2_recipe.saturate_g,unh_2_recipe.content ]
       
        unh_3 = [unh_3_recipe.Name, unh_0_recipe.id,unh_3_recipe.healthiness, unh_3_recipe.image_link, int(float(unh_3_recipe.calories_kCal)), int(float(unh_3_recipe.Servings)),int(float(unh_3_recipe.size_g) // float(unh_3_recipe.Servings)),unh_3_recipe.salt_g,unh_3_recipe.sugar_g,unh_3_recipe.fat_g,unh_3_recipe.saturate_g, unh_3_recipe.content]
       
        unh_4 = [unh_4_recipe.Name, unh_0_recipe.id,unh_4_recipe.healthiness, unh_4_recipe.image_link, int(float(unh_4_recipe.calories_kCal)), int(float(unh_4_recipe.Servings)),int(float(unh_4_recipe.size_g) // float(unh_4_recipe.Servings)),unh_4_recipe.salt_g,unh_4_recipe.sugar_g,unh_4_recipe.fat_g,unh_4_recipe.saturate_g, unh_4_recipe.content]
        
    
        unh_salt =[int(float(unh_0_recipe.salt_count)),int(float(unh_1_recipe.salt_count)),int(float(unh_2_recipe.salt_count)),int(float(unh_3_recipe.salt_count)),int(float(unh_4_recipe.salt_count))]
        
        
        unh_sugar = [int(float(unh_0_recipe.sugar_count)),int(float(unh_1_recipe.sugar_count)),int(float(unh_2_recipe.sugar_count)), int(float(unh_3_recipe.sugar_count)), int(float(unh_4_recipe.sugar_count))]
        unh_fat =[int(float(unh_0_recipe.fat_count)), int(float(unh_1_recipe.fat_count)), int(float(unh_2_recipe.fat_count)),int(float(unh_3_recipe.fat_count)),int(float(unh_4_recipe.fat_count))]
        unh_satfat =[ int(float(unh_0_recipe.satfat_count)),int(float(unh_1_recipe.satfat_count)),int(float(unh_2_recipe.satfat_count)),int(float(unh_3_recipe.satfat_count)), int(float(unh_4_recipe.satfat_count))]
        
        


        salt_unh = [mtl_color(unh_salt),unh_0[7],unh_1[7],unh_2[7],unh_3[7],unh_4[7]] 
        sugar_unh = [ mtl_color(unh_sugar),unh_0[8],unh_1[8],unh_2[8],unh_3[8],unh_4[8]] 
        fat_unh = [mtl_color(unh_fat),unh_0[9],unh_1[9],unh_2[9],unh_3[9],unh_4[9]] 
        satfat_unh = [ mtl_color(unh_satfat),unh_0[10],unh_1[10],unh_2[10],unh_3[10],unh_4[10]] 

    # send forms
    return render(request,'Labels_Nudges/recipe_recommendations.html',context={
                                                'h_0':h_0,
                                                'h_1':h_1,
                                                'h_2':h_2,
                                                'h_3':h_3,
                                                'h_4':h_4,
                                                'unh_0':unh_0,
                                                'unh_1':unh_1,
                                                'unh_2':unh_2,
                                                'unh_3':unh_3,
                                                'unh_4':unh_4,
                                                'h_salt':salt_h,
                                                'h_sugar':sugar_h,
                                                'h_fat':fat_h,
                                                'h_satfat':satfat_h,
                                                'unh_salt':salt_unh,
                                                'unh_sugar':sugar_unh,
                                                'unh_fat':fat_unh,
                                                'unh_satfat':satfat_unh
   
                                                })


def choice_evaluation(request):
    user_selected = EvaluateChoices.objects.filter(person_id = request.session['person_id'])
    if user_selected:
        EvaluateChoices.objects.filter(person_id=request.session['person_id']).delete()

    if request.method == 'POST':
        evaluation_form = ChoiceEvaluationForm(request.POST)
        person = request.session['person_id']
        ChoiceEvaltion = EvaluateChoices()
        if evaluation_form.is_valid():
            # print("-----------here we are")
            # ChoiceEvaltion.person = request.session['person_id']
            evaluation_ = evaluation_form.save(commit=False)
            evaluation_.person_id = person
            # ChoiceEvaltion.person_id = evaluation_form.foriengkey
            evaluation_.session_id = request.session['prolific_id']
            evaluation_.save()
            return redirect('Labels_Nudges:thank_u')
    else:
         evaluation_form = ChoiceEvaluationForm()
    return render(request, 'Labels_Nudges/choice_evaluation.html', context={'eval_form': evaluation_form})

def thank_u(request):
    return render(request, 'Labels_Nudges/thanks.html', context={'session_id':request.session['session_id']})

def error_404(request,exception):
    data = {}
    return render(request, 'Labels_Nudges/404.html',data)
def error_500(request):
        data = {}
        return render(request,'Labels_Nudges/404.html', data)




