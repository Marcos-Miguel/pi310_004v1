from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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

@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)