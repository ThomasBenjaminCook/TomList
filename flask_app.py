import pandas as pd
import statistics
import random
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string
from pathlib import Path
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

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

def get_next_index(dataframe):
    if(len(list(dataframe.index.values))>=1):
        next_index = int(list(dataframe.index.values)[-1])+1
    else:
        next_index = 0
    return(next_index)

class Kart(FlaskForm):
    itemer = StringField()
    submit1 = SubmitField('Submit')

class Adder(FlaskForm):
    itemire = StringField()
    shopper = StringField()
    submit2 = SubmitField('Submit')

class Remover(FlaskForm):
    itemerem = StringField()
    submit3 = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u3ygfr7evyguyg87y6fuev$%^&^%$'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ThomasAppMaker",
    password="P_R5nvjG5DV4Vd6",
    hostname="ThomasAppMaker.mysql.pythonanywhere-services.com",
    databasename="ThomasAppMaker$default",
)
engine = create_engine(SQLALCHEMY_DATABASE_URI)

@app.route("/", methods = ["GET","POST"])
def data():

    shopping_list_dataframe = pd.read_sql_table("shopping_list", con=engine, index_col="itemID")
    total_list_dataframe = pd.read_sql_table("all_items", con=engine, index_col="itemID")
    recipes_dataframe = pd.read_sql_table("recipe", con=engine, index_col="itemID")

    all_items = total_list_dataframe["item"].to_list()
    shops = dataframe_to_dict(total_list_dataframe,"item","shop")
    shopping_list = shopping_list_dataframe["item"].to_list()
    shopping_list_indicies = list(shopping_list_dataframe.index.values)

    first_layer = []

    kart_form = Kart()
    if (kart_form.validate_on_submit() and kart_form.submit1.data):
        if(kart_form.itemer.data in all_items):
            selected_item = kart_form.itemer.data
            kart_form.itemer.data = ""
            shopping_list.append(selected_item)
            next_index = get_next_index(shopping_list_dataframe)
            shopping_list_dataframe.loc[next_index]=selected_item
            shopping_list_indicies.append(next_index)
            shopping_list_dataframe.to_sql("shopping_list", con=engine, if_exists="replace")
        else:
            kart_form.itemer.data = ""

    
    add_form = Adder()
    if (add_form.validate_on_submit() and add_form.submit2.data):
        if((len(add_form.itemire.data) >= 2) and (len(add_form.shopper.data)>1) and (add_form.itemire.data not in all_items)):
            newer_item = add_form.itemire.data
            add_form.itemire.data = ""
            corresponding_shop = add_form.shopper.data
            add_form.shopper.data = ''
            next_index = get_next_index(total_list_dataframe)
            row = pd.DataFrame({"itemID": next_index, "item": newer_item, "shop" : corresponding_shop},index=[next_index])
            row.set_index('itemID', inplace=True)
            total_list_dataframe = pd.concat([total_list_dataframe,row], axis=0)
            total_list_dataframe.to_sql("all_items", con=engine, if_exists="replace",index_label="itemID")
            all_items = total_list_dataframe["item"].to_list()
            shops = dataframe_to_dict(total_list_dataframe,"item","shop")
        else:
            add_form.itemire.data = ""


    remove_form = Remover()
    if (remove_form.validate_on_submit() and remove_form.submit3.data):
        if(remove_form.itemerem.data not in shopping_list):
            thing_to_remove = remove_form.itemerem.data
            remove_form.itemerem.data = ""
            total_list_dataframe.drop(total_list_dataframe[total_list_dataframe["item"] == thing_to_remove].index.values, inplace=True)
            total_list_dataframe.to_sql("all_items", con=engine, if_exists="replace",index_label="itemID")
            all_items = total_list_dataframe["item"].to_list()
            shops = dataframe_to_dict(total_list_dataframe,"item","shop")
        else:
            remove_form.itemerem.data = ""

    weird_ids = []
    count = 0
    while count < len(shopping_list):
        item = shopping_list[count]
        target_index = shopping_list_indicies[count]
        if(shops[item] == "ALDI"):
            weird_id = "ALDI_"+str(target_index)
        if(shops[item] == "Coles"):
            weird_id = "Coles_"+str(target_index)
        weird_ids.append(weird_id)
        count = count + 1

    if request.method == "POST":
        count = 0
        while count < len(shopping_list):
            weird_id = weird_ids[count]
            item = shopping_list[count]
            if(request.form.get(weird_id)):
                shopping_list_dataframe.drop([int(weird_id.split("_")[-1])], axis=0, inplace=True)
                shopping_list = shopping_list_dataframe["item"].to_list()
                shopping_list_indicies = list(shopping_list_dataframe.index.values)
                shopping_list_dataframe.to_sql("shopping_list", con=engine, if_exists="replace")
            count = count + 1

    aldistring = " "
    colesstring = " "
    count = 0
    while count < len(shopping_list):
        item = shopping_list[count]
        target_index = shopping_list_indicies[count]
        if(shops[item] == "ALDI"):
            aldistring = aldistring + '<input type="submit" value="'+item+'" name="'+weird_ids[count]+'"/></br></br>'
        if(shops[item] == "Coles"):
            colesstring = colesstring + '<input type="submit" value="'+item+'" name="'+weird_ids[count]+'"/></br></br>'
        count = count + 1

    first_layer.append(aldistring)
    first_layer.append(colesstring)

    option_string = " "

    for item in all_items:
        option_string = option_string + '<option value="'+item+'">'

    first_layer.append(option_string)
    first_layer.append(option_string)

    recipe_string = " "

    for instruction in recipes_dataframe["instructions"]:
        recipe_string = recipe_string + '<div id="recipe">' + instruction + "</br></br><input type='submit' value='remove'/></br></br><input type='submit' value='edit'/></br></br></div></br>"

    first_layer.append(recipe_string)

    return render_template_string(stringinserter("@",page1,first_layer), kart_form=kart_form, add_form=add_form, remove_form=remove_form)