import pandas
import statistics
import random
from datetime import datetime, timedelta
from flask import Flask, request, redirect, make_response
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy

THIS_FOLDER = Path(__file__).parent.resolve()

app = Flask(__name__)

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

@app.route("/")
def data():

    all_items = ["milk","bread","cheese","chocolate","chia"]
    shops = {"milk":"ALDI","bread":"ALDI","cheese":"ALDI","chia":"Coles","chocolate":"Coles"}
    shopping_list = ["milk","chia","bread"]

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