from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Hustl')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
sports = db.sports
posts = db.posts
comments = db.comments

@app.route('/')
def main_index():
    return render_template('main_index.html', sports=sports.find(), sport={}, title='Sports')

@app.route('/sports/<sports_id>', methods=['POST'])
def sports_update(sport_id):
    updated_post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'Images': request.form.get('Image')

    }
    sports.update_one(
        {'_id': ObjectId(sport_id)},
        {'$set': updated_post})
    return redirect(url_for('main_index', sport_id=sport_id, sports=sports.find()))

@app.route('/sports/profile')
def sports_profile():
    return render_template('sports_profile.html', sport={}, title='Profile')

@app.route('/sports/AboutUs')
def sports_AboutUs():
    return render_template('AboutUs.html', title='About Us')

@app.route('/sports/<sport_id>/edit')
def sports_edit(sport_id):
    sport = sports.find_one({'_id': ObjectId(sport_id)})
    return render_template('sports_edit.html', sport=sport, title='Edit Posts')

@app.route('/sports/Post')
def sports_post():
    return render_template('Post.html', title='Post')


@app.route('/sports/<sport_id>/delete', methods=['POST'])
def sports_delete(sport_id):
    sports.delete_one({'_id': ObjectId(sport_id)})
    return redirect(url_for('main_index'))

@app.route('/sports/comments', methods=['POST'])
def comments_new():
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'sport_id': ObjectId(request.form.get('sport_id'))
    }
    print(comment)
    return redirect(url_for('sports_show', sport_id=request.form.get('sport_id')))

@app.route('/sports/<sport_id>')
def sports_show(sport_id):
    sport = sports.find_one({'_id': ObjectId(sport_id)})
    sport_comments = comments.find({'sport_id': ObjectId(sport_id)})
    return render_template('sports_show.html', sport=sport, comments=sport_comments, sports=sports.find())

@app.route('/sports/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('sports_show', sport_id=comment.get('sport_id')))

@app.route('/sports', methods=['POST'])
def sports_submit():
    sport = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'Images': request.form.get('Image'),
        'Height': request.form.get('Height'),
        'Weight': request.form.get('Weight'),
        'Hometown': request.form.get('Hometown'),
        'Schools': request.form.get('Schools'),
        'created_at': datetime.now()
    }
    sport_id = sports.insert_one(sport).inserted_id
    return redirect(url_for('sports_show', sport_id=sport_id, sports=sports.find()))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))