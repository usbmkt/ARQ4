import os
import json
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
import time
import re

logger = logging.getLogger(__name__)

class DeepSeekClient:
    """Cliente avançado para DeepSeek API com análise de avatar ultra-detalhada"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY não encontrada nas variáveis de ambiente")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        
        # Configurações otimizadas para análise detalhada
        self.model = "deepseek-chat"
        self.max_tokens = 16000
        self.temperature = 0.3  # Baixa para consistência
        self.top_p = 0.8
        
    def analyze_avatar_comprehensive(self, data: Dict) -> Dict:
        """Análise ultra-detalhada do avatar com DeepSeek"""
        
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
            
            # Extrai e valida JSON
            analysis = self._extract_and_validate_json(content)
            
            if not analysis:
                raise ValueError("Não foi possível extrair análise válida da resposta")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise DeepSeek: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Prompt de sistema otimizado para análise de avatar"""
        return """
Você é um consultor sênior especializado em psicologia do consumidor, neurociência aplicada ao marketing e análise comportamental profunda. Sua expertise inclui:

1. PSICOLOGIA COMPORTAMENTAL: Análise de padrões de comportamento, motivações inconscientes e gatilhos emocionais
2. NEUROCIÊNCIA DO MARKETING: Como o cérebro processa informações e toma decisões de compra
3. ANTROPOLOGIA DIGITAL: Comportamentos online, tribos digitais e influência social
4. ECONOMIA COMPORTAMENTAL: Vieses cognitivos, heurísticas e tomada de decisão
5. SEGMENTAÇÃO PSICOGRÁFICA: Valores, atitudes, interesses e estilos de vida

Sua missão é criar análises de avatar extremamente detalhadas, precisas e acionáveis que revelem insights profundos sobre o cliente ideal, indo muito além de dados demográficos superficiais.

PRINCÍPIOS FUNDAMENTAIS:
- Baseie-se em pesquisas científicas e dados comportamentais reais
- Use frameworks psicológicos comprovados (Maslow, Big Five, Jobs-to-be-Done)
- Identifique padrões inconscientes e motivações ocultas
- Crie perfis tridimensionais com profundidade emocional
- Forneça insights acionáveis para estratégias de marketing
- Use linguagem precisa e científica, mas acessível
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
MISSÃO: Realize uma análise ULTRA-DETALHADA e CIENTÍFICA do avatar ideal para este produto/serviço, utilizando frameworks de psicologia comportamental, neurociência e antropologia digital.

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

ESTRUTURA OBRIGATÓRIA DA ANÁLISE:

## 🎯 DEFINIÇÃO DO ESCOPO
Identifique e detalhe:
- Nicho principal e subnichos
- Produto/serviço ideal para lançamento
- Proposta de valor única

## 👥 ANÁLISE DO AVATAR (CLIENTE IDEAL)

### Demografia:
Pesquise e defina:
- Faixa etária predominante
- Gênero e distribuição
- Localização geográfica principal
- Faixa de renda média
- Nível de escolaridade comum
- Profissões mais frequentes

### Psicografia:
Mapeie:
- 3 valores principais
- Estilo de vida característico
- 2 principais aspirações
- 3 medos mais comuns
- 2 frustrações recorrentes

### Comportamento Digital:
Identifique:
- 2 plataformas mais usadas
- Horários de pico online
- Tipos de conteúdo preferidos
- Influenciadores que seguem

## 💔 MAPEAMENTO DE DORES E DESEJOS

Liste as 5 principais dores com:
- Descrição detalhada
- Como impacta a vida
- Nível de urgência (Alta/Média/Baixa)

Identifique:
- Estado atual vs. Estado desejado
- Obstáculos percebidos
- Sonho secreto não verbalizado

## 🏆 ANÁLISE DA CONCORRÊNCIA

Pesquise e liste:
- 2 concorrentes diretos principais (com preços, USP, forças e fraquezas)
- 2 concorrentes indiretos
- 3 gaps identificados no mercado

## 💰 ANÁLISE DE MERCADO E METRIFICAÇÃO

### Calcule o TAM/SAM/SOM:
- TAM: População total × % mercado × ticket médio anual
- SAM: TAM × % segmento × % alcance realista
- SOM: SAM × % market share possível

### Identifique:
- Volume de busca mensal do nicho
- Tendências em alta e em queda
- Sazonalidade (melhores e piores meses)

## 🎯 ANÁLISE DE PALAVRAS-CHAVE E CUSTOS

Pesquise as 5 principais palavras-chave com:
- Volume de busca mensal
- CPC e CPM médios
- Dificuldade SEO
- Intenção de busca

### Custos por plataforma:
Estime para Facebook, Google, YouTube e TikTok:
- CPM médio
- CPC médio
- CPL médio
- Taxa de conversão esperada

## 📊 MÉTRICAS DE PERFORMANCE

Defina benchmarks do mercado:
- CAC médio por canal
- Funil de conversão padrão (%)
- LTV médio e LTV:CAC ratio
- ROI esperado por canal

## 🗣️ VOZ DO MERCADO

Identifique:
- 3 principais objeções e como contorná-las
- Linguagem específica (termos, gírias, gatilhos)
- 3 crenças limitantes comuns

## 📊 HISTÓRICO DE LANÇAMENTOS

Pesquise:
- 2 cases de sucesso (com números)
- 1 fracasso notável e lições aprendidas

## 💸 ANÁLISE DE PREÇOS

Mapeie:
- Faixas de preço (Low/Mid/High ticket)
- Elasticidade e sensibilidade a preço
- Sweet spot de preço

## 🚀 ESTRATÉGIA DE AQUISIÇÃO

Recomende:
- Mix ideal de canais (% do budget)
- Budget por fase (pré/lançamento/pós)
- CPL esperado por canal

## 📈 PROJEÇÕES

Apresente 3 cenários (conservador/realista/otimista):
- Taxa de conversão
- Faturamento projetado
- ROI esperado

## 🎁 BÔNUS E GARANTIAS

Sugira:
- 3 bônus valorizados com valor percebido
- Tipo de garantia ideal

## 🎯 SÍNTESE ESTRATÉGICA

Crie:
- Big Idea única para o lançamento
- Promessa principal irresistível
- Mecanismo único de entrega
- Provas de conceito necessárias
- Meta SMART completa

## 💡 PLANO DE AÇÃO

Liste 7 próximos passos prioritários e práticos.

IMPORTANTE: 
- Use dados reais e atualizados quando possível
- Faça estimativas conservadoras baseadas em padrões do mercado
- Seja específico com números e métricas
- Foque em insights acionáveis
- Retorne APENAS um JSON válido com toda a análise estruturada

Retorne a resposta em formato JSON seguindo exatamente esta estrutura:

{{
  "escopo": {{
    "nicho_principal": "string",
    "subnichos": ["string"],
    "produto_ideal": "string",
    "proposta_valor": "string"
  }},
  "avatar": {{
    "demografia": {{
      "faixa_etaria": "string",
      "genero": "string",
      "localizacao": "string",
      "renda": "string",
      "escolaridade": "string",
      "profissoes": ["string"]
    }},
    "psicografia": {{
      "valores": ["string"],
      "estilo_vida": "string",
      "aspiracoes": ["string"],
      "medos": ["string"],
      "frustracoes": ["string"]
    }},
    "comportamento_digital": {{
      "plataformas": ["string"],
      "horarios_pico": "string",
      "conteudo_preferido": ["string"],
      "influenciadores": ["string"]
    }}
  }},
  "dores_desejos": {{
    "principais_dores": [
      {{
        "descricao": "string",
        "impacto": "string",
        "urgencia": "string"
      }}
    ],
    "estado_atual": "string",
    "estado_desejado": "string",
    "obstaculos": ["string"],
    "sonho_secreto": "string"
  }},
  "concorrencia": {{
    "diretos": [
      {{
        "nome": "string",
        "preco": "string",
        "usp": "string",
        "forcas": ["string"],
        "fraquezas": ["string"]
      }}
    ],
    "indiretos": [
      {{
        "nome": "string",
        "tipo": "string"
      }}
    ],
    "gaps_mercado": ["string"]
  }},
  "mercado": {{
    "tam": "string",
    "sam": "string",
    "som": "string",
    "volume_busca": "string",
    "tendencias_alta": ["string"],
    "tendencias_baixa": ["string"],
    "sazonalidade": {{
      "melhores_meses": ["string"],
      "piores_meses": ["string"]
    }}
  }},
  "palavras_chave": {{
    "principais": [
      {{
        "termo": "string",
        "volume": "string",
        "cpc": "string",
        "dificuldade": "string",
        "intencao": "string"
      }}
    ],
    "custos_plataforma": {{
      "facebook": {{"cpm": "string", "cpc": "string", "cpl": "string", "conversao": "string"}},
      "google": {{"cpm": "string", "cpc": "string", "cpl": "string", "conversao": "string"}},
      "youtube": {{"cpm": "string", "cpc": "string", "cpl": "string", "conversao": "string"}},
      "tiktok": {{"cpm": "string", "cpc": "string", "cpl": "string", "conversao": "string"}}
    }}
  }},
  "metricas": {{
    "cac_medio": "string",
    "funil_conversao": ["string"],
    "ltv_medio": "string",
    "ltv_cac_ratio": "string",
    "roi_canais": {{
      "facebook": "string",
      "google": "string",
      "youtube": "string",
      "tiktok": "string"
    }}
  }},
  "voz_mercado": {{
    "objecoes": [
      {{
        "objecao": "string",
        "contorno": "string"
      }}
    ],
    "linguagem": {{
      "termos": ["string"],
      "girias": ["string"],
      "gatilhos": ["string"]
    }},
    "crencas_limitantes": ["string"]
  }},
  "historico_lancamentos": {{
    "sucessos": [
      {{
        "nome": "string",
        "numeros": "string",
        "licoes": "string"
      }}
    ],
    "fracassos": [
      {{
        "nome": "string",
        "motivo": "string",
        "licoes": "string"
      }}
    ]
  }},
  "analise_precos": {{
    "faixas": {{
      "low_ticket": "string",
      "mid_ticket": "string",
      "high_ticket": "string"
    }},
    "elasticidade": "string",
    "sweet_spot": "string"
  }},
  "estrategia_aquisicao": {{
    "mix_canais": {{
      "facebook": "string",
      "google": "string",
      "youtube": "string",
      "tiktok": "string",
      "outros": "string"
    }},
    "budget_fases": {{
      "pre_lancamento": "string",
      "lancamento": "string",
      "pos_lancamento": "string"
    }},
    "cpl_esperado": {{
      "facebook": "string",
      "google": "string",
      "youtube": "string",
      "tiktok": "string"
    }}
  }},
  "projecoes": {{
    "conservador": {{
      "conversao": "string",
      "faturamento": "string",
      "roi": "string"
    }},
    "realista": {{
      "conversao": "string",
      "faturamento": "string",
      "roi": "string"
    }},
    "otimista": {{
      "conversao": "string",
      "faturamento": "string",
      "roi": "string"
    }}
  }},
  "bonus_garantias": {{
    "bonus": [
      {{
        "nome": "string",
        "valor_percebido": "string"
      }}
    ],
    "garantia": "string"
  }},
  "sintese_estrategica": {{
    "big_idea": "string",
    "promessa_principal": "string",
    "mecanismo_unico": "string",
    "provas_conceito": ["string"],
    "meta_smart": "string"
  }},
  "plano_acao": [
    {{
      "passo": 1,
      "acao": "string",
      "prazo": "string"
    }}
  ]
}}
"""

    def _extract_and_validate_json(self, content: str) -> Optional[Dict]:
        """Extrai e valida JSON da resposta"""
        try:
            # Tenta encontrar JSON na resposta
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            
            # Se não encontrar, tenta parsear o conteúdo inteiro
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao extrair JSON: {e}")
            return None