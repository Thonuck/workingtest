from flask import render_template, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Starter, Base

def hello_world():
    return render_template("index.html", title="Workingtest Planer")

def starter():
    if request.method == 'POST':
        print("post")
        return render_template("starter.html", title="Starter")
    engine = create_engine('sqlite:///starters.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    starters = session.query(Starter).all()
    session.close()
    print(starters)
    return render_template("starter.html", title="Starter", starters=starters)

@app.route('/')
def hello_world():
    return render_template("index.html", title="Workingtest Planer")