from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from Application.db import get_db
import json


class BrandManagerSchema(Schema):
    brand_name = fields.Str()
    manager_email = fields.Str()


class BrandManager:
    def __init__(self, brand_name, manager_email):
        self.id = id
        self.brand_name = brand_name
        self.manager_email = manager_email


bp = Blueprint('brand-manager', __name__, url_prefix='/brand-manager')


def addBrandManager(cur: Cursor, cu: BrandManager):
    cur.execute(
        'INSERT INTO brand_manager(brand_name, manager_email) VALUES (?, ?)',
        (cu.brand_name, cu.manager_email))


@bp.route('/byEmail', methods=['GET'])
@cross_origin()
def getByEmail():
    db = get_db().cursor()
    rows = db.execute(
        'SELECT * FROM brand_manager where manager_email=?', (request.args.get(
            'manager_email'),)
    ).fetchall()
    jsonRes = []
    schema = BrandManagerSchema()
    for row in rows:
        jsonRes.append(schema.dump(BrandManager(row[0], row[1])))
    return json.dumps(jsonRes)


@bp.route('', methods=['POST'])
@cross_origin()
def addOne():
    cur = get_db().cursor()
    addBrandManager(cur, BrandManager(request.json.get(
        'brand_name'), request.json.get('manager_email')))
    return {}
