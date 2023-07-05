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

def replace_column_value(dataframe, column_name, string1, string2):
    new_dataframe = dataframe.copy()
    new_dataframe[column_name] = new_dataframe[column_name].replace(string1, string2)
    return new_dataframe

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

class Recip(FlaskForm):
    instru = StringField()
    tetil = StringField()
    submit4 = SubmitField('Submit')

class Edit(FlaskForm):
    instruch = StringField()
    titel = StringField()
    submit5 = SubmitField('Submit')

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
    recipes_dataframe = replace_column_value(recipes_dataframe,"is_edit","one","zero")
    recipes_dataframe = replace_column_value(recipes_dataframe,"is_edit","two","one")

    all_items = total_list_dataframe["item"].to_list()
    shops = dataframe_to_dict(total_list_dataframe,"item","shop")
    shopping_list = shopping_list_dataframe["item"].to_list()
    shopping_list_indicies = list(shopping_list_dataframe.index.values)
    recipes_indicies = list(recipes_dataframe.index.values)

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

    reci_form = Recip()
    if (reci_form.validate_on_submit() and reci_form.submit4.data):
        if((len(reci_form.instru.data)>0) and (len(reci_form.tetil.data)>0)):
            newer_reci = reci_form.instru.data
            newer_title = reci_form.tetil.data
            reci_form.instru.data = ""
            reci_form.tetil.data = ""
            next_index = get_next_index(recipes_dataframe)
            row = pd.DataFrame({"itemID": next_index, "instructions": newer_reci,"is_edit":"zero", "title": newer_title},index=[next_index])
            row.set_index('itemID', inplace=True)
            recipes_dataframe = pd.concat([recipes_dataframe,row], axis=0)
            recipes_indicies = list(recipes_dataframe.index.values)
            recipes_dataframe.to_sql("recipe", con=engine, if_exists="replace",index_label="itemID")
        else:
            reci_form.instru.data = ""
            reci_form.tetil.data = ""


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

    personal_remove_ids = []
    personal_edit_ids = []
    for instruction in recipes_dataframe["instructions"]:
        personal_remove_id = ("_").join(instruction.split(" "))
        personal_remove_ids.append(personal_remove_id)
        personal_edit_id = ("v").join(instruction.split(" "))
        personal_edit_ids.append(personal_edit_id)

    target = "None"
    target_title = "None"
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

        for specific_remove_id in personal_remove_ids:
            if(request.form.get(specific_remove_id)):
                actual_remove_id = (" ").join(specific_remove_id.split("_"))
                recipes_dataframe.drop(recipes_dataframe[recipes_dataframe["instructions"] == actual_remove_id].index.values, inplace=True)
                recipes_indicies = list(recipes_dataframe.index.values)
                recipes_dataframe.to_sql("recipe", con=engine, if_exists="replace", index_label="itemID")

        for specific_edit_id in personal_edit_ids:
            if(request.form.get(specific_edit_id)):
                target = specific_edit_id
                recipes_dataframe.loc[recipes_dataframe[recipes_dataframe["instructions"] == (" ").join(target.split("v"))].index.values,"is_edit"] = "two"
                target_title = list(recipes_dataframe.loc[recipes_dataframe[recipes_dataframe["instructions"] == (" ").join(target.split("v"))].index.values,"title"])[0]
                recipes_dataframe.to_sql("recipe", con=engine, if_exists="replace", index_label="itemID")

    edi_form = Edit()
    if (edi_form.validate_on_submit() and edi_form.submit5.data):
        if((len(edi_form.instruch.data)>0) and (len(edi_form.titel.data)>0)):
            changed = edi_form.instruch.data
            changed_title = edi_form.titel.data
            index_to_change = recipes_dataframe[recipes_dataframe["is_edit"] == "one"].index.values
            recipes_dataframe.loc[index_to_change,"instructions"] = changed
            recipes_dataframe.loc[index_to_change,"title"] = changed_title
            recipes_dataframe.to_sql("recipe", con=engine, if_exists="replace", index_label="itemID")
    edi_form.instruch.data = (" ").join(target.split("v"))
    edi_form.titel.data = target_title

    if(len(recipes_indicies) > 0):
        recipe_string = " "
        count = 0
        for instruction in recipes_dataframe["instructions"]:
            recipe_index = recipes_indicies[count]
            title = recipes_dataframe.loc[recipe_index,"title"]
            personal_remove_id = ("_").join(instruction.split(" "))
            personal_edit_id = ("v").join(instruction.split(" "))
            if(recipes_dataframe.loc[recipe_index,"is_edit"] == "two"):
                recipe_string = recipe_string + '<div id="recipe"><form method="POST"><fieldset><legend>Edit Recipe</legend><label for="titler">Title:</label> {{ edi_form.hidden_tag() }} {{ edi_form.titel(class="form-control", autocomplete="off") }} </br></br> <label for="recr">Recipe:</label> {{ edi_form.instruch(class="form-control", autocomplete="off") }} </br></br> {{ edi_form.submit5() }}</fieldset></form></div>'
            else:
                recipe_string = recipe_string + '<div id="recipe"><b>' + title +"</b></br></br>"+ instruction + "</br></br><form method='POST'><input type='submit' value='remove' name='"+personal_remove_id+"'/>   <input type='submit' value='edit' name='"+personal_edit_id+"'/></form></div></br>"  
            count = count + 1
    else:
        recipe_string = " "

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

    option_string = " "
    for item in all_items:
        option_string = option_string + '<option value="'+item+'">'

    first_layer = []
    first_layer.append(aldistring)
    first_layer.append(colesstring)
    first_layer.append(option_string)
    first_layer.append(option_string)
    first_layer.append(recipe_string)

    return render_template_string(stringinserter("@",page1,first_layer), kart_form=kart_form, add_form=add_form, remove_form=remove_form, reci_form=reci_form, edi_form=edi_form)