from flask import render_template, url_for
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room_list')
def room_list():
    return render_template('room_list.html')


if __name__ == "__main__":
    app.run(debug=True)