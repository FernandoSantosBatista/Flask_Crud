from flask import  Flask, jsonify, request
from flask_sqlalchemy import  SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import  CORS



# settings
app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI']  =  'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



# table
class Cadastros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    bairro= db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, nome, bairro, cidade, email):
        self.nome = nome
        self.bairro = bairro
        self.cidade = cidade
        self.email = email

# schema
class CadastrosSchema(ma.Schema):
    class  Meta:
        fields = ("id", "nome", "bairro", "cidade", "email")


# schema obj
cadastro_schema = CadastrosSchema() 
cadastros_schema = CadastrosSchema(many=True) 

# routes

#  ------------------ get all
@app.route('/cadastro', methods=['GET'])
def get_articles():
    all_cadastros = Cadastros.query.all()
    return  cadastros_schema.jsonify(all_cadastros)


#  ------------------ get by ID
@app.route('/cadastro/<id>/', methods=['GET'])
def article_details(id):

    cadastro_detail = Cadastros.query.get(id)
    if cadastro_detail:
        return cadastro_schema.jsonify(cadastro_detail)
    else:
        return "No article with that ID"
    


#  ------------------ post or add new 
@app.route('/cadastro', methods=['POST'])
def add_cadastro():
    nome = request.json['nome']
    bairro = request.json['bairro']
    cidade = request.json['cidade']
    email = request.json['email']

    cadastros = Cadastros(nome, bairro, cidade, email)
    db.session.add(cadastros)
    db.session.commit()
    return cadastro_schema.jsonify(cadastros)

#  ------------------ update individual
@app.route('/cadastro/<id>/', methods=['PUT'])
def update_cadastros(id):
    update_cadastros = Cadastros.query.get(id)
    update_cadastros.nome = request.json['nome']
    update_cadastros.bairro = request.json['bairro']
    update_cadastros.cidade = request.json['cidade']
    update_cadastros.email = request.json['email']
    db.session.commit()
    return cadastro_schema.jsonify(update_cadastros)


#  ------------------ delete individual
@app.route('/cadastro/<id>/', methods=['DELETE'])
def delete_cadastros(id):
    delete_cadastros = Cadastros.query.get(id)
    db.session.delete(delete_cadastros)
    db.session.commit()
    return cadastro_schema.jsonify(delete_cadastros)


if __name__ == '__main__':
    app.run(debug=True)
