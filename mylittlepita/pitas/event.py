import datetime
from mylittlepita import get_db

class PitaEvent(object):
    peid = None
    pid = None
    aid = None
    event_type = None
    time = None

    def __init__(self, opts):
        for k in opts:
            if hasattr(self, k):
                setattr(self, k, opts[k])

    @staticmethod
    def record_event(pita, event_type, time = None):
        """
        Records an event in a Pita's lifetime. If time is omitted,
        the current time will be used.
        """
        time = time if time else datetime.datetime.now()
        cur = get_db().cursor()
        cur.execute('INSERT INTO pita_events (pid, aid, event_type, time) ' + \
                    'VALUES(%s, %s, %s, %s) RETURNING peid',
                    (pita.pid, pita.aid, event_type, time))
        peid = cur.fetchone()[0]
        cur.close()
        return PitaEvent({
            'peid': peid,
            'pid': pita.pid,
            'aid': pita.aid,
            'event_type': event_type,
            'time': time
        })
