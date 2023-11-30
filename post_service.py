from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5002"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

@app.route('/create_post', methods=['POST'])
@cross_origin()
def create_post():
    data = request.get_json()
    print(f"Received data: {data}")  # this line for debugging
    username = data.get('username')
    content = data.get('content')
    print(f"Username data: {username}")  # this line for debugging

    with app.app_context():
        user = User.query.filter_by(username=username).first()
        print(f"Found user: {user}")  # this line for debugging

        if not user:
            return jsonify({'error': 'User not found'}), 404

        new_post = Post(content=content, author=user)
        db.session.add(new_post)
        db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/get_posts', methods=['GET'])
@cross_origin()
def get_posts():
    with app.app_context():
        posts = Post.query.all()
        post_data = [{'id': post.id, 'username': post.author.username, 'content': post.content, 'likes': post.likes, 'comments': [{'username': comment.author.username, 'content': comment.content} for comment in post.comments]} for post in posts]
    return jsonify(post_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
