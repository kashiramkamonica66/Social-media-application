from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/like_post', methods=['POST'])
def like_post():
    data = request.get_json()
    post_id = data.get('post_id')
    username = data.get('username')

    post = posts.get(post_id)
    if post:
        post['likes'] += 1
        return jsonify({'message': 'Post liked successfully'}), 200
    else:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/comment_post', methods=['POST'])
def comment_post():
    data = request.get_json()
    post_id = data.get('post_id')
    username = data.get('username')
    comment = data.get('comment')

    post = posts.get(post_id)
    if post:
        post['comments'].append({'username': username, 'comment': comment})
        return jsonify({'message': 'Comment added successfully'}), 200
    else:
        return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5003)
