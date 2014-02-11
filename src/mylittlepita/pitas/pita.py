"""
The pita model.

@author jbowens
"""
from mylittlepita import get_db

class Pita(object):

    pid = None
    aid = None
    state = None
    parent_a = None
    parent_b = None

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

