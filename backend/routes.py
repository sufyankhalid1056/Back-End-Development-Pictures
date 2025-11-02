from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for x in data:
            if x["id"] == id:
                return jsonify(x), 200
        
        return {'Message': 'Not Found'}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    rec_data = request.json

    if not rec_data:
        return {"message": "Invalid input parameter"}, 422

    pic = {
        "id": rec_data.get("id"),
        'pic_url': rec_data.get('pic_url'),
        'event_country': rec_data.get('event_country'),
        'event_state': rec_data.get('event_state'),
        'event_city': rec_data.get('event_city'),
        'event_date': rec_data.get('event_date'),
    }

    try:
        for x in data:
            if x['id'] == pic['id']:
                return {"Message": f"picture with id {pic['id']} already present"}, 302
        data.append(pic)
        return jsonify(pic), 201
    except NameError:
        return {"Nessage": "data not defined"}, 500

    
    
    return {"Message": "Created"}, 201



######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    rec_data = request.json

    if not rec_data:
        return {"message": "Invalid input parameter"}, 422

    pic = {
        "id": rec_data.get("id"),
        'pic_url': rec_data.get('pic_url'),
        'event_country': rec_data.get('event_country'),
        'event_state': rec_data.get('event_state'),
        'event_city': rec_data.get('event_city'),
        'event_date': rec_data.get('event_date'),
    }

    try:
        for x in data:
            if x['id'] == pic['id']:
                x['id'] = pic['id']
                x['pic_url'] = pic['pic_url']
                x['event_country'] = pic['event_country']
                x['event_state'] = pic['event_state']
                x['event_city'] = pic['event_city']
                x['event_date'] = pic['event_date']
                return jsonify(x), 200
        return {"message": "picture not found"}, 404
    except NameError:
        return {"Nessage": "data not defined"}, 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
     if data:
        for x in data:
            if x['id'] == id:
                data.remove(x)
                return {'Message': ''}, 204
        
        return {'Message': 'picture not Found'}, 404
