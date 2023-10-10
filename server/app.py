from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import desc, asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages = Message.query.order_by(asc("created_at")).all()
        messages_dict = [message.to_dict() for message in messages]

        return make_response(messages_dict, 200)
    
    elif request.method == "POST":
        new_message = Message(
            body = request.json["body"],
            username = request.json["username"]
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if request.method == "PATCH":
        for key in request.json:
            setattr(message, key, request.json[key])
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(), 202)
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        
        return make_response({}, 204)

if __name__ == '__main__':
    app.run(port=5555)
