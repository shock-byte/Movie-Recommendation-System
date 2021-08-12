# Importing necessary libraries 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from progress.bar import IncrementalBar
from easygui import *
import easygui as gui
import pandas as pd
import numpy as np
import sys
# maxing out numpy arrray display size for easygui display 
np.set_printoptions(threshold=sys.maxsize)
# as its a relatively big dataset, the initial load will take about 30sec
# depending on your pc , thus an indication of loading is appopriate 
progress_bar = IncrementalBar('Loading Movie Database...', max=1)
for i in range(1):
    # reading in csv files
    df_tags = pd.read_csv("tags.csv", usecols = [1,2])
    df_movies = pd.read_csv("movies.csv")
    df_ratings = pd.read_csv("ratings.csv", usecols = [1,2])
    
    # merging columns from seperate dataframes into new dataframe
    df_1 = pd.merge(df_movies ,df_ratings, on='movieId', how='outer')
    # filling NaN rating values with mean rating
    df_1['rating'] = df_1['rating'].fillna(df_1['rating'].mean()) 
    # gouping df rows by average rating per movie
    df_1 = pd.DataFrame(df_1.groupby('movieId')['rating'].mean().reset_index().round(1))
    # adding title and genres column to df
    df_1['title'] = df_movies['title']
    df_1['genres'] = df_movies['genres']
    
    progress_bar.next()
    # progress bar completion on successful load of dataset 
progress_bar.finish()
def which_way():
    '''
    First function of program which gets executed when running the program. 
    This functions as a cross roads, either you choose to search movies by
    tag or by genre. Based on user choice, user gets directed to next window.
    
    '''
    
    # defining easygui choicebox parameters
    msg = "Choose an option:"
    title = "Main Menu"
    choices = ["Search recommended movies by genre:","Search recommended movies by tag:"]
    fieldValues = choicebox(msg,title, choices)
    
    # fieldValues variable is the user input which gets returned from the gui
    # conditional statement to guide user to the next interface based on input
    if fieldValues == "Search recommended movies by genre:":
        genre_entry()
    
    elif fieldValues == "Search recommended movies by tag:":
        tag_entry()
def field_check(msg, title, fieldNames):
    '''
    This function checks for missing user input values in the multienterbox
    and returns the user input as fieldValues variable
    
    Parameters:
    
    msg, title and fieldnames of the multi-enterbox GUI
    
    '''
    
    fieldValues = multenterbox(msg, title, fieldNames)
    
    # Loop with conditionals to make sure that none of the user input 
    # fields are left blank
    while 1:
        if fieldValues is None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "":
            break # if no empty fields found, proceed with next codeblock
        # Saving user input as list in fieldValues variable
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    
    return fieldValues
def tag_entry():
    ''' 
    This function defines the easygui multenterbox parameters and calls
    on the field_check functions, if field/user input is retrieved function
    calls on similarity test and if a match is not found user gets returned 
    to the same window  
    '''
    
    # defining easygui multenterbox parameters
    msg = "Enter movie tag for example: Movie name | Actor name  \nIf tag not found you will be returned to this window"
    title = 'Search by tag'                        
    fieldNames = ["Tag"]
    
    # calling on field_check() to check for missing user input and to
    # save user input as fieldValues variable
    fieldValues = field_check(msg, title, fieldNames)
    
    # If user input is not empty, slice list element and save in variable
    if fieldValues != None:
        global user_input_2
        user_input_2 = fieldValues[0]
        
        # here we call on a function which basically tests for string
        # similarity. if user press cancel, user gets returned to main menu 
        similarity_test2(user_input_2)
    else:
        which_way()
def tag():
    '''
    This function adds all tag-matched movies to pandas dataframe,
    alter the dataframe for correct easygui display by dropping some 
    columns, resetting df index, merging df's and sorting movies to display
    only movies rated >= 2.5 , it also casts the final df columns to lists
    and rearrange them in a numpy array for easygui display.  
    '''
    
    # append tag matched movies as dataframe object
    final_1 = []
    for i in final_2:
        final_1.append(df_tags.loc[df_tags['tag'].isin(i)])
    
    # reset df index, drop index column as well as duplicate entries
    lst = final_1[0]
    lst = lst.reset_index()
    lst.drop('index', axis=1, inplace=True)
    lst = lst.drop_duplicates(subset='movieId')
# merge movieId with movie names and genres + drop tag and movieId column
    df = pd.merge(lst, df_1, on='movieId', how='left')
    df.drop('tag', axis=1, inplace=True)
    df.drop('movieId', axis=1, inplace=True)
# sort movies by ratings, display only movies rated above or = 2.5 rating
    data = df.sort_values(by='rating', ascending=False)
    data = data[data['rating'] >= 2.5]
    heading = [] # add column names as first dataframe row for easygui display
    heading.insert(0, {'rating': 'Rating', 'title': '----------Title',
     'genres': '----------Genre'})
    data = pd.concat([pd.DataFrame(heading), data], ignore_index=True, sort=True)
    
    # casting dataframe columns to lists
    rating = data['rating'].tolist()
    title = data['title'].tolist()
    genres = data['genres'].tolist()
    
    # compiling numpy array from dataframe column lists for easygui display
    data = np.concatenate([np.array(i)[:,None] for i in [rating,title,genres]], axis=1)
    data = str(data).replace('[','').replace(']','')
    
    # displaying matched movies to user
    gui.codebox(msg='Movies filtered by tag returned from database:',
    text=(data),title='Movies')
    
    which_way()
def genre_entry():
    ''' 
    This function defines the easygui multenterbox parameters and calls
    on the field_check functions, if field/user input is retrieved function
    calls on similarity test and if a match is not found user gets returned 
    to the same window  
    '''
    # defining easygui multenterbox parameters
    msg = "Enter movie genre for example: Mystery | Action | Comedy | Horror \nIf genre not found you will be returned to this window"
    title = "Search by genre"
    fieldNames = ["Genre"]
    
    # calling on field_check() to check for missing user input and to
    # save user input as fieldValues variable
    fieldValues = field_check(msg, title, fieldNames)
    
    # If user input is not empty, slice list element and save in variable
    if fieldValues != None:
        global user_input
        user_input = fieldValues[0]
        
    # here we call on a function which basically tests for string
    # similarity. if user press cancel, user gets returned to main menu 
        similarity_test1(user_input)
    else:
        which_way()
def genre():
    '''
    This function adds all genre-matched movies to pandas dataframe,
    alter the dataframe for correct easygui display by dropping some 
    columns, resetting df index, merging df's and sorting movies to display
    only movies rated >= 2.5 , it also casts the final df columns to lists
    and rearrange them in a numpy array for easygui display.  
    '''
    
    # append genre matched movies as dataframe object
    final_1 = []
    for i in final:
        final_1.append(df_movies.loc[df_movies['genres'].isin(i)])
    
    # reset df index, drop index columns as well as duplicate entries
    lst = final_1[0]
    lst = lst.reset_index()
    lst.drop('index', axis=1, inplace=True)
    lst.drop('title', axis=1, inplace=True)
    lst.drop('genres', axis=1, inplace=True)
    lst = lst.drop_duplicates(subset='movieId')
    
    # merge movieId with movie names, rating and genres + drop index, title and genres column
    df = pd.merge(lst, df_1, on='movieId', how='left')
    
    # sort movies by ratings, display only movies rated above or = 2.5 rating
    data = df.sort_values(by='rating', ascending=False)
    data.drop('movieId', axis=1, inplace=True)
    data = data[data['rating'] >= 2.5]
    heading = [] # add column names as first dataframe row for easygui display
    heading.insert(0, {'rating': 'Rating', 'title': '----------Title',
     'genres': '----------Genre'})
    data = pd.concat([pd.DataFrame(heading), data], ignore_index=True, sort=True)
    
    # casting dataframe columns to lists
    rating = data['rating'].tolist()
    title = data['title'].tolist()
    genres = data['genres'].tolist()
    
    # compiling numpy array from dataframe column lists for easygui display
    data = np.concatenate([np.array(i)[:,None] for i in [rating,title,genres]], axis=1)
    data = str(data).replace('[','').replace(']','')
    
    # displaying matched movies to user
    gui.codebox(msg='Movies filtered by genre returned from database:',
    text=(data),title='Movies')
    
    which_way()
def similarity_test1(user_input):
    '''
    This function tests for string similarity by matching user input
    to movies genres, match/es > 90% gets saved in variable which
    then gets passed on to genre function for database match and
    return unless no match is found
    '''
    # saving movie genre/s as test base and user input to test for 
    genre_list = df_movies['genres'].unique()
    query = user_input
    choices = genre_list 
    # here fuzzywuzzy does its magic to test for similarity
    output = process.extract(query, choices)
    
    # saving returned matches in variable and passing it on to next function
    global final
    final = [i for i in output if i[1] > 90]
    
    # if no match of > 90%  is found, return to genre entry window for retry
    if final == []:
        genre_entry()
    else:
        genre()
def similarity_test2(user_input_2):
    '''
    This function tests for string similarity by matching user input
    to movie tags, match/es > 90% gets saved in variable which
    then gets passed on to tag function for database match and
    return unless no match is found
    '''
    # saving movie tag as test base and user input to test for
    tag_list = df_tags['tag'].unique()
    query = user_input_2
    choices = tag_list 
    # here fuzzywuzzy does its magic to test for similarity
    output = process.extract(query, choices)
    
    # saving returned matches in variable and passing it on to next function
    global final_2
    final_2 = [i for i in output if i[1] > 90]
    
    # if no match of > 90%  is found, return to tag entry window for retry
    if final_2 == []:
        tag_entry()
    else:
        tag()
if __name__ == '__main__':
    which_way()