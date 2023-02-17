import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
from datetime import datetime
import sys
import json
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
connection_count=0


# Define StreamHandlers for stdout and stderr
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
dual_handlers = [stdout_handler, stderr_handler]
 
# Define basic configuration for the log messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:[%(asctime)s] - %(message)s',
)
# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    logs1="Get all content"
    app.logger.info(logs1)
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      current_ts=get_current_timestamp()  
      logs=" Error Post id not found " 
      app.logger.info(logs)
      return render_template('404.html'), 404
    else:
      current_ts=get_current_timestamp()  
      logs="post id found " 
      app.logger.info(logs)  
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    current_ts=get_current_timestamp()  
    logs=" about page " 
    app.logger.info(logs)
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            current_ts=get_current_timestamp()  
            logs="POST title not found" 
            app.logger.info(logs)
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logs="POST title created" 
            app.logger.info(logs)
            return redirect(url_for('index'))

    return render_template('create.html')

#This function check healths
@app.route('/healthz')
def health_check():
    response=app.response_class(
        response=json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    logs=" health response success" 
    app.logger.info(logs)
    return response
#This function check healths
@app.route('/metrics')
def get_metrics():
    connection = get_db_connection()
    posts= connection.execute('SELECT * FROM posts').fetchall()
    post_count=0
    for post in posts:
        post_count+=1
    global connection_count
    connection_count+=1
    response = app.response_class(
            response=json.dumps({"status":"success","data":{"UserCount":connection_count,"UserCountActive":post_count}}),
            status=200,
            mimetype='application/json'
    )
    logs=" metrics response success " 
    app.logger.info(logs)
    connection.close()
    connection_count-=1
    return response


# to get the current timestamp
def get_current_timestamp():
    current_day = datetime.now().strftime('%d')
    current_month_text = datetime.now().strftime('%h')
    current_year_full = datetime.now().strftime('%Y')
    current_second= datetime.now().strftime('%S') 
    current_minute = datetime.now().strftime('%M') 
    current_hour = datetime.now().strftime('%H')
    current_ts=current_day+"//"+current_month_text+current_year_full+" "+current_hour+":"+current_minute+":"+current_second
    return current_ts

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
