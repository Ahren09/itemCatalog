from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Kind, Item
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)



@app.route('/')
@app.route('/catalog/')
def showCatalog():
    session = DBSession()
    kinds = session.query(Kind).order_by(asc(Kind.name))
    return render_template('catalog.html', kinds=kinds)

@app.route('/catalog/<kindName>/items/')
@app.route('/catalog/<kindName>/')
def showAllItems(kindName):
    session = DBSession()
    kinds = session.query(Kind).order_by(asc(Kind.name))
    kind = session.query(Kind).filter_by(name=kindName).one()
    items = session.query(Item).filter_by(kind=kind).all()
    return render_template('allItems.html', kinds=kinds, kind=kind, items=items)

@app.route('/catalog/<kindName>/<itemName>/')
def showOneItem(kindName, itemName):
    session = DBSession()
    kind = session.query(Kind).filter_by(name=kindName).one()
    item = session.query(Item).filter_by(name=itemName).one()
    return render_template('oneItem.html', kind=kind, item=item)

@app.route('/catalog/<kindName>/new/', methods=['GET','POST'])
def newItem(kindName):
    session = DBSession()
    kinds = session.query(Kind).order_by(asc(Kind.name))
    kind = session.query(Kind).filter_by(name=kindName).one()
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],description=request.form['description'])
        newItemKindName = request.form.get('kind')
        newItem.kind = session.query(Kind).filter_by(name=newItemKindName).one()
        session.add(newItem)
        session.commit()
        flash("Item Successfully Created!")
        return redirect(url_for('showOneItem', kindName=newItem.kind.name, itemName=newItem.name))
    else:
        return render_template('newItem.html', kinds=kinds, kind=kind)

@app.route('/catalog/<itemName>/edit/', methods=['GET','POST'])
def editItem(itemName):
    session = DBSession()
    kinds = session.query(Kind).order_by(asc(Kind.name))
    item = session.query(Item).filter_by(name=itemName).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['kind']:
            itemKindName = request.form.get('kind')
            item.kind = session.query(Kind).filter_by(name=itemKindName).one()
        session.add(item)
        session.commit()
        flash("Item Successfully Edited!")
        return redirect(url_for('showOneItem', kindName=item.kind.name, itemName=item.name))
    else:
        return render_template('editItem.html', kinds=kinds, item=item)

@app.route('/catalog/<itemName>/delete/', methods=['GET','POST'])
def deleteItem(itemName):
    session = DBSession()
    item = session.query(Item).filter_by(name=itemName).one()
    kindName = item.kind.name
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showAllItems', kindName=kindName))
    else:
        return render_template('deleteItem.html', item=item)



if __name__=='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port=8000)