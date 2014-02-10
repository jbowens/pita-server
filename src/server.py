from flask import Flask

app = Flask(__name__)

@app.route('/')
def show_frontend():
    return 'This API is for Pitas only.' 


# Spawn the server
if __name__ == '__main__':
    app.run()
