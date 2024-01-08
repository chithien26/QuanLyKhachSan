from flask import render_template, url_for
from app import app, db
import dao

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room_list')
def room_list():
    rooms = dao.get_phong()
    return render_template('room_list.html', room_list=rooms)


if __name__ == "__main__":
    app.run(debug=True)