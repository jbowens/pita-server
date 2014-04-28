import json
from flask.ext.script import Manager
from mylittlepita import app, get_db
manager = Manager(app)

@manager.command
def load():
    cur = get_db().cursor()
    f = open('dictionary.json', 'r')
    words = json.load(f)
    count = 0
    for w, pos in words.iteritems():
        cur.execute('INSERT INTO dictionary_words (word, pos) VALUES(%s, %s)',
                    (w, pos))
        count = count + 1
    f.close()
    print 'Inserted %d words.' % count

if __name__ == '__main__':
    manager.run()
