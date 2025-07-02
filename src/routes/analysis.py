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

analysis_bp = Blueprint('analysis', __name__)

# Configure Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = None

if supabase_url and supabase_key:
    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Erro ao configurar Supabase: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DeepSeek client
try:
    deepseek_client = DeepSeekClient()
except Exception as e:
    logger.error(f"Erro ao inicializar DeepSeek: {e}")
    deepseek_client = None

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    """Análise completa de mercado com DeepSeek"""
    try:
        data = request.get_json()
        
        if not data or not data.get('nicho'):
            return jsonify({'error': 'Nicho é obrigatório'}), 400
        
        # Extract and validate form data
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
        
        # Validate and convert numeric fields
        try:
            analysis_data['preco_float'] = float(analysis_data['preco']) if analysis_data['preco'] else None
            analysis_data['objetivo_receita_float'] = float(analysis_data['objetivo_receita']) if analysis_data['objetivo_receita'] else None
            analysis_data['orcamento_marketing_float'] = float(analysis_data['orcamento_marketing']) if analysis_data['orcamento_marketing'] else None
        except ValueError:
            analysis_data['preco_float'] = None
            analysis_data['objetivo_receita_float'] = None
            analysis_data['orcamento_marketing_float'] = None
        
        # Save initial analysis record
        analysis_id = save_initial_analysis(analysis_data)
        
        # Generate comprehensive analysis with DeepSeek
        if deepseek_client:
            analysis_result = deepseek_client.analyze_avatar_comprehensive(analysis_data)
        else:
            # Fallback para análise básica se DeepSeek não estiver disponível
            analysis_result = create_fallback_analysis(analysis_data)
        
        # Update analysis record with results
        if supabase and analysis_id:
            update_analysis_record(analysis_id, analysis_result)
            analysis_result['analysis_id'] = analysis_id
        
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor', 'details': str(e)}), 500

def save_initial_analysis(data: Dict) -> Optional[int]:
    """Salva registro inicial da análise"""
    if not supabase:
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
            'status': 'processing',
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('analyses').insert(analysis_record).execute()
        if result.data:
            analysis_id = result.data[0]['id']
            logger.info(f"Análise criada no Supabase com ID: {analysis_id}")
            return analysis_id
    except Exception as e:
        logger.warning(f"Erro ao salvar no Supabase: {str(e)}")
    
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
        logger.info(f"Análise {analysis_id} atualizada no Supabase")
        
    except Exception as e:
        logger.warning(f"Erro ao atualizar análise no Supabase: {str(e)}")

def create_fallback_analysis(data: Dict) -> Dict:
    """Cria análise de fallback quando DeepSeek não está disponível"""
    nicho = data.get('nicho', '')
    produto = data.get('produto', 'Produto Digital')
    preco = data.get('preco_float', 997)
    
    return {
        "escopo": {
            "nicho_principal": nicho,
            "subnichos": [f"{nicho} para iniciantes", f"{nicho} avançado", f"{nicho} empresarial"],
            "produto_ideal": produto,
            "proposta_valor": f"A solução mais completa para dominar {nicho} no mercado brasileiro"
        },
        "avatar": {
            "demografia": {
                "faixa_etaria": "32-45 anos",
                "genero": "60% mulheres, 40% homens",
                "localizacao": "Região Sudeste (SP, RJ, MG)",
                "renda": "R$ 8.000 - R$ 25.000",
                "escolaridade": "Superior completo",
                "profissoes": ["Empreendedores", "Consultores", "Profissionais liberais", "Gestores"]
            },
            "psicografia": {
                "valores": ["Crescimento pessoal", "Independência financeira", "Reconhecimento profissional"],
                "estilo_vida": "Vida corrida, busca por eficiência, valoriza tempo de qualidade",
                "aspiracoes": ["Ser referência no nicho", "Ter liberdade financeira"],
                "medos": ["Ficar para trás", "Perder oportunidades", "Não conseguir resultados"],
                "frustracoes": ["Falta de tempo", "Excesso de informação"]
            },
            "comportamento_digital": {
                "plataformas": ["Instagram", "LinkedIn"],
                "horarios_pico": "19h-22h e 6h-8h",
                "conteudo_preferido": ["Vídeos educativos", "Cases de sucesso", "Dicas práticas"],
                "influenciadores": ["Especialistas do nicho", "Empreendedores de sucesso"]
            }
        },
        "dores_desejos": {
            "principais_dores": [
                {
                    "descricao": f"Dificuldade para se destacar em {nicho}",
                    "impacto": "Baixo reconhecimento e faturamento",
                    "urgencia": "Alta"
                },
                {
                    "descricao": "Falta de estratégia clara",
                    "impacto": "Desperdício de tempo e recursos",
                    "urgencia": "Alta"
                },
                {
                    "descricao": "Concorrência acirrada",
                    "impacto": "Dificuldade para conquistar clientes",
                    "urgencia": "Média"
                }
            ],
            "estado_atual": "Profissional com conhecimento, mas sem resultados consistentes",
            "estado_desejado": "Autoridade reconhecida no nicho com negócio próspero",
            "obstaculos": ["Falta de método", "Dispersão de foco", "Recursos limitados"],
            "sonho_secreto": "Ser reconhecido como o maior especialista do nicho no Brasil"
        },
        "concorrencia": {
            "diretos": [
                {
                    "nome": f"Curso Premium {nicho}",
                    "preco": f"R$ {int(preco * 1.5):,}",
                    "usp": "Metodologia exclusiva",
                    "forcas": ["Marca estabelecida", "Comunidade ativa"],
                    "fraquezas": ["Preço elevado", "Pouco suporte"]
                },
                {
                    "nome": f"Mentoria {nicho} Pro",
                    "preco": f"R$ {int(preco * 2):,}",
                    "usp": "Acompanhamento personalizado",
                    "forcas": ["Resultados comprovados", "Networking"],
                    "fraquezas": ["Vagas limitadas", "Processo seletivo"]
                }
            ],
            "indiretos": [
                {"nome": "Cursos gratuitos no YouTube", "tipo": "Conteúdo gratuito"},
                {"nome": "Livros especializados", "tipo": "Material didático"}
            ],
            "gaps_mercado": [
                "Falta de metodologia prática e aplicável",
                "Ausência de suporte contínuo",
                "Preços inacessíveis para a maioria"
            ]
        },
        "mercado": {
            "tam": "R$ 2,1 bilhões",
            "sam": "R$ 420 milhões",
            "som": "R$ 21 milhões",
            "volume_busca": "45.000 buscas/mês",
            "tendencias_alta": ["IA aplicada", "Automação", "Sustentabilidade"],
            "tendencias_baixa": ["Métodos tradicionais", "Processos manuais"],
            "sazonalidade": {
                "melhores_meses": ["Janeiro", "Março", "Setembro"],
                "piores_meses": ["Dezembro", "Julho"]
            }
        },
        "palavras_chave": {
            "principais": [
                {
                    "termo": f"curso {nicho}",
                    "volume": "8.100",
                    "cpc": "R$ 3,50",
                    "dificuldade": "Média",
                    "intencao": "Comercial"
                },
                {
                    "termo": f"como aprender {nicho}",
                    "volume": "5.400",
                    "cpc": "R$ 2,80",
                    "dificuldade": "Baixa",
                    "intencao": "Informacional"
                }
            ],
            "custos_plataforma": {
                "facebook": {"cpm": "R$ 15", "cpc": "R$ 1,20", "cpl": "R$ 25", "conversao": "2,5%"},
                "google": {"cpm": "R$ 25", "cpc": "R$ 2,50", "cpl": "R$ 45", "conversao": "3,2%"},
                "youtube": {"cpm": "R$ 12", "cpc": "R$ 0,80", "cpl": "R$ 20", "conversao": "1,8%"},
                "tiktok": {"cpm": "R$ 8", "cpc": "R$ 0,60", "cpl": "R$ 18", "conversao": "1,5%"}
            }
        },
        "metricas": {
            "cac_medio": "R$ 350",
            "funil_conversao": ["100% visitantes", "15% leads", "3% vendas"],
            "ltv_medio": "R$ 1.200",
            "ltv_cac_ratio": "3,4:1",
            "roi_canais": {
                "facebook": "280%",
                "google": "320%",
                "youtube": "250%",
                "tiktok": "180%"
            }
        },
        "projecoes": {
            "conservador": {
                "conversao": "1,5%",
                "faturamento": f"R$ {int(preco * 150):,}",
                "roi": "180%"
            },
            "realista": {
                "conversao": "2,5%",
                "faturamento": f"R$ {int(preco * 250):,}",
                "roi": "280%"
            },
            "otimista": {
                "conversao": "4,0%",
                "faturamento": f"R$ {int(preco * 400):,}",
                "roi": "450%"
            }
        },
        "plano_acao": [
            {"passo": 1, "acao": "Validar proposta de valor com pesquisa de mercado", "prazo": "1 semana"},
            {"passo": 2, "acao": "Criar landing page otimizada", "prazo": "2 semanas"},
            {"passo": 3, "acao": "Configurar campanhas de tráfego pago", "prazo": "1 semana"},
            {"passo": 4, "acao": "Produzir conteúdo de aquecimento", "prazo": "2 semanas"},
            {"passo": 5, "acao": "Lançar campanha de pré-venda", "prazo": "1 semana"},
            {"passo": 6, "acao": "Executar lançamento oficial", "prazo": "1 semana"},
            {"passo": 7, "acao": "Otimizar baseado nos resultados", "prazo": "Contínuo"}
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