import pandas as pd
import statistics
import random
from datetime import datetime, timedelta
from flask import Flask, request, redirect, make_response
from pathlib import Path
from sqlalchemy import create_engine

THIS_FOLDER = Path(__file__).parent.resolve()

with open(THIS_FOLDER / "page1.txt") as f:
    page1 = f.readlines()
page1 = (" ").join(page1)

def stringinserter(tag,string,insertables):
    array = string.split(tag)
    outputarray = []
    for x in range(len(array)):
        outputarray.append(array[x])
        if x < len(insertables):
            outputarray.append(insertables[x])
    return(("").join(outputarray))

def dataframe_to_dict(dataframe, target_col_index,target_col_val):
    dictionary = {}
    count = 0
    while count < len(dataframe[target_col_index].to_list()):
        dictionary[dataframe[target_col_index].to_list()[count]] = dataframe[target_col_val].to_list()[count]
        count = count + 1
    return(dictionary)

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ThomasAppMaker",
    password="P_R5nvjG5DV4Vd6",
    hostname="ThomasAppMaker.mysql.pythonanywhere-services.com",
    databasename="ThomasAppMaker$default",
)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

@app.route("/")
def data():

    shopping_list_dataframe = pd.read_sql_table("shopping_list", con=engine, index_col="itemID")
    total_list_dataframe = pd.read_sql_table("all_items", con=engine, index_col="itemID")

    dataframe_to_dict

    all_items = total_list_dataframe["item"].to_list()
    shops = dataframe_to_dict(total_list_dataframe,"item","shop")
    shopping_list = shopping_list_dataframe["item"].to_list()

    first_layer = []

    coles_string = " "
    ALDI_string = " "

    for item in shopping_list:
        if(shops[item] == "ALDI"):
            ALDI_string = ALDI_string + '<input type="submit" value='+item+'><br><br>'
        else:
            coles_string = coles_string + '<input type="submit" value='+item+'><br><br>'

    first_layer.append(ALDI_string)
    first_layer.append(coles_string)

    option_string = " "

    for item in all_items:
        option_string = option_string + '<option value='+item+'>'

    first_layer.append(option_string)
    first_layer.append(option_string)

    return (stringinserter("@",page1,first_layer))