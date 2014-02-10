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

    def __init__(self, aid, name, phone, email, key):
        self.aid = aid
        self.name = name
        self.phone = phone
        self.email = email
        self.key = key

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
        rand_bytes = filter(lambda x: x < 128, os.urandom(1000))
        h = hashlib.sha512()
        h.update(str(rand_bytes))
        h.update(email)
        h.update(name)
        h.update(phone)
        account_key = h.hexdigest()

        cur = get_db().cursor()
        cur.execute('INSERT INTO accounts (name, phone, email, key) '+ 
                    ' VALUES(%s, %s, %s, %s) RETURNING aid',
                    (name, phone, email, account_key))
        aid = cur.fetchone()[0]
        return Account(aid, name, phone, email, account_key) if aid else None
