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

# Configuração do banco de dados usando suas variáveis
database_url = os.getenv('DATABASE_URL')
if database_url:
    try:
        # Configuração otimizada para Supabase
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_timeout': 60,
            'pool_size': 5, # Aumentado para 5
            'max_overflow': 10, # Aumentado para 10
            'connect_args': {
                'sslmode': 'require',
                'connect_timeout': 60,
                'application_name': 'ARQV2_DeepSeek_App',
                'keepalives_idle': 600,
                'keepalives_interval': 30,
                'keepalives_count': 5 # Aumentado para 5
            }
        }
        
        db.init_app(app)
        
        # Teste de conexão opcional - não bloqueia a aplicação
        with app.app_context():
            try:
                from sqlalchemy import text
                result = db.session.execute(text('SELECT 1'))
                logger.info("✅ Conexão com Supabase estabelecida com sucesso!")
            except Exception as e:
                logger.warning(f"⚠️ Conexão com banco não disponível no momento: {e}")
                logger.info("📱 Aplicação funcionará com funcionalidades limitadas")
                
    except Exception as e:
        logger.error(f"❌ Erro fatal na configuração do banco de dados: {e}")
        logger.info("📱 Aplicação funcionará sem persistência de dados")
else:
    logger.warning("📋 DATABASE_URL não encontrada. Executando sem funcionalidades de banco de dados.")

# Rota de health check
@app.route('/health')
def health_check():
    # Verificar status das APIs e banco
    deepseek_status = 'configured' if os.getenv('DEEPSEEK_API_KEY') else 'not_configured'
    supabase_status = 'configured' if os.getenv('SUPABASE_URL') else 'not_configured'
    database_status = 'configured' if database_url else 'not_configured'
    
    # Teste rápido de conexão com banco
    db_connection = 'disconnected'
    if database_url:
        try:
            with app.app_context():
                from sqlalchemy import text
                db.session.execute(text('SELECT 1'))
                db_connection = 'connected'
        except Exception as e:
            logger.error(f"Erro no health check do banco de dados: {e}")
            db_connection = 'error'
    
    return jsonify({
        'status': 'healthy',
        'message': 'UP Lançamentos - Arqueologia do Avatar com DeepSeek AI',
        'services': {
            'deepseek_ai': deepseek_status,
            'supabase': supabase_status,
            'database': database_status,
            'db_connection': db_connection
        },
        'version': '2.0.0'
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
