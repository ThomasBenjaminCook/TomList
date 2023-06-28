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

@app.route("/")
def data():
    return page1