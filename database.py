from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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

    def _repr_(self):
        return f'<Resultado {self.id} - {self.nome}>'