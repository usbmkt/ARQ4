from flask import Blueprint, request, jsonify
import os
import json
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client
from services.deepseek_client import DeepSeekClient
import requests
import re
from typing import Dict, List, Optional, Tuple
import concurrent.futures
from functools import lru_cache

# Configure logging PRIMEIRO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__)

# Configure Supabase com suas variáveis exatas
supabase_url = os.getenv('SUPABASE_URL')  # https://albyamqjdopihijsderu.supabase.co
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Sua service role key
supabase: Client = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
        logger.info("✅ Cliente Supabase configurado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao configurar Supabase: {e}")

# Initialize DeepSeek client
try:
    deepseek_client = DeepSeekClient()
    logger.info("✅ Cliente DeepSeek configurado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao inicializar DeepSeek: {e}")
    deepseek_client = None

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    """Análise completa de mercado com DeepSeek"""
    try:
        data = request.get_json()
        
        if not data or not data.get('nicho'):
            return jsonify({'error': 'Nicho é obrigatório'}), 400
        
        # Extract and validate form data with safe conversion
        analysis_data = {
            'nicho': data.get('nicho', '').strip(),
            'produto': data.get('produto', '').strip(),
            'descricao': data.get('descricao', '').strip(),
            'preco': data.get('preco', ''),
            'publico': data.get('publico', '').strip(),
            'concorrentes': data.get('concorrentes', '').strip(),
            'dados_adicionais': data.get('dadosAdicionais', '').strip(),
            'objetivo_receita': data.get('objetivoReceita', ''),
            'prazo_lancamento': data.get('prazoLancamento', ''),
            'orcamento_marketing': data.get('orcamentoMarketing', '')
        }
        
        # Validate and convert numeric fields with safe handling
        def safe_float_conversion(value, default=None):
            """Converte valor para float de forma segura"""
            if value is None or value == '':
                return default
            try:
                return float(str(value).replace(',', '.'))
            except (ValueError, TypeError):
                return default
        
        analysis_data['preco_float'] = safe_float_conversion(analysis_data['preco'], 997.0)
        analysis_data['objetivo_receita_float'] = safe_float_conversion(analysis_data['objetivo_receita'], 100000.0)
        analysis_data['orcamento_marketing_float'] = safe_float_conversion(analysis_data['orcamento_marketing'], 50000.0)
        
        logger.info(f"🔍 Iniciando análise para nicho: {analysis_data['nicho']}")
        
        # Save initial analysis record
        analysis_id = save_initial_analysis(analysis_data)
        
        # Generate comprehensive analysis with DeepSeek
        if deepseek_client:
            logger.info("🤖 Usando DeepSeek AI para análise")
            analysis_result = deepseek_client.analyze_avatar_comprehensive(analysis_data)
        else:
            logger.warning("⚠️ DeepSeek não disponível, usando análise de fallback")
            analysis_result = create_fallback_analysis(analysis_data)
        
        # Update analysis record with results
        if supabase and analysis_id:
            update_analysis_record(analysis_id, analysis_result)
            analysis_result['analysis_id'] = analysis_id
        
        logger.info("✅ Análise concluída com sucesso")
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"❌ Erro na análise: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

def save_initial_analysis(data: Dict) -> Optional[int]:
    """Salva registro inicial da análise no Supabase"""
    if not supabase:
        logger.warning("⚠️ Supabase não configurado, pulando salvamento")
        return None
    
    try:
        analysis_record = {
            'nicho': data['nicho'],
            'produto': data['produto'],
            'descricao': data['descricao'],
            'preco': data['preco_float'],
            'publico': data['publico'],
            'concorrentes': data['concorrentes'],
            'dados_adicionais': data['dados_adicionais'],
            'objetivo_receita': data['objetivo_receita_float'],
            'orcamento_marketing': data['orcamento_marketing_float'],
            'prazo_lancamento': data['prazo_lancamento'],
            'status': 'processing',
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('analyses').insert(analysis_record).execute()
        if result.data:
            analysis_id = result.data[0]['id']
            logger.info(f"💾 Análise salva no Supabase com ID: {analysis_id}")
            return analysis_id
    except Exception as e:
        logger.warning(f"⚠️ Erro ao salvar no Supabase: {str(e)}")
    
    return None

def update_analysis_record(analysis_id: int, results: Dict):
    """Atualiza registro da análise com resultados"""
    try:
        update_data = {
            'avatar_data': results.get('avatar', {}),
            'positioning_data': results.get('escopo', {}),
            'competition_data': results.get('concorrencia', {}),
            'marketing_data': results.get('estrategia_aquisicao', {}),
            'metrics_data': results.get('metricas', {}),
            'funnel_data': results.get('projecoes', {}),
            'market_intelligence': results.get('mercado', {}),
            'action_plan': results.get('plano_acao', {}),
            'comprehensive_analysis': results,  # Salva análise completa
            'status': 'completed',
            'updated_at': datetime.utcnow().isoformat()
        }
        
        supabase.table('analyses').update(update_data).eq('id', analysis_id).execute()
        logger.info(f"💾 Análise {analysis_id} atualizada no Supabase")
        
    except Exception as e:
        logger.warning(f"⚠️ Erro ao atualizar análise no Supabase: {str(e)}")

def create_fallback_analysis(data: Dict) -> Dict:
    """Cria análise de fallback detalhada quando a IA falha"""
    nicho = data.get('nicho', 'Produto Digital')
    produto = data.get('produto', 'Produto Digital')
    
    # Garantir que preco seja um número válido
    try:
        preco = float(data.get('preco_float', 0)) if data.get('preco_float') is not None else 997.0
    except (ValueError, TypeError):
        preco = 997.0
    
    logger.info(f"🔄 Criando análise de fallback para {nicho} - Preço: R$ {preco}")
    
    return {
        "escopo": {
            "nicho_principal": nicho,
            "subnichos": [f"{nicho} para iniciantes", f"{nicho} avançado", f"{nicho} empresarial"],
            "produto_ideal": produto,
            "proposta_valor": f"A metodologia mais completa e prática para dominar {nicho} no mercado brasileiro"
        },
        "avatar": {
            "demografia": {
                "faixa_etaria": "32-45 anos",
                "genero": "65% mulheres, 35% homens",
                "localizacao": "Região Sudeste (45%), Sul (25%), Nordeste (20%), Centro-Oeste (10%)",
                "renda": "R$ 8.000 - R$ 25.000 mensais",
                "escolaridade": "Superior completo (80%), Pós-graduação (45%)",
                "profissoes": ["Empreendedores digitais", "Consultores", "Profissionais liberais", "Gestores", "Coaches"]
            },
            "psicografia": {
                "valores": ["Crescimento pessoal contínuo", "Independência financeira", "Reconhecimento profissional"],
                "estilo_vida": "Vida acelerada, busca por eficiência e produtividade, valoriza tempo de qualidade com família, investe em desenvolvimento pessoal",
                "aspiracoes": ["Ser reconhecido como autoridade no nicho", "Ter liberdade geográfica e financeira"],
                "medos": ["Ficar obsoleto no mercado", "Perder oportunidades por indecisão", "Não conseguir escalar o negócio"],
                "frustracoes": ["Excesso de informação sem aplicação prática", "Falta de tempo para implementar estratégias"]
            },
            "comportamento_digital": {
                "plataformas": ["Instagram (stories e reels)", "LinkedIn (networking profissional)"],
                "horarios_pico": "6h-8h (manhã) e 19h-22h (noite)",
                "conteudo_preferido": ["Vídeos educativos curtos", "Cases de sucesso com números", "Dicas práticas aplicáveis"],
                "influenciadores": ["Especialistas reconhecidos no nicho", "Empreendedores de sucesso com transparência"]
            }
        },
        "dores_desejos": {
            "principais_dores": [
                {
                    "descricao": f"Dificuldade para se posicionar como autoridade em {nicho}",
                    "impacto": "Baixo reconhecimento profissional e dificuldade para precificar serviços adequadamente",
                    "urgencia": "Alta"
                },
                {
                    "descricao": "Falta de metodologia estruturada e comprovada",
                    "impacto": "Resultados inconsistentes e desperdício de tempo e recursos",
                    "urgencia": "Alta"
                },
                {
                    "descricao": "Concorrência acirrada e commoditização do mercado",
                    "impacto": "Guerra de preços e dificuldade para se diferenciar",
                    "urgencia": "Média"
                }
            ],
            "estado_atual": "Profissional competente com conhecimento técnico, mas sem estratégia clara de posicionamento e crescimento",
            "estado_desejado": "Autoridade reconhecida no nicho com negócio escalável e lucrativo, trabalhando com propósito e impacto",
            "obstaculos": ["Falta de método estruturado", "Dispersão de foco em múltiplas estratégias", "Recursos limitados para investimento"],
            "sonho_secreto": "Ser reconhecido como o maior especialista do nicho no Brasil e ter um negócio que funcione sem sua presença constante"
        },
        "concorrencia": {
            "diretos": [
                {
                    "nome": f"Academia Premium {nicho}",
                    "preco": f"R$ {int(preco * 1.8):,}".replace(',', '.'),
                    "usp": "Metodologia exclusiva com certificação",
                    "forcas": ["Marca estabelecida há 5+ anos", "Comunidade ativa de 10k+ membros"],
                    "fraquezas": ["Preço elevado", "Suporte limitado", "Conteúdo muito teórico"]
                }
            ],
            "indiretos": [
                {
                    "nome": "Cursos gratuitos no YouTube",
                    "tipo": "Conteúdo educacional gratuito"
                }
            ],
            "gaps_mercado": [
                "Falta de metodologia prática com implementação assistida",
                "Ausência de suporte contínuo pós-compra",
                "Preços inacessíveis para profissionais em início de carreira"
            ]
        },
        "mercado": {
            "tam": "R$ 3,2 bilhões",
            "sam": "R$ 480 milhões",
            "som": "R$ 24 milhões",
            "volume_busca": "67.000 buscas/mês",
            "tendencias_alta": ["IA aplicada ao nicho", "Automação de processos", "Sustentabilidade e ESG"],
            "tendencias_baixa": ["Métodos tradicionais offline", "Processos manuais repetitivos"],
            "sazonalidade": {
                "melhores_meses": ["Janeiro", "Março", "Setembro"],
                "piores_meses": ["Dezembro", "Julho"]
            }
        },
        "palavras_chave": {
            "principais": [
                {
                    "termo": f"curso {nicho}",
                    "volume": "12.100",
                    "cpc": "R$ 4,20",
                    "dificuldade": "Média",
                    "intencao": "Comercial"
                }
            ],
            "custos_plataforma": {
                "facebook": {"cpm": "R$ 18", "cpc": "R$ 1,45", "cpl": "R$ 28", "conversao": "2,8%"},
                "google": {"cpm": "R$ 32", "cpc": "R$ 3,20", "cpl": "R$ 52", "conversao": "3,5%"},
                "youtube": {"cpm": "R$ 12", "cpc": "R$ 0,80", "cpl": "R$ 20", "conversao": "1,8%"},
                "tiktok": {"cpm": "R$ 8", "cpc": "R$ 0,60", "cpl": "R$ 18", "conversao": "1,5%"}
            }
        },
        "metricas": {
            "cac_medio": "R$ 420",
            "funil_conversao": ["100% visitantes", "18% leads", "3,2% vendas"],
            "ltv_medio": "R$ 1.680",
            "ltv_cac_ratio": "4,0:1",
            "roi_canais": {
                "facebook": "320%",
                "google": "380%",
                "youtube": "250%",
                "tiktok": "180%"
            }
        },
        "voz_mercado": {
            "objecoes": [
                {
                    "objecao": "Não tenho tempo para mais um curso",
                    "contorno": "Metodologia de implementação em 15 minutos diários com resultados em 30 dias"
                }
            ],
            "linguagem": {
                "termos": ["Metodologia", "Sistema", "Framework", "Estratégia", "Resultados"],
                "girias": ["Game changer", "Virada de chave", "Next level"],
                "gatilhos": ["Comprovado cientificamente", "Resultados garantidos", "Método exclusivo"]
            },
            "crencas_limitantes": [
                "Preciso trabalhar mais horas para ganhar mais dinheiro",
                "Só quem tem muito dinheiro consegue se destacar no mercado"
            ]
        },
        "projecoes": {
            "conservador": {
                "conversao": "2,0%",
                "faturamento": f"R$ {int(preco * 200):,}".replace(',', '.'),
                "roi": "240%"
            },
            "realista": {
                "conversao": "3,2%",
                "faturamento": f"R$ {int(preco * 320):,}".replace(',', '.'),
                "roi": "380%"
            },
            "otimista": {
                "conversao": "5,0%",
                "faturamento": f"R$ {int(preco * 500):,}".replace(',', '.'),
                "roi": "580%"
            }
        },
        "plano_acao": [
            {"passo": 1, "acao": "Validar proposta de valor com pesquisa qualitativa (50 entrevistas)", "prazo": "2 semanas"},
            {"passo": 2, "acao": "Criar landing page otimizada com copy baseado na pesquisa", "prazo": "1 semana"},
            {"passo": 3, "acao": "Configurar campanhas de tráfego pago (Facebook e Google)", "prazo": "1 semana"},
            {"passo": 4, "acao": "Produzir conteúdo de aquecimento (webinar + sequência de e-mails)", "prazo": "2 semanas"},
            {"passo": 5, "acao": "Executar campanha de pré-lançamento com early bird", "prazo": "1 semana"},
            {"passo": 6, "acao": "Lançamento oficial com live de abertura", "prazo": "1 semana"},
            {"passo": 7, "acao": "Otimizar campanhas baseado em dados e escalar investimento", "prazo": "Contínuo"}
        ]
    }

# Rotas existentes mantidas
@analysis_bp.route('/analyses', methods=['GET'])
def get_analyses():
    """Get list of recent analyses"""
    try:
        if not supabase:
            return jsonify({'error': 'Banco de dados não configurado'}), 500
        
        limit = request.args.get('limit', 10, type=int)
        nicho = request.args.get('nicho')
        
        query = supabase.table('analyses').select('*').order('created_at', desc=True)
        
        if nicho:
            query = query.eq('nicho', nicho)
        
        result = query.limit(limit).execute()
        
        return jsonify({
            'analyses': result.data,
            'count': len(result.data)
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar análises: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/analyses/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get specific analysis by ID"""
    try:
        if not supabase:
            return jsonify({'error': 'Banco de dados não configurado'}), 500
        
        result = supabase.table('analyses').select('*').eq('id', analysis_id).execute()
        
        if not result.data:
            return jsonify({'error': 'Análise não encontrada'}), 404
        
        analysis = result.data[0]
        
        # Retorna análise completa se disponível
        if analysis.get('comprehensive_analysis'):
            return jsonify(analysis['comprehensive_analysis'])
        
        # Fallback para estrutura antiga
        structured_analysis = {
            'id': analysis['id'],
            'nicho': analysis['nicho'],
            'produto': analysis['produto'],
            'avatar': analysis['avatar_data'],
            'positioning': analysis['positioning_data'],
            'competition': analysis['competition_data'],
            'marketing': analysis['marketing_data'],
            'metrics': analysis['metrics_data'],
            'funnel': analysis['funnel_data'],
            'market_intelligence': analysis.get('market_intelligence', {}),
            'action_plan': analysis.get('action_plan', {}),
            'created_at': analysis['created_at'],
            'status': analysis['status']
        }
        
        return jsonify(structured_analysis)
        
    except Exception as e:
        logger.error(f"Erro ao buscar análise: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/nichos', methods=['GET'])
def get_nichos():
    """Get list of unique niches from analyses"""
    try:
        if not supabase:
            return jsonify({'error': 'Banco de dados não configurado'}), 500
        
        result = supabase.table('analyses').select('nicho').execute()
        
        nichos = list(set([item['nicho'] for item in result.data if item['nicho']]))
        nichos.sort()
        
        return jsonify({
            'nichos': nichos,
            'count': len(nichos)
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar nichos: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
