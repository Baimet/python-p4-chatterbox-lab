from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()

    response = jsonify([message.to_dict() for message in messages])
    return make_response(response, 200)
    

@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    message = Message.query.get_or_404(id) # Retrieve the message or return a 404 error if not found

    response = jsonify(message.to_dict())
    return make_response(response, 200)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json() # Extract JSON data from request body
    new_message = Message(body=data['body'], username=data['username'])

    # Add the new message to the database
    db.session.add(new_message)
    db.session.commit()

    # Respond with the newly created message
    response = jsonify(new_message.to_dict())
    return make_response(response, 201)  # Status 201 Created

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)  # Get the message or 404
    data = request.get_json() # Extract JSON data from request body

    # Update the body of the message
    if 'body' in data:
        message.body = data['body']

    # Save the updated message
    db.session.commit()

    # Respond with the updated message
    response = jsonify(message.to_dict())
    return make_response(response, 200)  # Status 200 OK

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)  # Get the message or 404
    
    # Delete the message from the database
    db.session.delete(message)
    db.session.commit()

    # Respond with an empty body
    return make_response(jsonify({}), 204)  # Status 204 No Content


if __name__ == '__main__':
    app.run(port=5555)
