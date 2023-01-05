#from tkinter.tix import Select
from django import forms
from django.core.exceptions import ValidationError
from django.db import close_old_connections, models
from django.db.models import fields
from django.forms import widgets
from .models import FoodCategory, Personal_info,EvaluateChoices
from django_starfield import Stars
from django.forms import formset_factory, modelformset_factory


class Personal_infoForm(forms.ModelForm):
    class Meta:
        model = Personal_info
        exclude = ('id', 'created', 'title', 'session_id')
        widgets = {
            'gender': forms.RadioSelect(attrs={'label_suffix': '', 'required': True}),
            'age': forms.Select(attrs={'class': 'form-select form-select-sm clabel'}),
            'country': forms.Select(attrs={'class': 'form-select form-select-sm clabel', 'required': True}),
            'education': forms.Select(attrs={'class': 'form-select form-select-sm clabel'}),
            
            'FK_9'  : forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'FK_10' : forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'FK_11' : forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'FK_12' : forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True})
        }
        labels = {
            'gender': 'Gender',
            'age': 'Age',
            'country': 'Country of residence',
            'education': 'Your highest completed education',

        # food knowledge
            'FK_9' : 'Compared with an average person, I know a lot about healthy eating',
            'FK_10': 'I think I know enough about healthy eating to feel pretty confident when choosing a recipe',
            'FK_11': 'I know a lot about how to evaluate the healthiness of a recipe',
            'FK_12': 'I do NOT feel very knowledgeable about healthy eating'
            #'FK_1': 'My diet is well-balanced and healthy',
            #'FK_2': 'The amount of sugar I get in my food is important',
            #'FK_3': 'I have the impression that I sacrifice a lot for my health',
            #'FK_4': 'My health does NOT depend on the foods I consume',
            #'FK_5': 'I am concerned about the quantity of salt that I get in my food',
            #'FK_6': 'It is important for me that my daily diet contains a lot of vitamins and minerals',
            #'FK_7': 'The healthiness of snacks makes no difference to me',
            #'FK_8': 'I do no avoid foods, even if they may raise my cholesterol'

        }

# class Ghs_fkForm(forms.ModelForm):
#     class Meta:
#         model = Ghs_fk
#         exclude = ('id','person','created','title','session_id')
#         widgets = {
#             # 'FK_1'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             # 'FK_2'  : forms.RadioSelect(attrs ={'label_suffix':'',}),
#             # 'FK_3'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             # 'FK_4'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             # 'FK_5'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             # 'FK_6'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             # 'FK_7'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             # 'FK_8'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             'FK_9'  : forms.RadioSelect(attrs={'label_suffix':'',}),
#             'FK_10' : forms.RadioSelect(attrs={'label_suffix':'',}),
#             'FK_11' : forms.RadioSelect(attrs={'label_suffix':'',}),
#             'FK_12' : forms.RadioSelect(attrs={'label_suffix':'',})
#         } 

#         labels = {
#             # 'FK_1' : 'The healthiness of food has little impact on my food choices',
#             # 'FK_2' : 'I am very particular about the healthiness of the food I eat',
#             # 'FK_3' : 'I eat what I like, and I do not worry much about the health of the food',
#             # 'FK_4' : 'It is important for me that my diet is low in fat',
#             # 'FK_5' : 'I always follow a healthy and balanced diet',
#             # 'FK_6' : 'It is important for me that my daily diet contains a lot of vitamins and minerals',
#             # 'FK_7' : 'The healthiness of snacks makes no difference to me',
#             # 'FK_8' : 'I do not avoid foods, even if they may raise my cholesterol',

#             # Items for subjective knowledge

#             'FK_9' : 'Compared with an average person, I know a lot about healthy eating',
#             'FK_10': 'I think I know enough about healthy eating to feel pretty confident when choosing a recipe',
#             'FK_11': 'I know a lot about how to evaluate the healthiness of a recipe',
#             'FK_12': 'I do NOT feel very knowledgeable about healthy eating'
#         }




likert_scale = [ 
('1','Strongly Disagree'),
('2','Disagree'),
('3','Neutral'),
('4','Agree'),
('5','Strongly Agree')
]
popularity_stars = [
    ('3.8','3 stars'),
    ('4','4 stars'),
    ('0','No preferences')
]

class FoodCategoryForm(forms.ModelForm):

    class Meta:
        model = FoodCategory
        exclude = ('id', 'created', 'person','session_id')
        widgets = {
            'category': forms.Select(attrs={'class': 'btn'}),
            'recipe_popularity':forms.RadioSelect(attrs={'label_suffix':''},choices=popularity_stars),
            'calories':forms.NumberInput(attrs={ 'placeholder':'min=200, max=1000'}),
            'recipe_size':forms.NumberInput(attrs={ 'placeholder':'min=1, max=10'}),
           # 'recipes_mood':forms.RadioSelect(attrs={'label_suffix':''},choices=likert_scale),
            'preparation_time':forms.NumberInput(attrs={ 'placeholder':'min=15, max=60'}),
            'n_ingredient':forms.NumberInput(attrs={'placeholder':'min=3, max=10'})

            
            }
        labels = {
            'category': 'Food Category',
            'recipe_popularity': 'I want recipes at least with ',
            'calories': 'Preferred amount of calories in my recipe',
            'recipe_size': 'The prefered number of servings in my recipes are',
            #'recipes_mood': 'I prefer to eat food that will enhance my mood',
            'preparation_time': 'The time I have availabe for cooking (in min)',
            'n_ingredient': 'The preferred number of ingredients in  my recipe'
        }


class ChoiceEvaluationForm(forms.ModelForm):
    class Meta:
        model = EvaluateChoices
        exclude = ('id', 'created', 'title','person','session_id')
        widgets = {

            # choice satisfaction
            'liked_recipes': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'prepare_recipes': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'fit_preference': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'know_many': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'recommend_recipe': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            
            # choice difficulty
            'many_to_choose': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'diet_restriction': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'easy_choice': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'choice_overwhelming': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),

            # Perceived effort
            'sys_time': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'unders_sys': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
            'many_actions': forms.Select(attrs={'class':'form-select form-select-sm clabel','required':True}),
        }
        labels = {
            
            # Choice satisfaction 
            'liked_recipes':"I like the recipe I've chosen",
            'prepare_recipes':"I think I will prepare the recipe I've chosen",
            'fit_preference': 'The chosen recipe fits my preferences',
            'know_many': 'I know many recipes that I like more than the one I have chosen',
            'recommend_recipe': 'I would recommend the chosen recipe to others',
            
            # Choice difficulty 
            'many_to_choose': 'I changed my mind several times before making a decision ',
            'diet_restriction': 'Do you have any dietary restrictions',
            'easy_choice': 'It was easy to make this choice ',
            'choice_overwhelming': 'Making a choice was overwhelming ',

            # Perceived effort
            'sys_time':'The system takes up a lot of time',
            'unders_sys':'I quickly understood the functionalities of the system',
            'many_actions':'Many actions were required to use the system'
        }













