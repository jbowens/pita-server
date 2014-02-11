"""
The account model.

@author jbowens
"""
import hashlib, os
from mylittlepita import get_db

class Account(object):

    aid = None
    name = ""
    phone = None
    email = None
    key = None

    def __init__(self, opts):
        for k in opts:
            if hasattr(self, k):
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
    def new(name, phone, email):
        # Generate a secret key that the client keeps to refer to the account.
        rand_bytes = os.urandom(1000)
        h = hashlib.sha512()
        h.update(rand_bytes)
        h.update(email)
        h.update(name)
        h.update(phone)
        account_key = h.hexdigest()

        cur = get_db().cursor()
        cur.execute('INSERT INTO accounts (name, phone, email, key) '+ 
                    ' VALUES(%s, %s, %s, %s) RETURNING aid',
                    (name, phone, email, account_key))
        aid = cur.fetchone()[0]
        d = { 'aid': aid, 'name': name, 'phone': phone, 'email': email,
              'key': account_key }
        return Account(d) if aid else None

    @staticmethod
    def get(aid, key):
        cur = get_db().cursor()
        cur.execute('SELECT aid FROM accounts WHERE aid = %s AND key %s',
                    (aid, key))
        acc = Account(cur.fetchone()) if cur.rowcount > 0 else None
        return acc

    def update_last_seen():
        cur = get_db().cursor()
        cur.execute('UPDATE accounts SET last_seen = now() WHERE aid = %s',
                (self.aid,))

