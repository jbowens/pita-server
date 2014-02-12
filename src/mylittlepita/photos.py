import psycopg2
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from flask import Blueprint, g, request, jsonify, current_app
from . import get_db
from errors import access_denied

photos = Blueprint('photos', __name__)

@photos.route('/record', methods=['POST'])
def log_photo():
    """
    Endpoint for recording photos taken on the client.
    """
    if not g.authorized:
        return access_denied()
    if not 'photo' in request.files:
        return api_error('no photo attached')

    f = request.files['photo']
    ext = f.filename.rsplit('.', 1)[1]

    context = request.form['context'] if 'context' in request.form else None

    # Insert the photo into the database.
    cur = get_db().cursor()
    cur.execute('INSERT INTO logged_photos (aid, ext, context) VALUES(%s, %s, %s) RETURNING aid',
            (g.account.aid, ext, context))
    pid = cur.fetchone()[0]

    # Send the image contents to S3
    conn = S3Connection(current_app.config['AWS_ACCESS_KEY'], current_app.config['AWS_SECRET_KEY'])
    bucket = conn.get_bucket(current_app.config['S3_BUCKET'])
    k = Key(bucket)
    k.key = str(pid)
    k.set_contents_from_file(f)

    # Mark the file as saved
    cur = get_db().cursor()
    cur.execute('UPDATE logged_photos SET saved = %s WHERE pid = %s',
            (True, pid))
    return jsonify(status='ok')

