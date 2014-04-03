"""
The account model.

@author jbowens
"""
import hashlib, os, datetime, ppygis
from mylittlepita import get_db
from psycopg2.extras import RealDictCursor

class Account(object):

    aid = None
    uuid = None
    name = ""
    phone = None
    email = None
    key = None
    created = None
    last_seen = None
    latitude = None
    longitude = None
    loc = None
    loc_time = None

    def __init__(self, opts):
        for k in opts:
            if hasattr(self, str(k)):
                setattr(self, k, opts[k])

    @staticmethod
    def phone_used(phone):
        cur = get_db().cursor()
        cur.execute('SELECT aid FROM accounts WHERE phone = %s', (phone,))
        used = cur.rowcount > 0
        cur.close()
        return used

    @staticmethod
    def email_used(email):
        cur = get_db().cursor()
        cur.execute('SELECT aid FROM accounts WHERE email = %s', (email,))
        used = cur.rowcount > 0
        cur.close()
        return used

    @staticmethod
    def uuid_used(uuid):
        cur = get_db().cursor()
        cur.execute('SELECT aid FROM accounts WHERE uuid = %s', (uuid,))
        used = cur.rowcount > 0
        cur.close()
        return used

    @staticmethod
    def new(uuid, name, phone, email):
        # Generate a secret key that the client keeps to refer to the account.
        rand_bytes = os.urandom(1000)
        h = hashlib.sha512()
        h.update(rand_bytes)
        h.update(uuid)
        if email:
            h.update(email)
        if name:
            h.update(name)
        if phone:
            h.update(phone)
        account_key = h.hexdigest()

        cur = get_db().cursor()
        cur.execute('INSERT INTO accounts (uuid, name, phone, email, key) ' +
                    ' VALUES(%s, %s, %s, %s, %s) RETURNING aid',
                    (uuid, name, phone, email, account_key))
        aid = cur.fetchone()[0]
        d = { 'aid': aid, 'uuid': uuid, 'name': name, 'phone': phone, 'email': email,
              'key': account_key }
        return Account(d) if aid else None

    @staticmethod
    def get(aid, key):
        cur = get_db().cursor(cursor_factory = RealDictCursor)
        cur.execute('SELECT * FROM accounts WHERE aid = %s AND key = %s',
                    (aid, key))
        row = cur.fetchone()
        acc = Account(row) if cur.rowcount > 0 else None
        return acc

    def update_last_seen(self):
        cur = get_db().cursor()
        cur.execute('UPDATE accounts SET last_seen = now() WHERE aid = %s',
                (self.aid,))

    def update_location(self, lat, lng, when):
        when = when if when else datetime.datetime.now()
        cur = get_db().cursor()
        cur.execute('UPDATE accounts SET latitude=%s, longitude=%s, loc=ST_SetSRID(ST_MakePoint(%s, %s),4326), loc_time = %s WHERE aid = %s',
                (float(lat), float(lng), float(lat), float(lng), when, self.aid))

        # Record the location in the locations table as well
        if when:
            cur.execute('INSERT INTO locations (aid, time, latitude, longitude, loc) VALUES(%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s,%s),4326))',
                    (self.aid, when, float(lat), float(lng), float(lat), float(lng)))
        else:
            cur.execute('INSERT INTO locations (aid, latitude, longitude, loc) VALUES(%s, %s, %s, ST_SetSRID(ST_MakePoint(%s,%s),4326))',
                    (self.aid, float(lat), float(lng), float(lat), float(lng)))

