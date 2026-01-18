from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import validators 
import shortuuid   
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, original_url, short_id):
        self.original_url = original_url
        self.short_id = short_id

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    short_url_display = None
    
    if request.method == 'POST':
        original_url = request.form.get('url_input')
        
        if not validators.url(original_url):
            flash('Invalid URL! Please include http:// or https://', 'danger')
            return redirect(url_for('home'))

        existing_url = Url.query.filter_by(original_url=original_url).first()
        
        if existing_url:
            short_id = existing_url.short_id
        else:
            short_id = shortuuid.ShortUUID().random(length=6)
            new_url = Url(original_url=original_url, short_id=short_id)
            db.session.add(new_url)
            db.session.commit()
        
        short_url_display = request.host_url + short_id
        
    return render_template('index.html', short_url=short_url_display)

@app.route('/history')
def history():
    urls = Url.query.order_by(Url.id.desc()).all() 
    return render_template('history.html', urls=urls, host_url=request.host_url)

@app.route('/<short_id>')
def redirect_to_url(short_id):
    link = Url.query.filter_by(short_id=short_id).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    app.run(debug=True)