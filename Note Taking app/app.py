from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Note {self.content}>'

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note_content = request.form.get("note")
        
        
        if note_content:
            new_note = Note(content=note_content)
            db.session.add(new_note)  
            db.session.commit()       

    all_notes = Note.query.all()
    return render_template("home.html", notes=all_notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)