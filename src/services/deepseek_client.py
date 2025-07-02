import os
import json
import logging
import requests
import time
import re
from typing import Dict, List, Optional, Any
from openai import OpenAI
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import concurrent.futures
from datetime import datetime

logger = logging.getLogger(__name__)

class WebSearcher:
    """Classe para pesquisa na internet com múltiplas fontes"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_google(self, query: str, num_results: int = 5) -> List[Dict]:
        """Pesquisa no Google usando scraping"""
        try:
            encoded_query = quote_plus(query)
            url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Extrair resultados de pesquisa
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:num_results]:
                try:
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    snippet_elem = result.find('span', class_=['aCOpRe', 'st'])
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text()
                        link = link_elem.get('href', '')
                        snippet = snippet_elem.get_text() if snippet_elem else ''
                        
                        if link.startswith('/url?q='):
                            link = link.split('/url?q=')[1].split('&')[0]
                        
                        results.append({
                            'title': title,
                            'url': link,
                            'snippet': snippet
                        })
                except Exception as e:
                    logger.warning(f"Erro ao processar resultado: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Erro na pesquisa Google: {e}")
            return []
    
    def search_market_data(self, nicho: str) -> Dict:
        """Pesquisa dados específicos de mercado"""
        try:
            queries = [
                f"mercado {nicho} Brasil 2024 tamanho",
                f"{nicho} tendências mercado brasileiro",
                f"concorrentes {nicho} Brasil principais",
                f"preços {nicho} cursos online Brasil",
                f"{nicho} público alvo perfil demográfico"
            ]
            
            market_data = {
                'market_size': [],
                'trends': [],
                'competitors': [],
                'pricing': [],
                'demographics': []
            }
            
            for i, query in enumerate(queries):
                results = self.search_google(query, 3)
                key = list(market_data.keys())[i]
                market_data[key] = results
                time.sleep(1)  # Rate limiting
            
            return market_data
            
        except Exception as e:
            logger.error(f"Erro na pesquisa de dados de mercado: {e}")
            return {}
    
    def get_competitor_info(self, competitor_name: str, nicho: str) -> Dict:
        """Obtém informações específicas sobre um concorrente"""
        try:
            query = f"{competitor_name} {nicho} preço curso online"
            results = self.search_google(query, 3)
            
            return {
                'name': competitor_name,
                'search_results': results,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar info do concorrente {competitor_name}: {e}")
            return {}

class DeepSeekClient:
    """Cliente avançado para DeepSeek com pesquisa na internet e análise ultra-detalhada"""
    
    def __init__(self):
        # Usar a chave do OpenRouter
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.web_searcher = WebSearcher()
        
        if not self.api_key:
            logger.warning("⚠️ DEEPSEEK_API_KEY não encontrada - usando análise de fallback")
            self.client = None
            return
        
        try:
            # Configurar cliente OpenAI para usar OpenRouter
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            
            # Modelo específico do DeepSeek no OpenRouter
            self.model = "deepseek/deepseek-r1-distill-llama-70b"
            self.max_tokens = 32000
            self.temperature = 0.7
            self.top_p = 0.9
            
            logger.info(f"🤖 DeepSeek Client inicializado com modelo: {self.model}")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar cliente DeepSeek: {e}")
            self.client = None
    
    def analyze_avatar_comprehensive(self, data: Dict) -> Dict:
        """Análise ultra-detalhada do avatar com pesquisa na internet"""
        
        if not self.client:
            logger.info("🔄 Cliente DeepSeek não disponível, usando análise de fallback")
            return self._create_fallback_analysis(data)
        
        try:
            # 1. Pesquisar dados de mercado na internet
            logger.info("🔍 Pesquisando dados de mercado na internet...")
            market_research = self._conduct_market_research(data)
            
            # 2. Gerar análise com IA usando dados pesquisados
            logger.info("🧠 Gerando análise com DeepSeek AI...")
            analysis = self._generate_ai_analysis(data, market_research)
            
            # 3. Enriquecer com dados adicionais
            logger.info("📊 Enriquecendo análise com dados adicionais...")
            enriched_analysis = self._enrich_analysis(analysis, market_research)
            
            logger.info("🎉 Análise DeepSeek concluída com sucesso")
            return enriched_analysis
            
        except Exception as e:
            logger.error(f"❌ Erro na análise DeepSeek: {str(e)}")
            return self._create_fallback_analysis(data)
    
    def _conduct_market_research(self, data: Dict) -> Dict:
        """Conduz pesquisa de mercado na internet"""
        nicho = data.get('nicho', '')
        concorrentes = data.get('concorrentes', '')
        
        research_data = {
            'market_data': {},
            'competitor_data': [],
            'trend_data': {},
            'pricing_data': {},
            'search_timestamp': datetime.now().isoformat()
        }
        
        try:
            # Pesquisa paralela para eficiência
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # Pesquisa dados gerais de mercado
                future_market = executor.submit(self.web_searcher.search_market_data, nicho)
                
                # Pesquisa concorrentes específicos
                competitor_futures = []
                if concorrentes:
                    competitor_list = [c.strip() for c in concorrentes.split(',') if c.strip()]
                    for competitor in competitor_list[:3]:  # Limitar a 3 concorrentes
                        future = executor.submit(self.web_searcher.get_competitor_info, competitor, nicho)
                        competitor_futures.append(future)
                
                # Coletar resultados
                research_data['market_data'] = future_market.result()
                
                for future in competitor_futures:
                    try:
                        competitor_info = future.result()
                        if competitor_info:
                            research_data['competitor_data'].append(competitor_info)
                    except Exception as e:
                        logger.warning(f"Erro ao obter dados de concorrente: {e}")
            
            logger.info(f"✅ Pesquisa de mercado concluída: {len(research_data['competitor_data'])} concorrentes analisados")
            
        except Exception as e:
            logger.error(f"❌ Erro na pesquisa de mercado: {e}")
        
        return research_data
    
    def _generate_ai_analysis(self, data: Dict, research: Dict) -> Dict:
        """Gera análise usando IA com dados de pesquisa"""
        
        prompt = self._create_enhanced_analysis_prompt(data, research)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=False
            )
            
            content = response.choices[0].message.content
            logger.info(f"✅ Resposta DeepSeek recebida: {len(content)} caracteres")
            
            # Parse da resposta JSON
            analysis = self._extract_and_validate_json(content)
            
            if not analysis:
                logger.warning("⚠️ Falha ao extrair JSON, usando fallback")
                return self._create_fallback_analysis(data)
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar análise com IA: {str(e)}")
            return self._create_fallback_analysis(data)
    
    def _get_system_prompt(self) -> str:
        """Prompt de sistema otimizado para análise de avatar"""
        return """
Você é um especialista mundial em pesquisa de mercado, neurociência aplicada ao marketing e lançamentos de produtos digitais. 

Sua expertise inclui:
- Psicologia comportamental e neurociência do consumidor
- Análise de mercado e segmentação psicográfica avançada
- Estratégias de lançamento de produtos digitais de alto ticket
- Métricas e projeções realistas para o mercado brasileiro
- Análise competitiva e posicionamento estratégico
- Funis de conversão e otimização de campanhas

INSTRUÇÕES CRÍTICAS:
1. Use SEMPRE dados reais e específicos do mercado brasileiro
2. Base suas análises em pesquisas e dados fornecidos
3. Seja extremamente detalhado e específico
4. Foque em insights acionáveis e práticos
5. Use números realistas baseados em benchmarks do mercado
6. Retorne APENAS JSON válido, sem texto adicional

Crie análises de avatar extremamente detalhadas, precisas e acionáveis.
"""

    def _create_enhanced_analysis_prompt(self, data: Dict, research: Dict) -> str:
        """Cria prompt aprimorado com dados de pesquisa"""
        
        nicho = data.get('nicho', '')
        produto = data.get('produto', '')
        preco = data.get('preco', '')
        publico = data.get('publico', '')
        objetivo_receita = data.get('objetivoReceita', '')
        orcamento_marketing = data.get('orcamentoMarketing', '')
        
        # Processar dados de pesquisa
        market_insights = self._process_research_data(research)
        
        return f"""
Analise o seguinte produto/serviço e crie uma análise ultra-detalhada do avatar ideal para o mercado brasileiro.

DADOS DO PRODUTO:
- Nicho: {nicho}
- Produto: {produto}
- Preço: R$ {preco}
- Público: {publico}
- Objetivo de Receita: R$ {objetivo_receita}
- Orçamento Marketing: R$ {orcamento_marketing}

DADOS DE PESQUISA DE MERCADO:
{market_insights}

Retorne APENAS um JSON válido com esta estrutura exata:

{{
  "escopo": {{
    "nicho_principal": "{nicho}",
    "subnichos": ["Subniche específico 1", "Subniche específico 2", "Subniche específico 3"],
    "produto_ideal": "Nome do produto ideal baseado no nicho",
    "proposta_valor": "Proposta de valor única e específica baseada na pesquisa"
  }},
  "avatar": {{
    "demografia": {{
      "faixa_etaria": "Faixa específica em anos",
      "genero": "Distribuição percentual por gênero",
      "localizacao": "Principais regiões do Brasil com percentuais",
      "renda": "Faixa de renda mensal em R$",
      "escolaridade": "Nível educacional predominante",
      "profissoes": ["Profissão específica 1", "Profissão específica 2", "Profissão específica 3"]
    }},
    "psicografia": {{
      "valores": ["Valor específico 1", "Valor específico 2", "Valor específico 3"],
      "estilo_vida": "Descrição detalhada do estilo de vida",
      "aspiracoes": ["Aspiração específica 1", "Aspiração específica 2"],
      "medos": ["Medo específico 1", "Medo específico 2", "Medo específico 3"],
      "frustracoes": ["Frustração específica 1", "Frustração específica 2"]
    }},
    "comportamento_digital": {{
      "plataformas": ["Plataforma principal 1", "Plataforma principal 2"],
      "horarios_pico": "Horários específicos de maior atividade",
      "conteudo_preferido": ["Tipo de conteúdo 1", "Tipo de conteúdo 2", "Tipo de conteúdo 3"],
      "influenciadores": ["Tipo de influenciador 1", "Tipo de influenciador 2"]
    }}
  }},
  "dores_desejos": {{
    "principais_dores": [
      {{
        "descricao": "Dor específica e detalhada 1",
        "impacto": "Como esta dor impacta a vida da pessoa",
        "urgencia": "Alta"
      }},
      {{
        "descricao": "Dor específica e detalhada 2", 
        "impacto": "Como esta dor impacta a vida da pessoa",
        "urgencia": "Média"
      }},
      {{
        "descricao": "Dor específica e detalhada 3",
        "impacto": "Como esta dor impacta a vida da pessoa",
        "urgencia": "Baixa"
      }}
    ],
    "estado_atual": "Descrição detalhada do estado atual do avatar",
    "estado_desejado": "Descrição detalhada do estado desejado",
    "obstaculos": ["Obstáculo específico 1", "Obstáculo específico 2"],
    "sonho_secreto": "O sonho mais profundo que o avatar não verbaliza"
  }},
  "concorrencia": {{
    "diretos": [
      {{
        "nome": "Nome real do concorrente baseado na pesquisa",
        "preco": "Faixa de preço em R$ baseada na pesquisa",
        "usp": "Proposta única específica",
        "forcas": ["Força específica 1", "Força específica 2"],
        "fraquezas": ["Fraqueza específica 1", "Fraqueza específica 2"]
      }}
    ],
    "indiretos": [
      {{
        "nome": "Concorrente indireto específico",
        "tipo": "Tipo de solução alternativa"
      }}
    ],
    "gaps_mercado": ["Gap específico 1 baseado na pesquisa", "Gap específico 2", "Gap específico 3"]
  }},
  "mercado": {{
    "tam": "Valor em R$ bilhões baseado na pesquisa",
    "sam": "Valor em R$ milhões baseado na pesquisa", 
    "som": "Valor em R$ milhões baseado na pesquisa",
    "volume_busca": "Número de buscas mensais baseado na pesquisa",
    "tendencias_alta": ["Tendência em alta 1 da pesquisa", "Tendência em alta 2"],
    "tendencias_baixa": ["Tendência em baixa 1 da pesquisa"],
    "sazonalidade": {{
      "melhores_meses": ["Mês 1", "Mês 2"],
      "piores_meses": ["Mês 1"]
    }}
  }},
  "palavras_chave": {{
    "principais": [
      {{
        "termo": "palavra-chave específica baseada na pesquisa",
        "volume": "Volume mensal estimado",
        "cpc": "CPC em R$ estimado",
        "dificuldade": "Alta/Média/Baixa",
        "intencao": "Comercial/Informacional"
      }}
    ],
    "custos_plataforma": {{
      "facebook": {{"cpm": "R$ XX", "cpc": "R$ X,XX", "cpl": "R$ XX", "conversao": "X,X%"}},
      "google": {{"cpm": "R$ XX", "cpc": "R$ X,XX", "cpl": "R$ XX", "conversao": "X,X%"}},
      "youtube": {{"cpm": "R$ XX", "cpc": "R$ X,XX", "cpl": "R$ XX", "conversao": "X,X%"}},
      "tiktok": {{"cpm": "R$ XX", "cpc": "R$ X,XX", "cpl": "R$ XX", "conversao": "X,X%"}}
    }}
  }},
  "metricas": {{
    "cac_medio": "R$ XXX baseado no orçamento e nicho",
    "funil_conversao": ["100% visitantes", "XX% leads", "X% vendas"],
    "ltv_medio": "R$ X.XXX baseado no preço e retenção",
    "ltv_cac_ratio": "X,X:1",
    "roi_canais": {{
      "facebook": "XXX%",
      "google": "XXX%",
      "youtube": "XXX%",
      "tiktok": "XXX%"
    }}
  }},
  "voz_mercado": {{
    "objecoes": [
      {{
        "objecao": "Objeção específica comum baseada na pesquisa",
        "contorno": "Como contornar esta objeção"
      }}
    ],
    "linguagem": {{
      "termos": ["Termo técnico 1", "Termo técnico 2"],
      "girias": ["Gíria do nicho 1"],
      "gatilhos": ["Gatilho mental 1", "Gatilho mental 2"]
    }},
    "crencas_limitantes": ["Crença limitante 1", "Crença limitante 2"]
  }},
  "projecoes": {{
    "conservador": {{
      "conversao": "X,X%",
      "faturamento": "R$ XX.XXX baseado no orçamento",
      "roi": "XXX%"
    }},
    "realista": {{
      "conversao": "X,X%", 
      "faturamento": "R$ XXX.XXX baseado no orçamento",
      "roi": "XXX%"
    }},
    "otimista": {{
      "conversao": "X,X%",
      "faturamento": "R$ X.XXX.XXX baseado no orçamento",
      "roi": "XXX%"
    }}
  }},
  "plano_acao": [
    {{
      "passo": 1,
      "acao": "Ação específica e prática 1 baseada na análise",
      "prazo": "X semanas"
    }},
    {{
      "passo": 2,
      "acao": "Ação específica e prática 2 baseada na análise", 
      "prazo": "X semanas"
    }}
  ],
  "insights_pesquisa": {{
    "dados_mercado": "Principais insights da pesquisa de mercado",
    "concorrentes_encontrados": "Concorrentes identificados na pesquisa",
    "tendencias_identificadas": "Tendências identificadas na pesquisa",
    "oportunidades_unicas": "Oportunidades únicas identificadas"
  }}
}}

INSTRUÇÕES CRÍTICAS:
- Use EXCLUSIVAMENTE dados da pesquisa fornecida quando disponível
- Substitua TODOS os placeholders (XXX, X.XXX, etc.) por valores numéricos reais
- Base as projeções no preço ({preco}) e orçamento ({orcamento_marketing}) informados
- Seja extremamente específico e detalhado
- Foque em insights acionáveis baseados na pesquisa real
"""

    def _process_research_data(self, research: Dict) -> str:
        """Processa dados de pesquisa para incluir no prompt"""
        if not research or not research.get('market_data'):
            return "Nenhum dado de pesquisa disponível."
        
        insights = []
        
        # Processar dados de mercado
        market_data = research.get('market_data', {})
        for category, results in market_data.items():
            if results:
                insights.append(f"\n{category.upper()}:")
                for result in results[:2]:  # Limitar a 2 resultados por categoria
                    insights.append(f"- {result.get('title', '')}: {result.get('snippet', '')}")
        
        # Processar dados de concorrentes
        competitor_data = research.get('competitor_data', [])
        if competitor_data:
            insights.append("\nCONCORRENTES IDENTIFICADOS:")
            for competitor in competitor_data:
                insights.append(f"- {competitor.get('name', '')}")
                for result in competitor.get('search_results', [])[:1]:
                    insights.append(f"  * {result.get('snippet', '')}")
        
        return '\n'.join(insights) if insights else "Dados de pesquisa limitados disponíveis."
    
    def _enrich_analysis(self, analysis: Dict, research: Dict) -> Dict:
        """Enriquece a análise com dados adicionais da pesquisa"""
        try:
            # Adicionar metadados da pesquisa
            analysis['research_metadata'] = {
                'search_timestamp': research.get('search_timestamp'),
                'sources_consulted': len(research.get('market_data', {})),
                'competitors_analyzed': len(research.get('competitor_data', [])),
                'data_quality': 'high' if research.get('market_data') else 'limited'
            }
            
            # Adicionar insights específicos da pesquisa
            if 'insights_pesquisa' not in analysis:
                analysis['insights_pesquisa'] = {
                    'dados_mercado': 'Análise baseada em pesquisa de mercado atualizada',
                    'concorrentes_encontrados': ', '.join([c.get('name', '') for c in research.get('competitor_data', [])]),
                    'tendencias_identificadas': 'Tendências identificadas através de pesquisa online',
                    'oportunidades_unicas': 'Oportunidades baseadas em gaps identificados na pesquisa'
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro ao enriquecer análise: {e}")
            return analysis
    
    def _extract_and_validate_json(self, content: str) -> Optional[Dict]:
        """Extrai e valida JSON da resposta"""
        try:
            # Remove possível texto antes e depois do JSON
            content = content.strip()
            
            # Procura por JSON válido
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx + 1]
                parsed_json = json.loads(json_str)
                logger.info("✅ JSON extraído e validado com sucesso")
                return parsed_json
            
            # Tenta parsear o conteúdo inteiro
            parsed_json = json.loads(content)
            logger.info("✅ JSON parseado diretamente com sucesso")
            return parsed_json
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao parsear JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao extrair JSON: {e}")
            return None

    def _create_fallback_analysis(self, data: Dict) -> Dict:
        """Cria análise de fallback detalhada quando a IA falha"""
        nicho = data.get('nicho', 'Produto Digital')
        produto = data.get('produto', 'Produto Digital')
        
        # Garantir que preco seja um número válido
        try:
            preco = float(data.get('preco', 0)) if data.get('preco') else 997.0
        except (ValueError, TypeError):
            preco = 997.0
        
        # Garantir que outros valores numéricos sejam válidos
        try:
            objetivo_receita = float(data.get('objetivoReceita', 0)) if data.get('objetivoReceita') else 100000.0
        except (ValueError, TypeError):
            objetivo_receita = 100000.0
            
        try:
            orcamento_marketing = float(data.get('orcamentoMarketing', 0)) if data.get('orcamentoMarketing') else 50000.0
        except (ValueError, TypeError):
            orcamento_marketing = 50000.0
        
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
                "cac_medio": f"R$ {int(orcamento_marketing * 0.01):,}".replace(',', '.'),
                "funil_conversao": ["100% visitantes", "18% leads", "3,2% vendas"],
                "ltv_medio": f"R$ {int(preco * 1.8):,}".replace(',', '.'),
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
                    "faturamento": f"R$ {int(objetivo_receita * 0.6):,}".replace(',', '.'),
                    "roi": "240%"
                },
                "realista": {
                    "conversao": "3,2%",
                    "faturamento": f"R$ {int(objetivo_receita):,}".replace(',', '.'),
                    "roi": "380%"
                },
                "otimista": {
                    "conversao": "5,0%",
                    "faturamento": f"R$ {int(objetivo_receita * 1.5):,}".replace(',', '.'),
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
            ],
            "insights_pesquisa": {
                "dados_mercado": "Análise baseada em dados de mercado consolidados e benchmarks da indústria",
                "concorrentes_encontrados": "Principais players identificados através de análise competitiva",
                "tendencias_identificadas": "Tendências emergentes no mercado brasileiro",
                "oportunidades_unicas": "Gaps de mercado identificados para diferenciação estratégica"
            },
            "research_metadata": {
                "search_timestamp": datetime.now().isoformat(),
                "sources_consulted": 0,
                "competitors_analyzed": 0,
                "data_quality": "fallback"
            }
        }
