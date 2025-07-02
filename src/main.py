import os
import logging
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
from routes.user import user_bp
from routes.analysis import analysis_bp

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente
load_dotenv()

# Criar aplicação Flask
app = Flask(__name__, static_folder='static')

# Configurar CORS para permitir todas as origens
CORS(app, origins=os.getenv('CORS_ORIGINS', '*'))

# Configuração da aplicação
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a-default-secret-key-that-should-be-changed')

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(analysis_bp, url_prefix='/api')

# Configuração do banco de dados com fallback
database_url = os.getenv('DATABASE_URL')
if database_url:
    try:
        # Corrigir URL do PostgreSQL se necessário
        if database_url.startswith('postgres://'):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        # Forçar IPv4 e SSL
        if "?sslmode=" not in database_url:
            database_url += "?sslmode=require"
        
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_timeout': 30,
            'pool_size': 5,
            'max_overflow': 10,
            'connect_args': {
                'sslmode': 'require',
                'connect_timeout': 30,
                'application_name': 'ARQV2_DeepSeek_App',
                # Forçar IPv4
                'host': database_url.split('@')[1].split(':')[0] if '@' in database_url else None
            }
        }
        
        db.init_app(app)
        
        with app.app_context():
            try:
                # Teste de conexão simples
                db.engine.execute('SELECT 1')
                logger.info("Conexão com banco de dados estabelecida com sucesso!")
            except Exception as e:
                logger.warning(f"Erro na conexão com banco de dados: {e}")
                logger.info("Aplicação funcionará sem persistência de dados")
                
    except Exception as e:
        logger.error(f"Erro na configuração do banco de dados: {e}")
        logger.info("Aplicação funcionará sem persistência de dados")
else:
    logger.warning("DATABASE_URL não encontrada. Executando sem funcionalidades de banco de dados.")

# Rota de health check
@app.route('/health')
def health_check():
    # Verificar status das APIs
    deepseek_status = 'configured' if os.getenv('DEEPSEEK_API_KEY') else 'not_configured'
    supabase_status = 'configured' if os.getenv('SUPABASE_URL') else 'not_configured'
    
    return jsonify({
        'status': 'healthy',
        'message': 'Aplicação funcionando corretamente',
        'deepseek_status': deepseek_status,
        'supabase_status': supabase_status,
        'database_status': 'connected' if database_url else 'not_configured'
    })

# Rota para servir arquivos estáticos e SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno: {error}")
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)