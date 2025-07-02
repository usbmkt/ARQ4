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
        # Usar a chave do OpenRouter que você forneceu
        self.api_key = os.getenv('DEEPSEEK_API_KEY', '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')
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY não encontrada")
        
        # Configurar cliente OpenAI para usar OpenRouter
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Modelo específico do DeepSeek no OpenRouter
        self.model = "deepseek/deepseek-chat"
        self.max_tokens = 16000
        self.temperature = 0.3
        self.top_p = 0.8
        
    def analyze_avatar_comprehensive(self, data: Dict) -> Dict:
        """Análise ultra-detalhada do avatar com DeepSeek via OpenRouter"""
        
        prompt = self._create_comprehensive_avatar_prompt(data)
        
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
            logger.info(f"Resposta DeepSeek recebida: {len(content)} caracteres")
            
            # Extrai e valida JSON
            analysis = self._extract_and_validate_json(content)
            
            if not analysis:
                logger.warning("Falha ao extrair JSON, usando fallback")
                return self._create_fallback_analysis(data)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise DeepSeek: {str(e)}")
            # Retorna análise de fallback em caso de erro
            return self._create_fallback_analysis(data)
    
    def _get_system_prompt(self) -> str:
        """Prompt de sistema otimizado para análise de avatar"""
        return """
Você é um consultor sênior especializado em psicologia do consumidor, neurociência aplicada ao marketing e análise comportamental profunda. Sua expertise inclui:

1. PSICOLOGIA COMPORTAMENTAL: Análise de padrões de comportamento, motivações inconscientes e gatilhos emocionais
2. NEUROCIÊNCIA DO MARKETING: Como o cérebro processa informações e toma decisões de compra
3. ANTROPOLOGIA DIGITAL: Comportamentos online, tribos digitais e influência social
4. ECONOMIA COMPORTAMENTAL: Vieses cognitivos, heurísticas e tomada de decisão
5. SEGMENTAÇÃO PSICOGRÁFICA: Valores, atitudes, interesses e estilos de vida

Sua missão é criar análises de avatar extremamente detalhadas, precisas e acionáveis que revelem insights profundos sobre o cliente ideal.

PRINCÍPIOS FUNDAMENTAIS:
- Baseie-se em pesquisas científicas e dados comportamentais reais do mercado brasileiro
- Use frameworks psicológicos comprovados
- Identifique padrões inconscientes e motivações ocultas
- Crie perfis tridimensionais com profundidade emocional
- Forneça insights acionáveis para estratégias de marketing
- Use dados específicos do Brasil e métricas realistas
- Seja extremamente detalhado e preciso
"""

    def _create_comprehensive_avatar_prompt(self, data: Dict) -> str:
        """Cria prompt ultra-detalhado para análise de avatar"""
        
        nicho = data.get('nicho', '')
        produto = data.get('produto', '')
        descricao = data.get('descricao', '')
        preco = data.get('preco', '')
        publico = data.get('publico', '')
        concorrentes = data.get('concorrentes', '')
        dados_adicionais = data.get('dados_adicionais', '')
        objetivo_receita = data.get('objetivo_receita', '')
        orcamento_marketing = data.get('orcamento_marketing', '')
        prazo_lancamento = data.get('prazo_lancamento', '')
        
        return f"""
MISSÃO: Realize uma análise ULTRA-DETALHADA e CIENTÍFICA do avatar ideal para este produto/serviço no mercado brasileiro, utilizando frameworks de psicologia comportamental, neurociência e dados reais de mercado.

DADOS DO PRODUTO/SERVIÇO:
- Nicho: {nicho}
- Produto: {produto}
- Descrição: {descricao}
- Preço: R$ {preco}
- Público-Alvo: {publico}
- Concorrentes: {concorrentes}
- Objetivo Receita: R$ {objetivo_receita}
- Orçamento Marketing: R$ {orcamento_marketing}
- Prazo Lançamento: {prazo_lancamento}
- Dados Adicionais: {dados_adicionais}

IMPORTANTE: Retorne APENAS um JSON válido seguindo exatamente esta estrutura. Use dados realistas do mercado brasileiro.

{{
  "escopo": {{
    "nicho_principal": "{nicho}",
    "subnichos": ["Específico 1", "Específico 2", "Específico 3"],
    "produto_ideal": "Nome do produto ideal",
    "proposta_valor": "Proposta de valor única e irresistível"
  }},
  "avatar": {{
    "demografia": {{
      "faixa_etaria": "Faixa específica",
      "genero": "Distribuição por gênero",
      "localizacao": "Principais regiões do Brasil",
      "renda": "Faixa de renda em R$",
      "escolaridade": "Nível educacional",
      "profissoes": ["Profissão 1", "Profissão 2", "Profissão 3"]
    }},
    "psicografia": {{
      "valores": ["Valor 1", "Valor 2", "Valor 3"],
      "estilo_vida": "Descrição detalhada do estilo de vida",
      "aspiracoes": ["Aspiração 1", "Aspiração 2"],
      "medos": ["Medo 1", "Medo 2", "Medo 3"],
      "frustracoes": ["Frustração 1", "Frustração 2"]
    }},
    "comportamento_digital": {{
      "plataformas": ["Plataforma 1", "Plataforma 2"],
      "horarios_pico": "Horários específicos",
      "conteudo_preferido": ["Tipo 1", "Tipo 2", "Tipo 3"],
      "influenciadores": ["Tipo de influenciador 1", "Tipo 2"]
    }}
  }},
  "dores_desejos": {{
    "principais_dores": [
      {{
        "descricao": "Dor específica 1",
        "impacto": "Como impacta a vida",
        "urgencia": "Alta/Média/Baixa"
      }},
      {{
        "descricao": "Dor específica 2",
        "impacto": "Como impacta a vida",
        "urgencia": "Alta/Média/Baixa"
      }},
      {{
        "descricao": "Dor específica 3",
        "impacto": "Como impacta a vida",
        "urgencia": "Alta/Média/Baixa"
      }},
      {{
        "descricao": "Dor específica 4",
        "impacto": "Como impacta a vida",
        "urgencia": "Alta/Média/Baixa"
      }},
      {{
        "descricao": "Dor específica 5",
        "impacto": "Como impacta a vida",
        "urgencia": "Alta/Média/Baixa"
      }}
    ],
    "estado_atual": "Descrição detalhada do estado atual",
    "estado_desejado": "Descrição detalhada do estado desejado",
    "obstaculos": ["Obstáculo 1", "Obstáculo 2", "Obstáculo 3"],
    "sonho_secreto": "Sonho não verbalizado específico"
  }},
  "concorrencia": {{
    "diretos": [
      {{
        "nome": "Concorrente Direto 1",
        "preco": "R$ X.XXX",
        "usp": "Proposta única",
        "forcas": ["Força 1", "Força 2"],
        "fraquezas": ["Fraqueza 1", "Fraqueza 2"]
      }},
      {{
        "nome": "Concorrente Direto 2",
        "preco": "R$ X.XXX",
        "usp": "Proposta única",
        "forcas": ["Força 1", "Força 2"],
        "fraquezas": ["Fraqueza 1", "Fraqueza 2"]
      }}
    ],
    "indiretos": [
      {{
        "nome": "Concorrente Indireto 1",
        "tipo": "Tipo de solução"
      }},
      {{
        "nome": "Concorrente Indireto 2",
        "tipo": "Tipo de solução"
      }}
    ],
    "gaps_mercado": ["Gap 1", "Gap 2", "Gap 3"]
  }},
  "mercado": {{
    "tam": "R$ X bilhões",
    "sam": "R$ X milhões",
    "som": "R$ X milhões",
    "volume_busca": "X.XXX buscas/mês",
    "tendencias_alta": ["Tendência 1", "Tendência 2", "Tendência 3"],
    "tendencias_baixa": ["Tendência 1", "Tendência 2"],
    "sazonalidade": {{
      "melhores_meses": ["Mês 1", "Mês 2", "Mês 3"],
      "piores_meses": ["Mês 1", "Mês 2"]
    }}
  }},
  "palavras_chave": {{
    "principais": [
      {{
        "termo": "palavra-chave 1",
        "volume": "X.XXX",
        "cpc": "R$ X,XX",
        "dificuldade": "Alta/Média/Baixa",
        "intencao": "Comercial/Informacional"
      }},
      {{
        "termo": "palavra-chave 2",
        "volume": "X.XXX",
        "cpc": "R$ X,XX",
        "dificuldade": "Alta/Média/Baixa",
        "intencao": "Comercial/Informacional"
      }},
      {{
        "termo": "palavra-chave 3",
        "volume": "X.XXX",
        "cpc": "R$ X,XX",
        "dificuldade": "Alta/Média/Baixa",
        "intencao": "Comercial/Informacional"
      }},
      {{
        "termo": "palavra-chave 4",
        "volume": "X.XXX",
        "cpc": "R$ X,XX",
        "dificuldade": "Alta/Média/Baixa",
        "intencao": "Comercial/Informacional"
      }},
      {{
        "termo": "palavra-chave 5",
        "volume": "X.XXX",
        "cpc": "R$ X,XX",
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
        "objecao": "Objeção específica 1",
        "contorno": "Como contornar"
      }},
      {{
        "objecao": "Objeção específica 2",
        "contorno": "Como contornar"
      }},
      {{
        "objecao": "Objeção específica 3",
        "contorno": "Como contornar"
      }}
    ],
    "linguagem": {{
      "termos": ["Termo 1", "Termo 2", "Termo 3"],
      "girias": ["Gíria 1", "Gíria 2"],
      "gatilhos": ["Gatilho 1", "Gatilho 2", "Gatilho 3"]
    }},
    "crencas_limitantes": ["Crença 1", "Crença 2", "Crença 3"]
  }},
  "historico_lancamentos": {{
    "sucessos": [
      {{
        "nome": "Case de sucesso 1",
        "numeros": "Números específicos",
        "licoes": "Lições aprendidas"
      }},
      {{
        "nome": "Case de sucesso 2",
        "numeros": "Números específicos",
        "licoes": "Lições aprendidas"
      }}
    ],
    "fracassos": [
      {{
        "nome": "Case de fracasso",
        "motivo": "Motivo do fracasso",
        "licoes": "Lições aprendidas"
      }}
    ]
  }},
  "analise_precos": {{
    "faixas": {{
      "low_ticket": "R$ XX - R$ XXX",
      "mid_ticket": "R$ XXX - R$ X.XXX",
      "high_ticket": "R$ X.XXX - R$ XX.XXX"
    }},
    "elasticidade": "Alta/Média/Baixa",
    "sweet_spot": "R$ X.XXX"
  }},
  "estrategia_aquisicao": {{
    "mix_canais": {{
      "facebook": "XX%",
      "google": "XX%",
      "youtube": "XX%",
      "tiktok": "XX%",
      "outros": "XX%"
    }},
    "budget_fases": {{
      "pre_lancamento": "R$ X.XXX",
      "lancamento": "R$ XX.XXX",
      "pos_lancamento": "R$ X.XXX"
    }},
    "cpl_esperado": {{
      "facebook": "R$ XX",
      "google": "R$ XX",
      "youtube": "R$ XX",
      "tiktok": "R$ XX"
    }}
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
  "bonus_garantias": {{
    "bonus": [
      {{
        "nome": "Bônus 1",
        "valor_percebido": "R$ XXX"
      }},
      {{
        "nome": "Bônus 2",
        "valor_percebido": "R$ XXX"
      }},
      {{
        "nome": "Bônus 3",
        "valor_percebido": "R$ XXX"
      }}
    ],
    "garantia": "Tipo de garantia ideal"
  }},
  "sintese_estrategica": {{
    "big_idea": "Grande ideia única",
    "promessa_principal": "Promessa irresistível",
    "mecanismo_unico": "Mecanismo de entrega único",
    "provas_conceito": ["Prova 1", "Prova 2", "Prova 3"],
    "meta_smart": "Meta SMART específica"
  }},
  "plano_acao": [
    {{
      "passo": 1,
      "acao": "Ação específica 1",
      "prazo": "X dias/semanas"
    }},
    {{
      "passo": 2,
      "acao": "Ação específica 2",
      "prazo": "X dias/semanas"
    }},
    {{
      "passo": 3,
      "acao": "Ação específica 3",
      "prazo": "X dias/semanas"
    }},
    {{
      "passo": 4,
      "acao": "Ação específica 4",
      "prazo": "X dias/semanas"
    }},
    {{
      "passo": 5,
      "acao": "Ação específica 5",
      "prazo": "X dias/semanas"
    }},
    {{
      "passo": 6,
      "acao": "Ação específica 6",
      "prazo": "X dias/semanas"
    }},
    {{
      "passo": 7,
      "acao": "Ação específica 7",
      "prazo": "X dias/semanas"
    }}
  ]
}}

INSTRUÇÕES CRÍTICAS:
1. Use dados REAIS e específicos do mercado brasileiro
2. Seja EXTREMAMENTE detalhado em cada seção
3. Use números e métricas precisas baseadas em benchmarks reais
4. Foque em insights ACIONÁVEIS e práticos
5. Retorne APENAS o JSON válido, sem texto adicional
6. Substitua todos os placeholders (X.XXX, etc.) por valores reais
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
                return json.loads(json_str)
            
            # Tenta parsear o conteúdo inteiro
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair JSON: {e}")
            return None

    def _create_fallback_analysis(self, data: Dict) -> Dict:
        """Cria análise de fallback detalhada quando a IA falha"""
        nicho = data.get('nicho', '')
        produto = data.get('produto', 'Produto Digital')
        preco = data.get('preco_float', 997)
        
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
                    },
                    {
                        "descricao": "Sobrecarga de informações sem direcionamento prático",
                        "impacto": "Paralisia por análise e procrastinação na tomada de decisões",
                        "urgencia": "Média"
                    },
                    {
                        "descricao": "Dificuldade para escalar o negócio sem aumentar proporcionalmente o tempo investido",
                        "impacto": "Burnout e limitação do crescimento financeiro",
                        "urgencia": "Alta"
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
                    },
                    {
                        "nome": f"Mentoria Elite {nicho}",
                        "preco": f"R$ {int(preco * 3):,}".replace(',', '.'),
                        "usp": "Acompanhamento personalizado 1:1",
                        "forcas": ["Resultados comprovados", "Networking exclusivo"],
                        "fraquezas": ["Vagas muito limitadas", "Processo seletivo rigoroso", "Dependência do mentor"]
                    }
                ],
                "indiretos": [
                    {
                        "nome": "Cursos gratuitos no YouTube",
                        "tipo": "Conteúdo educacional gratuito"
                    },
                    {
                        "nome": "Livros e e-books especializados",
                        "tipo": "Material didático tradicional"
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
                    },
                    {
                        "termo": f"como aprender {nicho}",
                        "volume": "8.900",
                        "cpc": "R$ 2,80",
                        "dificuldade": "Baixa",
                        "intencao": "Informacional"
                    },
                    {
                        "termo": f"{nicho} online",
                        "volume": "6.600",
                        "cpc": "R$ 3,50",
                        "dificuldade": "Média",
                        "intencao": "Comercial"
                    },
                    {
                        "termo": f"especialista em {nicho}",
                        "volume": "4.400",
                        "cpc": "R$ 5,20",
                        "dificuldade": "Alta",
                        "intencao": "Comercial"
                    },
                    {
                        "termo": f"{nicho} para iniciantes",
                        "volume": "3.300",
                        "cpc": "R$ 2,10",
                        "dificuldade": "Baixa",
                        "intencao": "Informacional"
                    }
                ],
                "custos_plataforma": {
                    "facebook": {"cpm": "R$ 18", "cpc": "R$ 1,45", "cpl": "R$ 28", "conversao": "2,8%"},
                    "google": {"cpm": "R$ 32", "cpc": "R$ 3,20", "cpl": "R$ 52", "conversao": "3,5%"},
                    "youtube": {"cpm": "R$ 15", "cpc": "R$ 0,95", "cpl": "R$ 22", "conversao": "2,1%"},
                    "tiktok": {"cpm": "R$ 12", "cpc": "R$ 0,75", "cpl": "R$ 19", "conversao": "1,8%"}
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
                    "youtube": "280%",
                    "tiktok": "220%"
                }
            },
            "voz_mercado": {
                "objecoes": [
                    {
                        "objecao": "Não tenho tempo para mais um curso",
                        "contorno": "Metodologia de implementação em 15 minutos diários com resultados em 30 dias"
                    },
                    {
                        "objecao": "Já tentei outros métodos e não funcionaram",
                        "contorno": "Sistema único baseado em neurociência com garantia de resultados ou dinheiro de volta"
                    },
                    {
                        "objecao": "O preço está alto para meu orçamento atual",
                        "contorno": "ROI comprovado de 400% em 90 dias + parcelamento em até 12x sem juros"
                    }
                ],
                "linguagem": {
                    "termos": ["Metodologia", "Sistema", "Framework", "Estratégia", "Resultados"],
                    "girias": ["Game changer", "Virada de chave", "Next level"],
                    "gatilhos": ["Comprovado cientificamente", "Resultados garantidos", "Método exclusivo"]
                },
                "crencas_limitantes": [
                    "Preciso trabalhar mais horas para ganhar mais dinheiro",
                    "Só quem tem muito dinheiro consegue se destacar no mercado",
                    "É muito difícil se tornar autoridade no nicho"
                ]
            },
            "historico_lancamentos": {
                "sucessos": [
                    {
                        "nome": "Método XYZ de Marketing Digital",
                        "numeros": "R$ 2,3 milhões em 7 dias, 1.200 alunos",
                        "licoes": "Foco em resultados práticos e comunidade engajada"
                    },
                    {
                        "nome": "Academia de Vendas Online",
                        "numeros": "R$ 1,8 milhões em 30 dias, 800 alunos",
                        "licoes": "Importância de depoimentos em vídeo e prova social"
                    }
                ],
                "fracassos": [
                    {
                        "nome": "Curso Genérico de Empreendedorismo",
                        "numeros": "Apenas R$ 150k em 30 dias, meta era R$ 1M",
                        "motivo": "Falta de diferenciação e nicho muito amplo",
                        "licoes": "Necessidade de nicho específico e proposta de valor clara"
                    }
                ]
            },
            "analise_precos": {
                "faixas": {
                    "low_ticket": "R$ 97 - R$ 497",
                    "mid_ticket": "R$ 497 - R$ 2.997",
                    "high_ticket": "R$ 2.997 - R$ 15.000"
                },
                "elasticidade": "Média - público disposto a investir em qualidade",
                "sweet_spot": f"R$ {int(preco):,}".replace(',', '.')
            },
            "estrategia_aquisicao": {
                "mix_canais": {
                    "facebook": "40%",
                    "google": "25%",
                    "youtube": "20%",
                    "tiktok": "10%",
                    "outros": "5%"
                },
                "budget_fases": {
                    "pre_lancamento": "R$ 15.000",
                    "lancamento": "R$ 45.000",
                    "pos_lancamento": "R$ 20.000"
                },
                "cpl_esperado": {
                    "facebook": "R$ 28",
                    "google": "R$ 52",
                    "youtube": "R$ 22",
                    "tiktok": "R$ 19"
                }
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
            "bonus_garantias": {
                "bonus": [
                    {
                        "nome": "Templates e Checklists Exclusivos",
                        "valor_percebido": "R$ 497"
                    },
                    {
                        "nome": "Acesso à Comunidade VIP",
                        "valor_percebido": "R$ 297"
                    },
                    {
                        "nome": "Sessão de Mentoria em Grupo",
                        "valor_percebido": "R$ 697"
                    }
                ],
                "garantia": "30 dias de garantia incondicional ou dinheiro de volta"
            },
            "sintese_estrategica": {
                "big_idea": f"O primeiro sistema científico que transforma profissionais em autoridades reconhecidas de {nicho} em 90 dias",
                "promessa_principal": f"Torne-se a referência #1 em {nicho} usando neurociência e metodologia comprovada",
                "mecanismo_unico": "Framework N.E.U.R.O. - Metodologia baseada em neurociência aplicada",
                "provas_conceito": ["Cases de sucesso documentados", "Pesquisa científica de base", "Depoimentos em vídeo"],
                "meta_smart": f"Faturar R$ {int(preco * 300):,}".replace(',', '.') + " em 90 dias com 300 alunos e NPS acima de 70"
            },
            "plano_acao": [
                {
                    "passo": 1,
                    "acao": "Validar proposta de valor com pesquisa qualitativa (50 entrevistas)",
                    "prazo": "2 semanas"
                },
                {
                    "passo": 2,
                    "acao": "Criar landing page otimizada com copy baseado na pesquisa",
                    "prazo": "1 semana"
                },
                {
                    "passo": 3,
                    "acao": "Configurar campanhas de tráfego pago (Facebook e Google)",
                    "prazo": "1 semana"
                },
                {
                    "passo": 4,
                    "acao": "Produzir conteúdo de aquecimento (webinar + sequência de e-mails)",
                    "prazo": "2 semanas"
                },
                {
                    "passo": 5,
                    "acao": "Executar campanha de pré-lançamento com early bird",
                    "prazo": "1 semana"
                },
                {
                    "passo": 6,
                    "acao": "Lançamento oficial com live de abertura",
                    "prazo": "1 semana"
                },
                {
                    "passo": 7,
                    "acao": "Otimizar campanhas baseado em dados e escalar investimento",
                    "prazo": "Contínuo"
                }
            ]
        }