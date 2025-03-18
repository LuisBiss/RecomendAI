from flask import Flask, render_template, request, jsonify
import os
from database import db, Resultado
from pdf_extractor import buscar_resultados
from recommender import classificar_resultado_com_modelo
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NOME_DO_BANCO_AQUI.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db.init_app(app)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdfExame' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400
    
    file = request.files['pdfExame']
    
    if file and file.filename.endswith('.pdf'):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        print(f"PDF recebido: {file.filename}")
        
        resultados = buscar_resultados(filename)
        if resultados:
            nome = request.form.get('nome', 'Desconhecido')
            novo_resultado = Resultado(
                nome=nome,
                colesterol=float(resultados.get("colesterol", 0)),
                glicose=float(resultados.get("glicose", 0)),
                t3=float(resultados.get("t3", 0)),
                t4=float(resultados.get("t4", 0)),
                tsh=float(resultados.get("tsh", 0)),
                triglicerideos=float(resultados.get("triglicerideos", 0))
            )
            db.session.add(novo_resultado)
            db.session.commit()

            recomendacao = classificar_resultado_com_modelo([
                novo_resultado.colesterol,
                novo_resultado.glicose,
                novo_resultado.t3,
                novo_resultado.t4,
                novo_resultado.tsh,
                novo_resultado.triglicerideos
            ])
            
            print(recomendacao)

            return jsonify({
                "message": "PDF enviado e dados salvos com sucesso!", 
                "resultados": resultados,
                "recomendacoes": recomendacao
            }), 200
        else:
            return jsonify({"message": "Valores não encontrados no PDF."}), 400

    return jsonify({"message": "Arquivo inválido. Envie um PDF."}), 400

@app.route('/resultados', methods=['GET'])
def resultados():
    resultados = Resultado.query.all()
    return render_template("resultados.html", resultados=resultados)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)