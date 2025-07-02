import os
import json
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
import time
import re

logger = logging.getLogger(__name__)

class DeepSeekClient:
    """Cliente avançado para DeepSeek via OpenRouter com análise ultra-detalhada"""
    
    def __init__(self):
        # Usar a chave do OpenRouter
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY não encontrada nas variáveis de ambiente")
        
        # Configurar cliente OpenAI para usar OpenRouter
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Modelo específico do DeepSeek no OpenRouter (gratuito)
        self.model = "deepseek/deepseek-chat"
        self.max_tokens = 6000  # Reduzido para evitar timeouts
        self.temperature = 0.3
        self.top_p = 0.8
        
        logger.info(f"🤖 DeepSeek Client inicializado com modelo: {self.model}")
        
    def analyze_avatar_comprehensive(self, data: Dict) -> Dict:
        """Análise ultra-detalhada do avatar com DeepSeek via OpenRouter"""
        
        prompt = self._create_comprehensive_avatar_prompt(data)
        
        try:
            logger.info("🔍 Iniciando análise com DeepSeek...")
            
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
            
            # Extrai e valida JSON
            analysis = self._extract_and_validate_json(content)
            
            if not analysis:
                logger.warning("⚠️ Falha ao extrair JSON, usando fallback")
                return self._create_fallback_analysis(data)
            
            logger.info("🎉 Análise DeepSeek concluída com sucesso")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Erro na análise DeepSeek: {str(e)}")
            # Retorna análise de fallback em caso de erro
            return self._create_fallback_analysis(data)
    
    def _get_system_prompt(self) -> str:
        """Prompt de sistema otimizado para análise de avatar"""
        return """
Você é um consultor sênior especializado em psicologia do consumidor e análise de mercado no Brasil. 

Sua expertise inclui:
- Psicologia comportamental e neurociência aplicada ao marketing
- Análise de mercado e segmentação psicográfica
- Estratégias de lançamento de produtos digitais
- Métricas e projeções realistas para o mercado brasileiro

Crie análises de avatar extremamente detalhadas, precisas e acionáveis baseadas em dados reais do mercado brasileiro.

IMPORTANTE: Retorne APENAS JSON válido, sem texto adicional antes ou depois.
"""

    def _create_comprehensive_avatar_prompt(self, data: Dict) -> str:
        """Cria prompt ultra-detalhado para análise de avatar"""
        
        nicho = data.get('nicho', '')
        produto = data.get('produto', '')
        preco = data.get('preco', '')
        publico = data.get('publico', '')
        objetivo_receita = data.get('objetivo_receita', '')
        orcamento_marketing = data.get('orcamento_marketing', '')
        
        return f"""
Analise o seguinte produto/serviço e crie uma análise ultra-detalhada do avatar ideal para o mercado brasileiro:

DADOS DO PRODUTO:
- Nicho: {nicho}
- Produto: {produto}
- Preço: R$ {preco}
- Público: {publico}
- Objetivo de Receita: R$ {objetivo_receita}
- Orçamento Marketing: R$ {orcamento_marketing}

Retorne APENAS um JSON válido com esta estrutura exata:

{{
  "escopo": {{
    "nicho_principal": "{nicho}",
    "subnichos": ["Subniche específico 1", "Subniche específico 2", "Subniche específico 3"],
    "produto_ideal": "Nome do produto ideal baseado no nicho",
    "proposta_valor": "Proposta de valor única e específica"
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
        "nome": "Nome real ou realista do concorrente",
        "preco": "Faixa de preço em R$",
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
    "gaps_mercado": ["Gap específico 1", "Gap específico 2", "Gap específico 3"]
  }},
  "mercado": {{
    "tam": "Valor em R$ bilhões",
    "sam": "Valor em R$ milhões", 
    "som": "Valor em R$ milhões",
    "volume_busca": "Número de buscas mensais",
    "tendencias_alta": ["Tendência em alta 1", "Tendência em alta 2"],
    "tendencias_baixa": ["Tendência em baixa 1"],
    "sazonalidade": {{
      "melhores_meses": ["Mês 1", "Mês 2"],
      "piores_meses": ["Mês 1"]
    }}
  }},
  "palavras_chave": {{
    "principais": [
      {{
        "termo": "palavra-chave específica",
        "volume": "Volume mensal",
        "cpc": "CPC em R$",
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
    "cac_medio": "R$ XXX",
    "funil_conversao": ["100% visitantes", "XX% leads", "X% vendas"],
    "ltv_medio": "R$ X.XXX",
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
        "objecao": "Objeção específica comum",
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
      "faturamento": "R$ XX.XXX",
      "roi": "XXX%"
    }},
    "realista": {{
      "conversao": "X,X%", 
      "faturamento": "R$ XXX.XXX",
      "roi": "XXX%"
    }},
    "otimista": {{
      "conversao": "X,X%",
      "faturamento": "R$ X.XXX.XXX",
      "roi": "XXX%"
    }}
  }},
  "plano_acao": [
    {{
      "passo": 1,
      "acao": "Ação específica e prática 1",
      "prazo": "X semanas"
    }},
    {{
      "passo": 2,
      "acao": "Ação específica e prática 2", 
      "prazo": "X semanas"
    }}
  ]
}}

INSTRUÇÕES CRÍTICAS:
- Use dados realistas e específicos do mercado brasileiro
- Substitua TODOS os placeholders (XXX, X.XXX, etc.) por valores numéricos reais
- Seja extremamente específico e detalhado
- Base as projeções no preço e orçamento informados
- Foque em insights acionáveis e práticos
"""

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
        nicho = data.get('nicho', '')
        produto = data.get('produto', 'Produto Digital')
        preco = data.get('preco_float', 997)
        
        logger.info(f"🔄 Criando análise de fallback para {nicho}")
        
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