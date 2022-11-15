import pandas as pd
import numpy as np
import random


def stratified_data(file_path):
    """
    @type  file_path: string
    @param file_path: file pathway to the data one wants stratified/randomized
    return: boolean; true if stratified/randomized was a success and false otherwise
    output: updated file with 24 random entries
    """
    data = pd.read_csv(file_path)
    # Updating the data so we only keep clips with a duration of 60 seconds
    data = data[data.get('Duration') > 60]

    sifting = data.groupby("AudioMothID").count().get("AudioMothCode").reset_index()
    to_keep = sifting[sifting.get("AudioMothCode") >= 24].get("AudioMothID").to_numpy()

    # Once again updating data, so it only has audiomoths that have 24 clips
    data = data.loc[data["AudioMothID"].isin(to_keep)]

    # Collecting all of the hours and adding a column for those hours
    # Makes it easier to randomly get one of each hour
    hours = []
    for i in range(len(data)):
        hours.append(data.get("StartDateTime").iloc[i][11:13])

    data["Hours"] = hours

    # Important to reset the indexes so that we can ensure the index is within the
    # size of the table
    data.reset_index()

    possible_times = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
                      "16", "17", "18", "19", "20", "21", "22", "23"]
    list_of_possible = []

    # Creating a list of random indexes and using them to create a new file of 24 audios
    for time in possible_times:
        indexes = data.index[data.get('Hours') == time].tolist()
        list_of_possible.append(random.choice(indexes))

    new = data.loc[list_of_possible].reset_index().drop(columns="Hours")
    new.to_csv("Peru_2019_AudioMoth_Data_Stratified")

    return stratified_data_helper(new)


def stratified_data_helper(file):
    """
    @type file: string
    @param file: file we want to check has been stratified/randomized correctly
    @return: boolean, true if the file meets the requirements: size of 24, clips are 60 seconds long
    """
    #Making sure all the elements are 60 seconds long
    holder = False
    for elem in file.get("Duration").to_numpy():
        if elem < 60:
            break
        else:
            holder = True

    #Checking that the new file has 24 elements
    if len(file) == 24 and holder:
        return True

    #Will return false if it was not successful
    return False
