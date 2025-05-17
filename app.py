from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pi310.sqlite3.db"

# initialize the app with the extension
db = SQLAlchemy(app)

class Contatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    descricao = db.Column(db.String(200))
    date_created = db.Column(db.DateTime(6), default=db.func.current_timestamp(), nullable = False)

    def __init__(self, nome, email, descricao):
        self.nome = nome
        self.email = email
        self.descricao = descricao

with app.app_context():
    db.create_all()

@app.route('/imc/', methods=['GET', 'POST'])
def imc_calc():
    imc = None
    classificacao = None

    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
            imc = round(peso / (altura ** 2), 2)

            if imc < 18.5:
                classificacao = "Abaixo do peso"
            elif imc < 25:
                classificacao = "Peso normal"
            elif imc < 30:
                classificacao = "Sobrepeso"
            else:
                classificacao = "Obesidade"
        except:
            imc = "Erro nos dados"
            classificacao = ""

    return render_template('imc.html', imc=imc, classificacao=classificacao)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Neste estágio do aplicativo a leitura dos dados inseridos
#no banco de dados poderá ser feito pelo software: sqlitestudio.
@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        contato = Contatos(nome, email, assunto)
        db.session.add(contato)
        db.session.commit()
        status = "Mensagem registrada"
    return render_template('contato.html', status = status)

if __name__ == '__main__':
    app.run(debug=True)