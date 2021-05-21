from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


tutorials = [
    {
        'id': 1,
        'first name': 'Ivan',
        'last name': 'Ivanov',
        'mail':'i@mail.ru',
        'transaction':500,
        'data': '2020-02-18'
    },
    {
        'id': 2,
        'first name': 'Ivan_2',
        'last name': 'Ivanov_2',
        'mail':'i@mail.ru',
        'transaction':9520,
        'data': '2020-05-18'
    },
    {
        'id': 3,
        'first name': 'Ivan',
        'last name': 'Ivanov',
        'mail':'i@mail.ru',
        'transaction':10000,
        'data': '2021-05-18'
    }
]



@app.route('/tutorials', methods=['GET'])
def get_list():
    users = User.query.all()
    serialized = []
    for u in users:
        serialized.append({
            'id': u.id,
            'first name': u.first_name,
            'last name': u.last_name,
            'mail': u.mail,
            'transaction': u.transaction,
            'data': u.data
        })
    return jsonify(serialized)


@app.route('/tutorials', methods=['POST'])
def update_list():
    new_one = User(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': User.id,
        'first name': User.first_name,
        'last name': User.last_name,
        'mail': User.mail,
        'transaction': User.transaction,
        'data': User.data
    }
    return jsonify(serialized)


@app.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
def update_tutorial(tutorial_id):
    item = User.query.filter(User.id == tutorial_id).first()
    params = request.json
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': User.id,
        'first name': User.first_name,
        'last name': User.last_name,
        'mail': User.mail,
        'transaction': User.transaction,
        'data': User.data
    }
    return serialized


@app.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
def delete_tutorial(tutorial_id):
    item = User.query.filter(User.id == tutorial_id).first()
    if not item:
        return {'message': 'No tutorials with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
