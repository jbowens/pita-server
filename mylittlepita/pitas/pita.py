"""
The pita model.

@author jbowens
"""
import math, random
from mylittlepita import get_db
from flask import current_app
from psycopg2.extras import RealDictCursor

def random_color():
    return random.uniform(0, 2.0 * math.pi)

class Pita(object):

    pid = None
    aid = None
    state = None
    parent_a = None
    parent_b = None
    name = None
    body_hue = None
    spots_hue = None
    tail_hue = None
    has_spots = False
    happiness = None
    hunger = None
    sleepiness = None

    def __init__(self, opts):
        for k in opts:
            if hasattr(self, k):
                setattr(self, k, opts[k])

    def save_status(self, status):
        """
        Sets the Pita's status attributes to be the attributes given in
        the passed dictionary.
        """
        cur = get_db().cursor()
        cur.execute('UPDATE pitas SET happiness = %s, hunger = %s, sleepiness = %s WHERE pid = %s',
                    (status['happiness'], status['hunger'], status['sleepiness'], self.pid))
        cur.close()

    @staticmethod
    def get_by_account(aid):
        """
        Retrieves the Pita associated with the given account id, if any.
        """
        cur = get_db().cursor(cursor_factory = RealDictCursor)
        cur.execute('SELECT * FROM pitas WHERE aid = %s AND (state = \'alive\' OR state = \'egg\')',
                    (aid,))
        row = cur.fetchone()
        current_app.logger.debug(row)
        pita = Pita(row) if cur.rowcount > 0 else None
        return pita

    @staticmethod
    def create_random_pita(aid):
        """
        Creates a ranom Pita. This is mostly intended for testing
        purposes.
        """
        pita = Pita({
            'aid': aid,
            'state': 'egg',
            'parent_a': None,
            'parent_b': None,
            'name': Pita.generate_name(),
            'body_hue': random_color(),
            'spots_hue': random_color(),
            'tail_hue': random_color(),
            'has_spots': bool(random.getrandbits(1))
        })
        Pita.create_pita(pita)
        return pita

    @staticmethod
    def generate_name():
        """
        Generates a random pita name.
        """
        cur = get_db().cursor()
        cur.execute('SELECT word FROM dictionary_words WHERE pos=\'noun\' ORDER BY random() LIMIT 1')
        second_word = cur.fetchone()[0]
        first_word_type = random.choice(['adjective', 'noun'])
        cur.execute('SELECT word FROM dictionary_words WHERE pos = %s ORDER BY random() LIMIT 1', (first_word_type,))
        first_word = cur.fetchone()[0]
        name = first_word + ' ' + second_word
        name = name.title()
        return name

    @staticmethod
    def create_pita(pita):
        """
        Takes a Pita object and inserts it into the database. It will
        also update tables related to Pita events.
        """
        cur = get_db().cursor()
        q = 'INSERT INTO pitas (aid, state, parent_a, parent_b, name, body_hue, ' + \
            'spots_hue, tail_hue, has_spots) ' +  \
            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING pid'
        cur.execute(q, [pita.aid,
                        pita.state,
                        pita.parent_a,
                        pita.parent_b,
                        pita.name,
                        pita.body_hue,
                        pita.spots_hue,
                        pita.tail_hue,
                        pita.has_spots])
        pita.pid = cur.fetchone()[0]
        cur.execute('INSERT INTO pita_events (pid, aid, event_type) ' + \
                    'VALUES(%s, %s, %s)', \
                    [pita.pid, pita.aid, 'conception'])
        cur.close()


