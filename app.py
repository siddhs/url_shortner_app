import json
import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, redirect, jsonify, Response
import validators
import datetime


"""
Opens a connection to the database.db database file and then sets the row_factory attribute to sqlite3.Row
As a result, we can have name-based access to columns; the database connection will return rows that behave like regular Python dictionaries.
Lastly, the function returns the conn connection object we will be using to access the database.
"""
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = "q)D)^LnGUjt^x`V3H1YP0g8~*!W!'8"

# Hashids is a library that generates a short unique ID from integers.
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']
        expiry = request.form['expiry']

        formatted_expiry_date = None
        if expiry:
            formatted_expiry_date = datetime.datetime.strptime(expiry, '%Y-%m-%d')
        else:
            # If expiry is not provided then default expiry is 10 years from current timestamp
            formatted_expiry_date = datetime.datetime.now() + datetime.timedelta(days=3650)

        # This is for handling case when no url is passed
        if not url:
            resp = Response(json.dumps({"message":"Empty URL!"}), mimetype='application/json')
            resp.status_code = 400
            return resp
        # This is for handling case when malformed url is passed, e.g abcd
        if not validators.url(url):
            resp = Response(json.dumps({"message":"Invalid URL!!"}), mimetype='application/json')
            resp.status_code = 400
            return resp
        
        # Fetch the current number of rows
        cursor = conn.execute('SELECT COUNT(*) FROM urls')
        url_count = cursor.fetchone()[0]

        # Increment the row count to determine the new url_id, we will use this incremented number in our encoding method
        url_id = url_count + 1
        # Encode the URL ID to create a unique short URL
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        url_data = conn.execute('''INSERT INTO urls (id, original_url, short_url, expiry) VALUES (?, ?, ?, ?)''',
                                (hashid, url, short_url, formatted_expiry_date))
        
        # Save and close the DB connection
        conn.commit()
        conn.close()
        return jsonify({'shortened_url': short_url})
    
    if request.method == 'GET':
        return jsonify({"message":"Welcome to URL Shortner App!"})

@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()
    
    if id:
        # Retrieve URL data from the database based on the provided ID, the ID will be a hash of a long url
        url_data = conn.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (id,)
                                ).fetchone()
        
        if url_data is None:
            conn.close()
            resp = Response(json.dumps({"message":"URL with given ID not found"}), mimetype='application/json')
            resp.status_code = 404
            return resp
        
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        # Increment the clicks count and update it in the database
        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks+1, id))

        conn.commit()
        conn.close()

        # Redirect the user to the original URL
        return redirect(original_url)
    else:
        resp = Response(json.dumps({"message":"Invalid URL!!"}), mimetype='application/json')
        resp.status_code = 400
        return resp

@app.route('/stats')
def stats():
    conn = get_db_connection()

    # Fetch all data from the database
    db_urls = conn.execute('SELECT id, created, original_url, short_url, expiry, clicks FROM urls'
                           ).fetchall()
    conn.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        urls.append(dict(url))
    return jsonify({'urls': urls})

@app.route('/delete/<id>', methods = ['DELETE'])
def delete_url(id):
    conn = get_db_connection()
    # Fetch the short URL associated with the provided ID from the database
    url_data = conn.execute('SELECT short_url FROM urls WHERE id = ?', (id,)).fetchone()
    
    if url_data is None:
        conn.close()
        resp = Response(json.dumps({"message":"URL with given ID not found"}), mimetype='application/json')
        resp.status_code = 404
        return resp
    
    short_url = url_data['short_url']
    
    conn.execute('DELETE FROM urls WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': f'URL with ID {id} and short URL {short_url} has been deleted'})
