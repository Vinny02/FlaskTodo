from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os



app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    completed = db.Column(db.Boolean)
    dateAdded = db.Column(db.DateTime, default=datetime.now())




    def __init__(self, text, completed=False, dateAdded=None):
        self.text = text
        self.completed = completed
        self.dateAdded = dateAdded if dateAdded is not None else datetime.now()

    
    


def create_task(text):
    task = Task(text=text)
    db.session.add(task)
    db.session.commit()
    db.session.refresh(task)


def read_tasks():
    return db.session.query(Task).all()


def update_task(task_id, text, completed):
    db.session.query(Task).filter_by(id=task_id).update({
        "text": text,
        "completed": True if completed == "on" else False
    })
    db.session.commit()


def delete_task(task_id):
    db.session.query(Task).filter_by(id=task_id).delete()
    db.session.commit()


@app.route("/", methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        create_task(request.form['text'])
    return render_template("index.html", tasks=read_tasks())


@app.route("/edit/<task_id>", methods=["POST", "GET"])
def edit_task(task_id):
    if request.method == "POST":
        update_task(task_id, text=request.form['text'], completed=request.form['completed'])
    elif request.method == "GET":
        delete_task(task_id)
    return redirect("/", code=302)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)