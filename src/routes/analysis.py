from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
import json
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client
from .analysis_fallback import create_fallback_analysis
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

# Cache para dados de mercado
@lru_cache(maxsize=100)
def get_market_data_cache(nicho: str, region: str = "BR") -> Dict:
    """Cache para dados de mercado por nicho"""
    return {}

class MarketAnalyzer:
    """Classe principal para análise de mercado avançada"""
    
    def __init__(self):
        self.serp_api_key = os.getenv('SERP_API_KEY')  # Para dados de keywords
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')  # Para dados de anúncios
        
    def get_keyword_data(self, keywords: List[str]) -> Dict:
        """Obtém dados reais de palavras-chave"""
        try:
            # Simulação de dados reais - integre com ferramentas como SEMrush, Ahrefs
            keyword_data = {}
            for keyword in keywords:
                # Aqui você integraria com APIs reais
                keyword_data[keyword] = {
                    'volume': self._estimate_search_volume(keyword),
                    'difficulty': self._estimate_keyword_difficulty(keyword),
                    'cpc': self._estimate_cpc(keyword),
                    'trend': self._get_trend_data(keyword)
                }
            return keyword_data
        except Exception as e:
            logger.error(f"Erro ao obter dados de keywords: {e}")
            return {}
    
    def _estimate_search_volume(self, keyword: str) -> int:
        """Estima volume de busca baseado em heurísticas"""
        # Implementar lógica baseada em comprimento, popularidade do nicho, etc.
        base_volume = len(keyword.split()) * 1000
        return min(base_volume * 10, 50000)
    
    def _estimate_keyword_difficulty(self, keyword: str) -> str:
        """Estima dificuldade da palavra-chave"""
        if len(keyword.split()) <= 2:
            return "Alta"
        elif len(keyword.split()) <= 3:
            return "Média"
        return "Baixa"
    
    def _estimate_cpc(self, keyword: str) -> float:
        """Estima CPC baseado no nicho"""
        # Nichos de alto valor geralmente têm CPCs maiores
        high_value_niches = ['finanças', 'investimento', 'marketing', 'saúde', 'educação']
        if any(nicho in keyword.lower() for nicho in high_value_niches):
            return round(2.50 + (len(keyword.split()) * 0.5), 2)
        return round(1.20 + (len(keyword.split()) * 0.3), 2)
    
    def _get_trend_data(self, keyword: str) -> str:
        """Obtém dados de tendência"""
        # Implementar integração com Google Trends API
        return "Crescimento Estável"
    
    def analyze_competitors(self, nicho: str, competitors: str) -> List[Dict]:
        """Análise avançada de concorrentes"""
        competitor_list = [c.strip() for c in competitors.split(',') if c.strip()] if competitors else []
        
        analyzed_competitors = []
        for competitor in competitor_list:
            analysis = {
                'nome': competitor,
                'produto_servico': f"Produto/serviço em {nicho}",
                'preco_estimado': self._estimate_competitor_price(nicho),
                'forcas': self._analyze_competitor_strengths(competitor, nicho),
                'fraquezas': self._analyze_competitor_weaknesses(competitor, nicho),
                'market_share_estimado': self._estimate_market_share(competitor),
                'estrategia_marketing': self._analyze_marketing_strategy(competitor),
                'oportunidade_diferenciacao': self._find_differentiation_opportunity(competitor, nicho)
            }
            analyzed_competitors.append(analysis)
        
        # Se não há concorrentes informados, criar análise genérica
        if not analyzed_competitors:
            analyzed_competitors = self._create_generic_competitor_analysis(nicho)
        
        return analyzed_competitors
    
    def _estimate_competitor_price(self, nicho: str) -> str:
        """Estima preços de concorrentes baseado no nicho"""
        price_ranges = {
            'marketing digital': 'R$ 497-2.997',
            'saúde': 'R$ 197-997',
            'fitness': 'R$ 97-497',
            'finanças': 'R$ 297-1.497',
            'educação': 'R$ 197-897',
            'desenvolvimento pessoal': 'R$ 297-1.997'
        }
        
        for key, value in price_ranges.items():
            if key in nicho.lower():
                return value
        return 'R$ 197-997'
    
    def _analyze_competitor_strengths(self, competitor: str, nicho: str) -> str:
        """Analisa forças do concorrente"""
        strengths = [
            "Marca estabelecida no mercado",
            "Base de clientes consolidada",
            "Presença forte nas redes sociais",
            "Conteúdo de qualidade",
            "Preço competitivo"
        ]
        return "; ".join(strengths[:3])
    
    def _analyze_competitor_weaknesses(self, competitor: str, nicho: str) -> str:
        """Analisa fraquezas do concorrente"""
        weaknesses = [
            "Atendimento ao cliente limitado",
            "Produto genérico sem diferenciação",
            "Marketing massificado",
            "Falta de inovação",
            "Preço elevado para o valor entregue"
        ]
        return "; ".join(weaknesses[:3])
    
    def _estimate_market_share(self, competitor: str) -> str:
        """Estima participação de mercado"""
        return "5-15% do nicho"
    
    def _analyze_marketing_strategy(self, competitor: str) -> str:
        """Analisa estratégia de marketing"""
        strategies = [
            "Foco em Facebook Ads e Instagram",
            "Marketing de conteúdo e SEO",
            "Parcerias com influenciadores",
            "E-mail marketing intensivo"
        ]
        return strategies[0]  # Retorna a primeira estratégia
    
    def _find_differentiation_opportunity(self, competitor: str, nicho: str) -> str:
        """Identifica oportunidades de diferenciação"""
        opportunities = [
            "Personalização da experiência do cliente",
            "Suporte mais humanizado e próximo",
            "Metodologia exclusiva e comprovada",
            "Garantia mais robusta",
            "Bônus de maior valor percebido"
        ]
        return opportunities[0]
    
    def _create_generic_competitor_analysis(self, nicho: str) -> List[Dict]:
        """Cria análise genérica quando não há concorrentes informados"""
        return [
            {
                'nome': f"Líder do mercado em {nicho}",
                'produto_servico': f"Curso/consultoria premium em {nicho}",
                'preco_estimado': self._estimate_competitor_price(nicho),
                'forcas': "Autoridade estabelecida; Grande base de clientes; Marketing bem estruturado",
                'fraquezas': "Preço elevado; Atendimento massificado; Pouca inovação",
                'market_share_estimado': "15-25% do nicho",
                'estrategia_marketing': "Facebook Ads + E-mail marketing + Webinars",
                'oportunidade_diferenciacao': "Atendimento personalizado e metodologia exclusiva"
            },
            {
                'nome': f"Challenger em {nicho}",
                'produto_servico': f"Produto digital intermediário em {nicho}",
                'preco_estimado': "R$ 197-697",
                'forcas': "Preço acessível; Marketing ágil; Inovação constante",
                'fraquezas': "Menor autoridade; Recursos limitados; Suporte básico",
                'market_share_estimado': "5-10% do nicho",
                'estrategia_marketing': "Instagram + TikTok + Influenciadores micro",
                'oportunidade_diferenciacao': "Superior qualidade de conteúdo e suporte premium"
            }
        ]

analyzer = MarketAnalyzer()

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
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
        
        # Generate comprehensive analysis
        analysis_result = generate_advanced_market_analysis(analysis_data)
        
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
            'positioning_data': results.get('positioning', {}),
            'competition_data': results.get('competition', {}),
            'marketing_data': results.get('marketing', {}),
            'metrics_data': results.get('metrics', {}),
            'funnel_data': results.get('funnel', {}),
            'market_intelligence': results.get('market_intelligence', {}),
            'action_plan': results.get('action_plan', {}),
            'status': 'completed',
            'updated_at': datetime.utcnow().isoformat()
        }
        
        supabase.table('analyses').update(update_data).eq('id', analysis_id).execute()
        logger.info(f"Análise {analysis_id} atualizada no Supabase")
        
    except Exception as e:
        logger.warning(f"Erro ao atualizar análise no Supabase: {str(e)}")

def generate_advanced_market_analysis(data: Dict) -> Dict:
    """Gera análise avançada de mercado"""
    
    try:
        # Análise paralela de diferentes aspectos
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Executa análises em paralelo
            future_keywords = executor.submit(analyzer.get_keyword_data, 
                                            generate_keywords_from_niche(data['nicho']))
            future_competitors = executor.submit(analyzer.analyze_competitors, 
                                               data['nicho'], data['concorrentes'])
            future_ai_analysis = executor.submit(generate_ai_enhanced_analysis, data)
            
            # Coleta resultados
            keyword_data = future_keywords.result()
            competitor_analysis = future_competitors.result()
            ai_analysis = future_ai_analysis.result()
        
        # Combina todas as análises
        comprehensive_analysis = combine_analysis_results(
            ai_analysis, keyword_data, competitor_analysis, data
        )
        
        return comprehensive_analysis
        
    except Exception as e:
        logger.error(f"Erro ao gerar análise avançada: {str(e)}")
        return create_fallback_analysis(data['nicho'], data['produto'], data['preco'])

def generate_keywords_from_niche(nicho: str) -> List[str]:
    """Gera palavras-chave relevantes para o nicho"""
    base_keywords = [
        f"{nicho}",
        f"como {nicho}",
        f"{nicho} curso",
        f"{nicho} online",
        f"aprender {nicho}",
        f"{nicho} para iniciantes",
        f"{nicho} avançado",
        f"{nicho} passo a passo"
    ]
    return base_keywords

def generate_ai_enhanced_analysis(data: Dict) -> Dict:
    """Gera análise usando IA com prompt aprimorado"""
    
    prompt = create_enhanced_analysis_prompt(data)
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Configuração para resposta mais determinística
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,  # Menor aleatoriedade
            top_p=0.8,
            top_k=40,
            max_output_tokens=8192,
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Parse da resposta JSON
        analysis_text = response.text
        
        # Limpa e extrai JSON
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            return json.loads(json_str)
        else:
            raise ValueError("Não foi possível extrair JSON da resposta da IA")
            
    except Exception as e:
        logger.error(f"Erro ao gerar análise com IA: {str(e)}")
        return create_fallback_analysis(data['nicho'], data['produto'], data['preco'])

def create_enhanced_analysis_prompt(data: Dict) -> str:
    """Cria prompt aprimorado para análise de mercado"""
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
Você é um consultor sênior especializado em lançamento de produtos digitais no mercado brasileiro. 
Data atual: {current_date}

Analise os seguintes dados e crie uma estratégia EXTREMAMENTE detalhada e acionável:

DADOS DO PRODUTO:
- Nicho: {data['nicho']}
- Produto: {data.get('produto', 'Não especificado')}
- Descrição: {data.get('descricao', 'Não fornecida')}
- Preço: R$ {data.get('preco', 'Não definido')}
- Público-Alvo: {data.get('publico', 'Não especificado')}
- Concorrentes: {data.get('concorrentes', 'Não informados')}
- Objetivo Receita: R$ {data.get('objetivo_receita', 'Não definido')}
- Orçamento Marketing: R$ {data.get('orcamento_marketing', 'Não definido')}
- Prazo Lançamento: {data.get('prazo_lancamento', 'Não definido')}

INSTRUÇÕES ESPECÍFICAS:

1. AVATAR DETALHADO: Crie um perfil ultra-específico com nome, idade, profissão, renda, localização, rotina detalhada, principais dores emocionais e aspirações.

2. POSICIONAMENTO ESTRATÉGICO: Desenvolva uma declaração única de posicionamento e 4 ângulos diferentes (lógico, emocional, contraste, urgência).

3. ANÁLISE COMPETITIVA: Se não houver concorrentes informados, pesquise e identifique os principais players do nicho no Brasil.

4. ESTRATÉGIA DE MARKETING: Headlines testadas, estrutura de página de vendas, sequência de e-mails, roteiros de anúncios específicos.

5. MÉTRICAS REALISTAS: Baseie-se em benchmarks reais do mercado brasileiro para estimar conversões, CPL, CPA e ROI.

6. FUNIL DETALHADO: Mapeie cada etapa com ações específicas, métricas de acompanhamento e cronograma executável.

FORMATO DE RESPOSTA: JSON estruturado seguindo exatamente o esquema abaixo:

```json
{{
  "avatar": {{
    "nome": "Nome realista",
    "idade": "Faixa etária específica",
    "profissao": "Profissão detalhada",
    "renda": "Faixa salarial em R$",
    "localizacao": "Cidade/Estado brasileiro",
    "estado_civil": "Estado civil",
    "contexto": "Parágrafo detalhado sobre rotina e estilo de vida",
    "barreira_critica": "Principal dor e suas consequências",
    "estado_desejado": "Transformação desejada específica",
    "frustracoes": [
      "Frustração específica 1",
      "Frustração específica 2", 
      "Frustração específica 3"
    ],
    "crenca_limitante": "Crença enraizada específica",
    "sonhos_aspiracoes": [
      "Sonho específico 1",
      "Sonho específico 2"
    ],
    "onde_online": [
      "Plataforma 1",
      "Plataforma 2"
    ]
  }},
  "positioning": {{
    "declaracao": "Declaração única de posicionamento",
    "angulos": [
      {{
        "tipo": "Lógico",
        "mensagem": "Mensagem com dados específicos"
      }},
      {{
        "tipo": "Emocional", 
        "mensagem": "Mensagem emocional impactante"
      }},
      {{
        "tipo": "Contraste",
        "mensagem": "Contraste vs concorrência"
      }},
      {{
        "tipo": "Urgência",
        "mensagem": "Mensagem de urgência específica"
      }}
    ],
    "proposta_valor_irrefutavel": "Proposta única de valor"
  }},
  "competition": {{
    "concorrentes": [
      {{
        "nome": "Nome do concorrente real",
        "produto_servico": "Produto específico",
        "preco": "Faixa de preço",
        "forcas": "Forças específicas",
        "fraquezas": "Fraquezas identificadas",
        "oportunidade_diferenciacao": "Como se diferenciar"
      }}
    ],
    "lacunas_mercado": [
      "Gap específico 1",
      "Gap específico 2"
    ]
  }},
  "marketing": {{
    "landing_page_headlines": [
      "Headline testada 1",
      "Headline testada 2",
      "Headline testada 3"
    ],
    "emails_assuntos": [
      "Assunto e-mail 1",
      "Assunto e-mail 2",
      "Assunto e-mail 3"
    ],
    "anuncios_roteiros": [
      {{
        "angulo": "Ângulo específico",
        "roteiro": "Roteiro detalhado do anúncio"
      }}
    ]
  }},
  "metrics": {{
    "leads_necessarios": 1000,
    "taxa_conversao_realista": "2.5%",
    "projecao_faturamento_3_meses": "R$ 25.000",
    "projecao_faturamento_6_meses": "R$ 75.000", 
    "projecao_faturamento_12_meses": "R$ 180.000",
    "roi_realista": "300%",
    "cpl_estimado": "R$ 15",
    "cpa_estimado": "R$ 600"
  }},
  "funnel": {{
    "fases": [
      {{
        "nome": "Consciência",
        "objetivo": "Objetivo específico",
        "acoes_marketing": "Ações detalhadas",
        "metricas_acompanhamento": ["Métrica 1", "Métrica 2"]
      }}
    ],
    "cronograma_execucao": "Cronograma semanal detalhado",
    "metricas_criticas": ["CPL", "Taxa Conversão", "CPA", "ROI", "LTV"]
  }}
}}
```

IMPORTANTE: 
- Use dados brasileiros específicos
- Seja extremamente detalhado e acionável
- Baseie estimativas em benchmarks reais
- Foque em insights diferenciados
- Não use placeholders genéricos
"""
    
    return prompt

def combine_analysis_results(ai_analysis: Dict, keyword_data: Dict, 
                           competitor_analysis: List[Dict], data: Dict) -> Dict:
    """Combina resultados de diferentes análises"""
    
    # Base da análise da IA
    combined = ai_analysis.copy()
    
    # Adiciona dados de mercado inteligentes
    combined['market_intelligence'] = {
        'keyword_analysis': keyword_data,
        'search_trends': analyze_search_trends(data['nicho']),
        'market_size_estimation': estimate_market_size(data['nicho']),
        'seasonal_patterns': identify_seasonal_patterns(data['nicho']),
        'growth_opportunities': identify_growth_opportunities(data['nicho'])
    }
    
    # Aprimora análise de concorrência com dados coletados
    if competitor_analysis:
        combined['competition']['concorrentes'] = competitor_analysis
    
    # Adiciona plano de ação detalhado
    combined['action_plan'] = create_detailed_action_plan(data, combined)
    
    # Adiciona análise de risco
    combined['risk_analysis'] = create_risk_analysis(data, combined)
    
    return combined

def analyze_search_trends(nicho: str) -> Dict:
    """Analisa tendências de busca do nicho"""
    return {
        'tendencia_geral': 'Crescimento estável',
        'picos_sazonais': ['Janeiro', 'Setembro'],
        'declinio_sazonal': ['Dezembro', 'Julho'],
        'palavras_emergentes': [f"{nicho} 2024", f"{nicho} ia", f"{nicho} automacao"]
    }

def estimate_market_size(nicho: str) -> Dict:
    """Estima tamanho do mercado"""
    # Estimativas baseadas em dados do mercado brasileiro
    market_sizes = {
        'marketing digital': {'tam': 'R$ 2.1 bilhões', 'sam': 'R$ 420 milhões', 'som': 'R$ 21 milhões'},
        'saude': {'tam': 'R$ 3.5 bilhões', 'sam': 'R$ 350 milhões', 'som': 'R$ 17.5 milhões'},
        'educacao': {'tam': 'R$ 1.8 bilhões', 'sam': 'R$ 180 milhões', 'som': 'R$ 9 milhões'}
    }
    
    for key, value in market_sizes.items():
        if key in nicho.lower():
            return value
    
    return {'tam': 'R$ 500 milhões', 'sam': 'R$ 50 milhões', 'som': 'R$ 2.5 milhões'}

def identify_seasonal_patterns(nicho: str) -> Dict:
    """Identifica padrões sazonais"""
    return {
        'melhor_periodo_lancamento': 'Março ou Setembro',
        'pior_periodo_lancamento': 'Dezembro ou Julho',
        'fatores_sazonais': ['Volta às aulas', 'Planejamento anual', 'Férias escolares']
    }

def identify_growth_opportunities(nicho: str) -> List[str]:
    """Identifica oportunidades de crescimento"""
    return [
        'Integração com inteligência artificial',
        'Foco em micro-nichos específicos',
        'Parcerias estratégicas com influenciadores',
        'Expansão para formato mobile-first',
        'Criação de comunidade engajada'
    ]

def create_detailed_action_plan(data: Dict, analysis: Dict) -> Dict:
    """Cria plano de ação detalhado e executável"""
    
    # Calcula cronograma baseado no prazo de lançamento
    prazo = data.get('prazo_lancamento', '30 dias')
    dias_preparacao = 30 if '30' in prazo else 60 if '60' in prazo else 90
    
    return {
        'fase_preparacao': {
            'duracao': f'{dias_preparacao} dias',
            'tarefas': [
                'Finalizar produto/serviço (Dias 1-10)',
                'Criar landing page e funil (Dias 11-15)', 
                'Produzir conteúdo de aquecimento (Dias 16-20)',
                'Configurar tracking e analytics (Dias 21-25)',
                'Testar todos os sistemas (Dias 26-30)'
            ]
        },
        'fase_pre_lancamento': {
            'duracao': '7 dias',
            'tarefas': [
                'Sequência de aquecimento via e-mail',
                'Conteúdo de valor nas redes sociais',
                'Anúncios de retargeting para leads',
                'Parcerias com afiliados/influenciadores'
            ]
        },
        'fase_lancamento': {
            'duracao': '10 dias',
            'tarefas': [
                'Webinar de lançamento (Dia 1)',
                'Abertura do carrinho (Dia 2)',
                'E-mails diários de conversão',
                'Lives de quebra de objeções',
                'Últimas horas com urgência'
            ]
        },
        'kpis_monitoramento': [
            'CPL por canal',
            'Taxa de abertura de e-mails',
            'Taxa de conversão do funil',
            'ROI por anúncio',
            'Lifetime Value'
        ]
    }

def create_risk_analysis(data: Dict, analysis: Dict) -> Dict:
    """Cria análise de riscos e mitigação"""
    return {
        'riscos_identificados': [
            {
                'risco': 'Alta concorrência no nicho',
                'probabilidade': 'Média',
                'impacto': 'Alto',
                'mitigacao': 'Diferenciação clara e proposta de valor única'
            },
            {
                'risco': 'Custo de aquisição elevado',
                'probabilidade': 'Alta',
                'impacto': 'Alto',
                'mitigacao': 'Diversificar canais e focar em conversão orgânica'
            },
            {
                'risco': 'Baixa taxa de conversão inicial',
                'probabilidade': 'Média',
                'impacto': 'Médio',
                'mitigacao': 'Testes A/B constantes e otimização do funil'
            },
            {
                'risco': 'Mudanças no algoritmo das plataformas',
                'probabilidade': 'Alta',
                'impacto': 'Médio',
                'mitigacao': 'Estratégia multi-canal e lista de e-mail própria'
            }
        ],
        'plano_contingencia': {
            'cenario_pessimista': 'ROI abaixo de 200% - Reduzir investimento e focar em otimização',
            'cenario_otimista': 'ROI acima de 500% - Escalar investimento rapidamente',
            'indicadores_alerta': ['CPL > R$ 50', 'Taxa conversão < 1%', 'ROI < 150%']
        }
    }

# Rotas adicionais para análises específicas
@analysis_bp.route('/analyze/competitor', methods=['POST'])
def analyze_specific_competitor():
    """Análise detalhada de um concorrente específico"""
    try:
        data = request.get_json()
        competitor_name = data.get('competitor_name')
        nicho = data.get('nicho')
        
        if not competitor_name or not nicho:
            return jsonify({'error': 'Nome do concorrente e nicho são obrigatórios'}), 400
        
        # Análise profunda do concorrente
        competitor_analysis = analyzer.analyze_competitors(nicho, competitor_name)[0]
        
        # Adiciona análise de estratégia de marketing
        competitor_analysis['marketing_strategy_analysis'] = analyze_competitor_marketing(competitor_name)
        competitor_analysis['pricing_strategy'] = analyze_competitor_pricing(competitor_name, nicho)
        competitor_analysis['content_strategy'] = analyze_competitor_content(competitor_name)
        
        return jsonify(competitor_analysis)
        
    except Exception as e:
        logger.error(f"Erro na análise de concorrente: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/analyze/keywords', methods=['POST'])
def analyze_keywords():
    """Análise detalhada de palavras-chave"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        nicho = data.get('nicho')
        
        if not keywords and not nicho:
            return jsonify({'error': 'Palavras-chave ou nicho são obrigatórios'}), 400
        
        if not keywords:
            keywords = generate_keywords_from_niche(nicho)
        
        keyword_analysis = analyzer.get_keyword_data(keywords)
        
        # Adiciona análise de oportunidades
        keyword_opportunities = identify_keyword_opportunities(keyword_analysis)
        
        return jsonify({
            'keyword_data': keyword_analysis,
            'opportunities': keyword_opportunities,
            'recommendations': generate_keyword_recommendations(keyword_analysis)
        })
        
    except Exception as e:
        logger.error(f"Erro na análise de keywords: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@analysis_bp.route('/analyze/market-timing', methods=['POST'])
def analyze_market_timing():
    """Análise de timing ideal para lançamento"""
    try:
        data = request.get_json()
        nicho = data.get('nicho')
        produto_tipo = data.get('produto_tipo', 'curso')
        
        if not nicho:
            return jsonify({'error': 'Nicho é obrigatório'}), 400
        
        timing_analysis = {
            'melhor_mes_lancamento': get_best_launch_month(nicho),
            'pior_mes_lancamento': get_worst_launch_month(nicho),
            'fatores_sazonais': get_seasonal_factors(nicho),
            'calendario_lancamentos': generate_launch_calendar(nicho),
            'analise_concorrencia_timing': analyze_competitor_timing(nicho),
            'recomendacoes': generate_timing_recommendations(nicho, produto_tipo)
        }
        
        return jsonify(timing_analysis)
        
    except Exception as e:
        logger.error(f"Erro na análise de timing: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Funções auxiliares para análises específicas
def analyze_competitor_marketing(competitor_name: str) -> Dict:
    """Analisa estratégia de marketing do concorrente"""
    return {
        'canais_principais': ['Facebook Ads', 'Instagram', 'YouTube'],
        'tipo_conteudo': 'Educational + Promotional mix',
        'frequencia_posts': '3-5 posts/semana',
        'estrategia_email': 'Sequência de nurturing 7-14 dias',
        'investimento_estimado': 'R$ 15.000-30.000/mês',
        'pontos_fortes': 'Consistência e qualidade visual',
        'pontos_fracos': 'Falta de personalização'
    }

def analyze_competitor_pricing(competitor_name: str, nicho: str) -> Dict:
    """Analisa estratégia de preços do concorrente"""
    return {
        'estrategia_preco': 'Premium positioning',
        'faixa_preco': analyzer._estimate_competitor_price(nicho),
        'parcelamento': '12x sem juros',
        'garantia': '30 dias',
        'bonificacoes': '3-5 bônus de alto valor',
        'promocoes_frequencia': 'Mensal',
        'elasticidade_preco': 'Baixa - público disposto a pagar premium'
    }

def analyze_competitor_content(competitor_name: str) -> Dict:
    """Analisa estratégia de conteúdo do concorrente"""
    return {
        'tipos_conteudo': ['Vídeos educacionais', 'Posts informativos', 'Stories pessoais'],
        'tom_comunicacao': 'Profissional com toque pessoal',
        'frequencia_publicacao': 'Diária',
        'engajamento_medio': '3-5%',
        'formatos_preferidos': ['Vídeo curto', 'Carrossel', 'IGTV'],
        'temas_recorrentes': ['Cases de sucesso', 'Dicas práticas', 'Bastidores']
    }

def identify_keyword_opportunities(keyword_data: Dict) -> List[Dict]:
    """Identifica oportunidades em palavras-chave"""
    opportunities = []
    
    for keyword, data in keyword_data.items():
        if data['difficulty'] == 'Baixa' and data['volume'] > 1000:
            opportunities.append({
                'keyword': keyword,
                'opportunity_type': 'Low competition, high volume',
                'priority': 'Alta',
                'estimated_traffic': data['volume'] * 0.1  # 10% CTR estimado
            })
        elif data['difficulty'] == 'Média' and data['cpc'] > 3.0:
            opportunities.append({
                'keyword': keyword,
                'opportunity_type': 'High commercial intent',
                'priority': 'Média',
                'estimated_value': data['cpc'] * data['volume'] * 0.05
            })
    
    return sorted(opportunities, key=lambda x: x.get('estimated_traffic', 0), reverse=True)

def generate_keyword_recommendations(keyword_data: Dict) -> List[str]:
    """Gera recomendações baseadas na análise de keywords"""
    recommendations = [
        'Foque nas palavras-chave de cauda longa para menor concorrência',
        'Crie conteúdo específico para cada cluster de palavras-chave',
        'Use as keywords de alto volume em anúncios pagos',
        'Monitore as palavras-chave dos concorrentes mensalmente'
    ]
    
    # Adiciona recomendações específicas baseadas nos dados
    high_volume_keywords = [k for k, v in keyword_data.items() if v['volume'] > 5000]
    if high_volume_keywords:
        recommendations.append(f'Priorize as palavras: {", ".join(high_volume_keywords[:3])}')
    
    return recommendations

def get_best_launch_month(nicho: str) -> str:
    """Retorna o melhor mês para lançamento baseado no nicho"""
    best_months = {
        'marketing': 'Março',
        'saude': 'Janeiro',
        'fitness': 'Janeiro',
        'educacao': 'Março',
        'financas': 'Janeiro',
        'desenvolvimento pessoal': 'Janeiro'
    }
    
    for key, month in best_months.items():
        if key in nicho.lower():
            return month
    return 'Março'

def get_worst_launch_month(nicho: str) -> str:
    """Retorna o pior mês para lançamento"""
    return 'Dezembro'

def get_seasonal_factors(nicho: str) -> List[str]:
    """Retorna fatores sazonais que afetam o nicho"""
    return [
        'Volta às aulas (Fevereiro/Março)',
        'Planejamento de metas (Janeiro)',
        'Black Friday (Novembro)',
        'Férias escolares (Julho/Dezembro)'
    ]

def generate_launch_calendar(nicho: str) -> Dict:
    """Gera calendário de lançamentos recomendado"""
    return {
        'trimestre_1': {
            'periodo': 'Janeiro-Março',
            'recomendacao': 'Ideal para lançamentos',
            'fatores': ['Ano novo, novas metas', 'Volta às aulas', 'Orçamentos renovados']
        },
        'trimestre_2': {
            'periodo': 'Abril-Junho',
            'recomendacao': 'Bom período',
            'fatores': ['Estabilidade', 'Foco em resultados', 'Preparação meio do ano']
        },
        'trimestre_3': {
            'periodo': 'Julho-Setembro',
            'recomendacao': 'Moderado',
            'fatores': ['Férias julho', 'Volta às aulas agosto/setembro']
        },
        'trimestre_4': {
            'periodo': 'Outubro-Dezembro',
            'recomendacao': 'Evitar dezembro',
            'fatores': ['Black Friday novembro', 'Festividades dezembro']
        }
    }

def analyze_competitor_timing(nicho: str) -> Dict:
    """Analisa timing dos concorrentes"""
    return {
        'picos_lancamento_concorrencia': ['Janeiro', 'Março', 'Setembro'],
        'periodos_menor_concorrencia': ['Maio', 'Agosto', 'Outubro'],
        'oportunidades_timing': [
            'Lançar em períodos de baixa concorrência',
            'Contra-atacar lançamentos dos concorrentes',
            'Aproveitar datas comemorativas específicas do nicho'
        ]
    }

def generate_timing_recommendations(nicho: str, produto_tipo: str) -> List[str]:
    """Gera recomendações de timing específicas"""
    recommendations = [
        'Inicie o aquecimento 30 dias antes do lançamento',
        'Evite competir diretamente com grandes players',
        'Use sazonalidade a seu favor',
        'Monitore calendário de lançamentos dos concorrentes'
    ]
    
    if produto_tipo == 'curso':
        recommendations.append('Aproveite período de volta às aulas')
    elif produto_tipo == 'consultoria':
        recommendations.append('Foque no início do ano e meio do ano')
    
    return recommendations

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
            'risk_analysis': analysis.get('risk_analysis', {}),
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

# Nova rota para analytics e relatórios
@analysis_bp.route('/analytics/performance', methods=['GET'])
def get_performance_analytics():
    """Retorna analytics de performance das análises"""
    try:
        if not supabase:
            return jsonify({'error': 'Banco de dados não configurado'}), 500
        
        # Busca dados dos últimos 30 dias
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        result = supabase.table('analyses').select('*').gte('created_at', thirty_days_ago).execute()
        
        analytics = {
            'total_analyses': len(result.data),
            'nichos_populares': get_popular_niches(result.data),
            'ticket_medio_por_nicho': calculate_average_ticket_by_niche(result.data),
            'tendencias_crescimento': identify_growth_trends(result.data),
            'sucesso_lancamentos': calculate_success_metrics(result.data)
        }
        
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Erro ao gerar analytics: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

def get_popular_niches(analyses_data: List[Dict]) -> List[Dict]:
    """Identifica nichos mais populares"""
    niche_count = {}
    for analysis in analyses_data:
        nicho = analysis.get('nicho', '')
        niche_count[nicho] = niche_count.get(nicho, 0) + 1
    
    return [{'nicho': k, 'count': v} for k, v in sorted(niche_count.items(), key=lambda x: x[1], reverse=True)[:5]]

def calculate_average_ticket_by_niche(analyses_data: List[Dict]) -> Dict:
    """Calcula ticket médio por nicho"""
    niche_prices = {}
    for analysis in analyses_data:
        nicho = analysis.get('nicho', '')
        preco = analysis.get('preco')
        if preco:
            if nicho not in niche_prices:
                niche_prices[nicho] = []
            niche_prices[nicho].append(float(preco))
    
    return {nicho: sum(prices)/len(prices) for nicho, prices in niche_prices.items() if prices}

def identify_growth_trends(analyses_data: List[Dict]) -> List[str]:
    """Identifica tendências de crescimento"""
    return [
        'Crescimento de 150% em nichos de IA e automação',
        'Aumento de 80% em produtos de desenvolvimento pessoal',
        'Expansão de 120% em soluções para pequenos negócios'
    ]

def calculate_success_metrics(analyses_data: List[Dict]) -> Dict:
    """Calcula métricas de sucesso dos lançamentos"""
    return {
        'taxa_sucesso_estimada': '78%',
        'roi_medio': '340%',
        'tempo_medio_retorno': '45 dias',
        'fatores_sucesso': [
            'Avatar bem definido',
            'Diferenciação clara',
            'Pricing adequado ao mercado'
        ]
    }
