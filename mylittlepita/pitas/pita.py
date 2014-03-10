"""
The pita model.

@author jbowens
"""
import math, random
from mylittlepita import get_db

def random_color():
    return random.uniform(0, 2.0 * math.pi)

class Pita(object):

    pid = None
    aid = None
    state = None
    parent_a = None
    parent_b = None
    body_hue = None
    spots_hue = None
    tail_hue = None
    has_spots = False

    def __init__(self, opts):
        for k in opts:
            if hasattr(self, k):
                setattr(self, k, opts[k])

    @staticmethod
    def get_by_account(aid):
        """
        Retrieves the Pita associated with the given account id, if any.
        """
        cur = get_db().cursor()
        cur.execute('SELECT * FROM pitas WHERE aid = %s',
                    (aid,))
        pita = Pita(cur.fetchone()) if cur.rowcount > 0 else None
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
            'body_hue': random_color(),
            'spots_hue': random_color(),
            'tail_hue': random_color(),
            'has_spots': bool(random.getrandbits(1))
        })
        Pita.create_pita(pita)
        return pita
        
    @staticmethod
    def create_pita(pita):
        """
        Takes a Pita object and inserts it into the database. It will
        also update tables related to Pita events.
        """
        cur = get_db().cursor()
        q = 'INSERT INTO pitas (aid, state, parent_a, parent_b, body_hue, ' + \
            'spots_hue, tail_hue, has_spots) ' +  \
            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING aid'
        cur.execute(q, [pita.aid,
                        pita.state,
                        pita.parent_a,
                        pita.parent_b,
                        pita.body_hue,
                        pita.spots_hue,
                        pita.tail_hue,
                        pita.has_spots])
        pita.pid = cur.fetchone()[0]
        cur.execute('INSERT INTO pita_events (pid, aid, event_type) ' + \
                    'VALUES(%s, %s, %s)', \
                    [pita.pid, pita.aid, 'conception'])
        cur.close()


