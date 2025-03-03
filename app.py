from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import PyPDF2
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NOME_DO_BANCO_AQUI.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    glicose = db.Column(db.Float)
    t3 = db.Column(db.Float)
    t4 = db.Column(db.Float)
    tsh = db.Column(db.Float)
    colesterol = db.Column(db.Float)
    triglicerideos = db.Column(db.Float)

    def __repr__(self):
        return f'<Resultado {self.id} - {self.nome}>'

def buscar_resultados(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""

            for page in reader.pages:
                text += page.extract_text()

            text = text.replace("\n", " ")

            def buscar_valor(keyword):
                position = text.find(keyword)
                if position != -1:
                    result_position = text.find("RESULTADO", position)
                    if result_position != -1:
                        start = result_position + len("RESULTADO") + 1
                        end = start + 5
                        result_value = text[start:end].strip()
                        return result_value.replace(",", ".")
                return None

            resultados = {
                "glicose": buscar_valor("GLICOSE JEJUM"),
                "t3": buscar_valor("T3 TOTAL"),
                "t4": buscar_valor("T4 TOTAL"),
                "tsh": buscar_valor("TSH ULTRA SENSÍVEL"),
                "colesterol": buscar_valor("COLESTEROL TOTAL"),
                "triglicerideos": buscar_valor("TRIGLICERIDES")
            }

            return resultados

    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return None

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
                glicose=float(resultados.get("glicose", 0)),
                t3=float(resultados.get("t3", 0)),
                t4=float(resultados.get("t4", 0)),
                tsh=float(resultados.get("tsh", 0)),
                colesterol=float(resultados.get("colesterol", 0)),
                triglicerideos=float(resultados.get("triglicerideos", 0))
            )
            db.session.add(novo_resultado)
            db.session.commit()

            return jsonify({
                "message": "PDF enviado e dados salvos com sucesso!", 
                "resultados": resultados
            }), 200
        else:
            return jsonify({"message": "Valores não encontrados no PDF."}), 400
    else:
        return jsonify({"message": "Arquivo não é um PDF válido"}), 400
    
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        
    app.run(debug=True)