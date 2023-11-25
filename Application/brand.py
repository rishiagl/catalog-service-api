import os
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields
from Application.brand_managers import BrandManager, addBrandManager

from Application.db import get_db
from Application.exception import InvalidAPIUsage


class BrandSchema(Schema):
    name = fields.Str()
    logo_link = fields.Str()
    country_of_origin = fields.Str()
    owner_email = fields.Str()


class Brand:
    def __init__(self, name, logo_link, country_of_origin, owner_email):
        self.name = name
        self.logo_link = logo_link
        self.country_of_origin = country_of_origin
        self.owner_email = owner_email

    def __repr__(self):
        return "<Brand(name={self.name!r})>".format(self=self)


bp = Blueprint('brand', __name__, url_prefix='/brand')


def addBrand(cursor: Cursor, c: Brand):
    
    try:
        cursor.execute(
        'INSERT INTO Brand(name, logo_link, country_of_origin, owner_email) VALUES (?, ?, ?, ?,) returning name',
        (c.name, c.logo_link, c.country_of_origin, c.owner_email))
        last_insert_name = cursor.fetchone()[0]
    except:
        raise InvalidAPIUsage("Database Error Occurred")
    return last_insert_name


def getBrandByName(cursor: Cursor, name: str):
    try:
        cursor.execute(
        'SELECT * FROM brand where name=%s', (name,)
        )
        row = cursor.fetchone()
        if row == None:
            return 
    except:
        raise InvalidAPIUsage("Database Error Occurred")
    return Brand(row[0], row[1], row[2], row[3])


@bp.route('', methods=['POST'])
@cross_origin()
def addOne():
    
    try:
        cur = get_db().cursor()
        cur.execute('BEGIN')
        name = addBrand(cur, Brand(request.json.get('name'), request.json.get(
            'logo_link'), request.json.get('country_of_origin'), request.json.get('owner_email')))
        addBrandManager(cur, BrandManager(0, name, request.json.get(
        'name'), request.json.get('owner_email')))
        cur.execute('COMMIT')
    except:
        raise InvalidAPIUsage("Database Error Occurred")
    return {}


@bp.route('/<name>', methods=['GET'])
@cross_origin()
def getByname(name):
    cur = get_db().cursor()
    Brand = getBrandByName(cur, name)
    return BrandSchema().dump(Brand)
