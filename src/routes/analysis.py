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
        

# Configure Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    try:
        data = request.get_json()
        
        if not data or not data.get('nicho'):
            return jsonify({'error': 'Nicho é obrigatório'}), 400
        
        # Extract form data
        nicho = data.get('nicho', '')
        produto = data.get('produto', '')
        descricao = data.get('descricao', '')
        preco = data.get('preco', '')
        publico = data.get('publico', '')
        concorrentes = data.get('concorrentes', '')
        dados_adicionais = data.get('dadosAdicionais', '')
        
        # Save initial analysis record to Supabase
        analysis_id = None
        if supabase:
            try:
                analysis_record = {
                    'nicho': nicho,
                    'produto': produto,
                    'descricao': descricao,
                    'preco': float(preco) if preco else None,
                    'publico': publico,
                    'concorrentes': concorrentes,
                    'dados_adicionais': dados_adicionais,
                    'status': 'processing',
                    'created_at': datetime.utcnow().isoformat()
                }
                
                result = supabase.table('analyses').insert(analysis_record).execute()
                if result.data:
                    analysis_id = result.data[0]['id']
                    logger.info(f"Análise criada no Supabase com ID: {analysis_id}")
            except Exception as e:
                logger.warning(f"Erro ao salvar no Supabase: {str(e)}")
        
        # Generate analysis using Gemini AI
        analysis_result = generate_market_analysis(
            nicho, produto, descricao, preco, publico, concorrentes, dados_adicionais
        )
        
        # Update analysis record in Supabase with results
        if supabase and analysis_id:
            try:
                update_data = {
                    'avatar_data': analysis_result.get('avatar', {}),
                    'positioning_data': analysis_result.get('positioning', {}),
                    'competition_data': analysis_result.get('competition', {}),
                    'marketing_data': analysis_result.get('marketing', {}),
                    'metrics_data': analysis_result.get('metrics', {}),
                    'funnel_data': analysis_result.get('funnel', {}),
                    'status': 'completed',
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                supabase.table('analyses').update(update_data).eq('id', analysis_id).execute()
                logger.info(f"Análise {analysis_id} atualizada no Supabase")
                
                # Add analysis_id to response
                analysis_result['analysis_id'] = analysis_id
                
            except Exception as e:
                logger.warning(f"Erro ao atualizar análise no Supabase: {str(e)}")
        
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/analyses', methods=['GET'])
def get_analyses():
    """Get list of recent analyses"""
    try:
        if not supabase:
            return jsonify({'error': 'Banco de dados não configurado'}), 500
        
        # Get query parameters
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
        
        # Structure the response
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
        
        # Extract unique niches
        nichos = list(set([item['nicho'] for item in result.data if item['nicho']]))
        nichos.sort()
        
        return jsonify({
            'nichos': nichos,
            'count': len(nichos)
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar nichos: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

def generate_market_analysis(nicho, produto, descricao, preco, publico, concorrentes, dados_adicionais):
    """Generate comprehensive market analysis using Gemini AI"""
    
    # Create the prompt for Gemini
    prompt = create_analysis_prompt(nicho, produto, descricao, preco, publico, concorrentes, dados_adicionais)
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Parse the response and structure it
        analysis_text = response.text
        
        # Structure the analysis into the expected format
        structured_analysis = structure_analysis_response(analysis_text, nicho, produto, preco)
        
        return structured_analysis
        
    except Exception as e:
        logger.error(f"Erro ao gerar análise com Gemini: {str(e)}")
        # Return fallback analysis
        return create_fallback_analysis(nicho, produto, preco)

def create_analysis_prompt(nicho, produto, descricao, preco, publico, concorrentes, dados_adicionais):
    """Create a comprehensive prompt for Gemini AI analysis"""
    
    prompt = f"""
Você é um especialista em análise de mercado e estratégia de lançamento de produtos. Sua tarefa é criar uma análise completa e detalhada baseada nas informações fornecidas.

INFORMAÇÕES DO PRODUTO:
- Nicho: {nicho}
- Produto/Serviço: {produto if produto else 'Não especificado'}
- Descrição: {descricao if descricao else 'Não fornecida'}
- Preço: R$ {preco if preco else 'Não definido'}
- Público-Alvo: {publico if publico else 'Não especificado'}
- Concorrentes: {concorrentes if concorrentes else 'Não informados'}
- Dados Adicionais: {dados_adicionais if dados_adicionais else 'Nenhum'}

INSTRUÇÕES PARA ANÁLISE:

1. PERFIL DO AVATAR:
- Crie um avatar detalhado com nome, idade, profissão e contexto
- Identifique a barreira crítica (problema principal)
- Defina o estado desejado (objetivo final)
- Liste 3-5 frustrações diárias específicas
- Identifique a crença limitante principal

2. ESTRATÉGIA DE POSICIONAMENTO:
- Crie uma declaração de posicionamento única
- Desenvolva 3 ângulos de mensagem (lógico, emocional, contraste)
- Defina a proposta de valor irrefutável

3. ANÁLISE COMPETITIVA:
- Analise pelo menos 2-3 concorrentes diretos
- Identifique forças e fraquezas de cada um
- Encontre lacunas no mercado
- Sugira oportunidades de diferenciação

4. MATERIAIS DE MARKETING:
- Crie headline para landing page
- Desenvolva estrutura de página de vendas
- Sugira 3 assuntos de e-mail para sequência
- Crie 3 roteiros de anúncios de 15 segundos

5. PROJEÇÕES FINANCEIRAS:
- Estime leads necessários para o faturamento
- Calcule taxa de conversão realista
- Projete faturamento mensal/anual
- Calcule ROI esperado
- Distribua investimento por canal

6. FUNIL DE VENDAS:
- Defina 4-5 fases do funil
- Estabeleça cronograma de execução
- Sugira métricas de acompanhamento

FORMATO DE RESPOSTA:
Responda em formato JSON estruturado com as seguintes seções:
- avatar (nome, contexto, barreira_critica, estado_desejado, frustracoes[], crenca_limitante)
- positioning (declaracao, angulos[])
- competition (concorrentes[], lacunas[])
- marketing (landing_page, emails[], anuncios[])
- metrics (leads_projetados, conversao, faturamento, roi, investimento[])
- funnel (fases[], cronograma[])

Seja específico, prático e baseie-se em dados reais do mercado brasileiro. Use linguagem profissional mas acessível.
"""
    
    return prompt

def structure_analysis_response(analysis_text, nicho, produto, preco):
    """Structure the Gemini response into the expected format"""
    
    try:
        # Try to parse JSON if Gemini returned structured data
        if analysis_text.strip().startswith('{'):
            return json.loads(analysis_text)
    except:
        pass
    
    # If not JSON, create structured response from text
    return create_structured_analysis(analysis_text, nicho, produto, preco)

def create_structured_analysis(analysis_text, nicho, produto, preco):
    """Create structured analysis from text response"""
    
    # Extract price as number
    try:
        preco_num = float(preco) if preco else 997
    except:
        preco_num = 997
    
    # Calculate projections
    leads_projetados = 2500
    conversao = 1.5
    vendas = int(leads_projetados * (conversao / 100))
    faturamento = int(vendas * preco_num)
    investimento_total = 20000
    roi = int(((faturamento - investimento_total) / investimento_total) * 100)
    
    return {
        "avatar": {
            "nome": f"Avatar Ideal - {nicho}",
            "contexto": f"Profissional de 32-45 anos interessado em {nicho}, com renda familiar entre R$ 8.000 e R$ 25.000",
            "barreira_critica": f"Dificuldades para alcançar resultados consistentes em {nicho}",
            "estado_desejado": f"Dominar {nicho} e alcançar resultados excepcionais",
            "frustracoes": [
                f"Falta de conhecimento especializado em {nicho}",
                f"Dificuldade para implementar estratégias em {nicho}",
                f"Resultados inconsistentes",
                f"Falta de tempo para se dedicar ao aprendizado",
                f"Insegurança sobre qual caminho seguir"
            ],
            "crenca_limitante": f"Acredita que {nicho} é muito complexo ou que não tem capacidade para dominar a área"
        },
        "positioning": {
            "declaracao": f"Para profissionais que buscam excelência em {nicho}, {produto} é a única solução que combina conhecimento prático com resultados comprovados, permitindo alcançar o sucesso desejado de forma estruturada e eficiente.",
            "angulos": [
                {
                    "tipo": "Lógico - Focado na Dor",
                    "mensagem": f"Pare de lutar com as dificuldades em {nicho}. Nossa metodologia elimina as principais barreiras e acelera seus resultados."
                },
                {
                    "tipo": "Emocional - Focado no Desejo", 
                    "mensagem": f"Imagine ter total confiança e domínio em {nicho}, alcançando os resultados que sempre sonhou."
                },
                {
                    "tipo": "Contraste - Focado na Concorrência",
                    "mensagem": f"Enquanto outros oferecem teoria, nós entregamos um sistema prático e comprovado para {nicho}."
                }
            ]
        },
        "competition": {
            "concorrentes": [
                {
                    "nome": f"Concorrente A - {nicho}",
                    "preco": int(preco_num * 1.2),
                    "forcas": "Marca estabelecida no mercado",
                    "fraquezas": "Abordagem muito teórica, pouco prática",
                    "oportunidade": "Foco em aplicação prática e resultados rápidos"
                },
                {
                    "nome": f"Concorrente B - {nicho}",
                    "preco": int(preco_num * 0.8),
                    "forcas": "Preço mais acessível",
                    "fraquezas": "Conteúdo superficial, sem suporte adequado",
                    "oportunidade": "Oferecer conteúdo aprofundado com suporte premium"
                }
            ],
            "lacunas": [
                f"Falta de metodologia estruturada em {nicho}",
                "Ausência de suporte personalizado",
                "Pouco foco em resultados práticos",
                "Falta de comunidade engajada"
            ]
        },
        "marketing": {
            "landing_page": {
                "headline": f"Domine {nicho} em 30 Dias com o Método Comprovado",
                "secoes": [
                    {
                        "titulo": "Identificação com a Dor",
                        "conteudo": f"Se você está lutando para obter resultados em {nicho}..."
                    },
                    {
                        "titulo": "Apresentação da Solução",
                        "conteudo": f"Apresentamos {produto}, o método definitivo para {nicho}"
                    },
                    {
                        "titulo": "Prova Social",
                        "conteudo": "Veja os resultados de nossos alunos"
                    },
                    {
                        "titulo": "Oferta",
                        "conteudo": f"Acesso completo por apenas R$ {preco_num}"
                    }
                ]
            },
            "emails": [
                {
                    "tipo": "Pré-lançamento",
                    "assunto": f"O erro que 90% das pessoas cometem em {nicho}",
                    "preview": f"Descubra o principal erro que impede o sucesso em {nicho}..."
                },
                {
                    "tipo": "Lançamento", 
                    "assunto": f"🚀 {produto} - Vagas Abertas (Limitadas)",
                    "preview": f"As inscrições para {produto} estão oficialmente abertas..."
                },
                {
                    "tipo": "Última Chance",
                    "assunto": "⏰ Última chance - Encerra à meia-noite",
                    "preview": "Esta é sua última oportunidade de garantir sua vaga..."
                }
            ],
            "anuncios": [
                {
                    "angulo": "Dor",
                    "roteiro": f"Cansado de não conseguir resultados em {nicho}? Descubra o método que já transformou centenas de vidas."
                },
                {
                    "angulo": "Desejo",
                    "roteiro": f"Imagine dominar {nicho} completamente. Com {produto}, isso é possível em apenas 30 dias."
                },
                {
                    "angulo": "Contraste",
                    "roteiro": f"Enquanto outros prometem, nós entregamos. {produto} é o único método com resultados comprovados em {nicho}."
                }
            ]
        },
        "metrics": {
            "leads_projetados": leads_projetados,
            "conversao": conversao,
            "faturamento": faturamento,
            "roi": roi,
            "investimento": [
                {"canal": "Meta Ads", "percentual": 60, "valor": 12000},
                {"canal": "Google Ads", "percentual": 30, "valor": 6000},
                {"canal": "Parcerias", "percentual": 10, "valor": 2000}
            ]
        },
        "funnel": {
            "fases": [
                {
                    "nome": "Captura de Leads",
                    "duracao": "2 semanas",
                    "objetivo": "Capturar 2.500 leads qualificados",
                    "acoes": [
                        "Lançar campanhas de tráfego pago",
                        "Ativar parcerias com influenciadores",
                        "Criar conteúdo educacional"
                    ]
                },
                {
                    "nome": "Aquecimento",
                    "duracao": "1 semana", 
                    "objetivo": "Educar e aquecer os leads",
                    "acoes": [
                        "Enviar sequência de e-mails educacionais",
                        "Realizar lives no Instagram",
                        "Compartilhar cases de sucesso"
                    ]
                },
                {
                    "nome": "Evento de Lançamento",
                    "duracao": "3 dias",
                    "objetivo": "Apresentar a oferta e gerar interesse",
                    "acoes": [
                        "Realizar evento online gratuito",
                        "Apresentar o método",
                        "Revelar a oferta"
                    ]
                },
                {
                    "nome": "Período de Vendas",
                    "duracao": "5 dias",
                    "objetivo": "Converter leads em vendas",
                    "acoes": [
                        "Abrir carrinho de compras",
                        "Enviar sequência de fechamento",
                        "Criar urgência e escassez"
                    ]
                }
            ],
            "cronograma": [
                {
                    "periodo": "Semana 1-2",
                    "atividade": "Preparação e Captura",
                    "descricao": "Configurar campanhas e capturar leads"
                },
                {
                    "periodo": "Semana 3",
                    "atividade": "Aquecimento",
                    "descricao": "Educar e preparar audiência"
                },
                {
                    "periodo": "Semana 4",
                    "atividade": "Lançamento",
                    "descricao": "Evento e período de vendas"
                }
            ]
        }
    }

def create_fallback_analysis(nicho, produto, preco):
    """Create a fallback analysis if Gemini fails"""
    
    try:
        preco_num = float(preco) if preco else 997
    except:
        preco_num = 997
    
    return {
        "avatar": {
            "nome": f"Profissional {nicho}",
            "contexto": f"Pessoa interessada em {nicho} buscando conhecimento e resultados",
            "barreira_critica": f"Dificuldades para obter sucesso em {nicho}",
            "estado_desejado": f"Dominar {nicho} e alcançar objetivos",
            "frustracoes": [
                "Falta de conhecimento especializado",
                "Resultados inconsistentes", 
                "Falta de direcionamento claro"
            ],
            "crenca_limitante": f"Acredita que {nicho} é muito difícil"
        },
        "positioning": {
            "declaracao": f"{produto} é a solução definitiva para quem quer dominar {nicho}",
            "angulos": [
                {"tipo": "Lógico", "mensagem": f"Método comprovado para {nicho}"},
                {"tipo": "Emocional", "mensagem": f"Realize seus sonhos em {nicho}"},
                {"tipo": "Contraste", "mensagem": f"Único método realmente eficaz para {nicho}"}
            ]
        },
        "competition": {
            "concorrentes": [
                {"nome": "Concorrente A", "preco": int(preco_num * 1.2), "forcas": "Marca conhecida", "fraquezas": "Muito teórico", "oportunidade": "Foco prático"}
            ],
            "lacunas": ["Falta de metodologia clara", "Pouco suporte"]
        },
        "marketing": {
            "landing_page": {"headline": f"Domine {nicho} Agora", "secoes": []},
            "emails": [],
            "anuncios": []
        },
        "metrics": {
            "leads_projetados": 2500,
            "conversao": 1.5,
            "faturamento": int(2500 * 0.015 * preco_num),
            "roi": 89,
            "investimento": []
        },
        "funnel": {
            "fases": [],
            "cronograma": []
        }
    }

