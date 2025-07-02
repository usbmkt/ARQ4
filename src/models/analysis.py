from datetime import datetime
import json
from database import db

class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    nicho = db.Column(db.String(255), nullable=False)
    produto = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float)
    publico = db.Column(db.String(500))
    concorrentes = db.Column(db.Text)
    dados_adicionais = db.Column(db.Text)
    
    # Dados da análise em formato JSON
    avatar_data = db.Column(db.JSON)
    positioning_data = db.Column(db.JSON)
    competition_data = db.Column(db.JSON)
    marketing_data = db.Column(db.JSON)
    metrics_data = db.Column(db.JSON)
    funnel_data = db.Column(db.JSON)
    
    status = db.Column(db.String(50), default='processing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analysis {self.id}: {self.nicho}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nicho': self.nicho,
            'produto': self.produto,
            'descricao': self.descricao,
            'preco': self.preco,
            'publico': self.publico,
            'concorrentes': self.concorrentes,
            'dados_adicionais': self.dados_adicionais,
            'avatar_data': self.avatar_data,
            'positioning_data': self.positioning_data,
            'competition_data': self.competition_data,
            'marketing_data': self.marketing_data,
            'metrics_data': self.metrics_data,
            'funnel_data': self.funnel_data,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

