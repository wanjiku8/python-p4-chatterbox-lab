from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([{
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at,
        'updated_at': message.updated_at
    } for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at,
        'updated_at': message.updated_at
    }), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at,
        'updated_at': message.updated_at
    })

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555)