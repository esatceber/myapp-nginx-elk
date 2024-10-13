from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

# Tabloları uygulama başlatıldığında oluştur
db.create_all()

@app.route('/admin/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'balance': user.balance} for user in users])

@app.route('/admin/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(username=data['username'], balance=data['balance'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id}), 201

@app.route('/admin/user/<int:user_id>', methods=['PUT'])
def update_balance(user_id):
    data = request.json
    user = User.query.get(user_id)
    if user:
        user.balance += data['amount']
        db.session.commit()
        return jsonify({'balance': user.balance}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_balance(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'balance': user.balance}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')

