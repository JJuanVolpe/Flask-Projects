from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:comida@localhost/contactsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)


@app.before_request
def create_tables():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True
        

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/submit", methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()
    
    response_message = f"Thank you, {name}. Your message has been received."
     
    return jsonify({'message': response_message})




if __name__ == "__main__":
    app.run(debug=True)
    
    
