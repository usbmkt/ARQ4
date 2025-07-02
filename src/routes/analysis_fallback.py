def create_fallback_analysis(nicho, produto, preco):
    """Create a comprehensive fallback analysis when Gemini AI fails"""
    
    # Default values for projections
    preco_num = float(preco) if preco else 997
    
    # More sophisticated projections
    leads_projetados = 8000  # Aumentado para refletir um cenário mais ambicioso
    conversao = 2.5        # Taxa de conversão otimista mas realista
    vendas = int(leads_projetados * (conversao / 100))
    faturamento = int(vendas * preco_num)
    investimento_total = 50000 # Investimento mais robusto
    roi = int(((faturamento - investimento_total) / investimento_total) * 100) if investimento_total > 0 else 0

    # Comprehensive fallback structure
    return {
        "avatar": {
            "nome": f"Carlos Eduardo Silva - Especialista em {nicho}",
            "idade": "38 anos",
            "profissao": "Empreendedor Digital e Consultor",
            "renda": "R$ 15.000 - R$ 35.000",
            "localizacao": "São Paulo, SP",
            "estado_civil": "Casado, 2 filhos",
            "contexto": f"Carlos é um profissional experiente que busca dominar {nicho} para escalar seu negócio. Trabalha 12 horas por dia, mas sente que não está progredindo na velocidade desejada. Valoriza metodologias comprovadas e resultados mensuráveis. Tem experiência em gestão, mas precisa de estratégias específicas para {nicho} que realmente funcionem no mercado brasileiro.",
            "barreira_critica": f"A principal barreira de Carlos é a paralisia por análise - ele consome muito conteúdo sobre {nicho}, mas tem dificuldade em transformar conhecimento em ação efetiva. Isso gera frustração constante e a sensação de estar sempre um passo atrás da concorrência, impactando sua confiança e capacidade de tomar decisões estratégicas rápidas.",
            "estado_desejado": f"Carlos deseja ser reconhecido como uma autoridade em {nicho}, com um negócio que gere pelo menos R$ 100.000 mensais de forma consistente, permitindo-lhe trabalhar apenas 6 horas por dia e ter mais tempo de qualidade com a família, viajando pelo menos 3 vezes por ano.",
            "frustracoes": [
                f"Excesso de informação contraditória sobre {nicho} disponível online",
                f"Dificuldade em encontrar estratégias que funcionem especificamente no mercado brasileiro",
                f"Falta de tempo para implementar todas as táticas que aprende",
                f"Sensação de estar sempre correndo atrás de novas tendências sem dominar as básicas",
                f"Dificuldade em mensurar o ROI real das estratégias implementadas em {nicho}",
                f"Pressão constante para gerar resultados rápidos enquanto constrói algo sustentável"
            ],
            "crenca_limitante": f"Carlos acredita que para ter sucesso em {nicho} é preciso trabalhar mais horas e estar sempre atualizado com as últimas tendências, quando na verdade o sucesso vem da consistência na execução de estratégias fundamentais bem implementadas.",
            "sonhos_aspiracoes": [
                f"Construir um império digital em {nicho} que funcione sem sua presença constante",
                "Ter liberdade financeira para investir em outros negócios e projetos pessoais",
                "Ser palestrante reconhecido e mentor de outros empreendedores em {nicho}"
            ],
            "onde_online": [
                "LinkedIn (grupos de empreendedorismo digital e marketing)",
                "Instagram (seguindo influenciadores de negócios e mentores)",
                "YouTube (canais de educação empresarial e estratégias de marketing)",
                "Telegram (grupos exclusivos de empreendedores)",
                "Podcasts sobre negócios e marketing digital"
            ]
        },
        "positioning": {
            "declaracao": f"Para empreendedores ambiciosos que querem dominar {nicho} sem perder a sanidade, {produto} é a única metodologia que combina estratégias comprovadas com implementação prática, garantindo resultados mensuráveis em 90 dias ou menos.",
            "angulos": [
                {
                    "tipo": "Lógico - Baseado em Dados",
                    "mensagem": f"Nossos alunos aumentaram em média 347% seu faturamento em {nicho} nos primeiros 6 meses. Metodologia testada com mais de 500 casos de sucesso no mercado brasileiro."
                },
                {
                    "tipo": "Emocional - Transformação de Vida", 
                    "mensagem": f"Imagine acordar sabendo exatamente o que fazer para crescer em {nicho}, sem a ansiedade de estar perdendo oportunidades. Tenha a confiança de quem domina seu mercado."
                },
                {
                    "tipo": "Contraste - Diferenciação Clara",
                    "mensagem": f"Enquanto outros vendem teoria e promessas vazias, {produto} entrega um sistema passo-a-passo com acompanhamento real até você alcançar seus resultados em {nicho}."
                },
                {
                    "tipo": "Urgência/Escassez - Oportunidade Limitada",
                    "mensagem": f"Apenas 50 vagas disponíveis para a próxima turma de {produto}. O mercado de {nicho} está mudando rapidamente - quem não se posicionar agora ficará para trás."
                }
            ],
            "proposta_valor_irrefutavel": f"{produto} é o único programa que oferece não apenas as estratégias mais avançadas de {nicho}, mas também implementação assistida, comunidade exclusiva de alto nível e garantia de resultados em 90 dias. Se você não alcançar pelo menos 200% de ROI no período, devolvemos 100% do investimento."
        },
        "competition": {
            "concorrentes": [
                {
                    "nome": f"MasterClass {nicho} Brasil",
                    "produto_servico": "Curso online com certificação",
                    "preco": int(preco_num * 0.6),
                    "forcas": "Marca reconhecida, conteúdo extenso, preço acessível, certificação oficial.",
                    "fraquezas": "Conteúdo muito teórico, sem acompanhamento personalizado, baixa taxa de conclusão (12%), não foca em resultados práticos mensuráveis.",
                    "oportunidade_diferenciacao": "Oferecer mentoria em grupo, foco total em implementação prática, garantia de resultados e comunidade ativa para networking."
                },
                {
                    "nome": f"Consultoria Premium {nicho}",
                    "produto_servico": "Consultoria individual 1-on-1",
                    "preco": int(preco_num * 4.0),
                    "forcas": "Atendimento 100% personalizado, consultor experiente, resultados rápidos para quem implementa.",
                    "fraquezas": "Preço inacessível para maioria (R$ 4.000+), não escalável, dependência total do consultor, sem comunidade.",
                    "oportunidade_diferenciacao": "Criar modelo híbrido com sessões em grupo + individual, reduzir custo mantendo qualidade, adicionar comunidade exclusiva."
                },
                {
                    "nome": f"Agência Full Service {nicho}",
                    "produto_servico": "Gestão completa de estratégias",
                    "preco": int(preco_num * 5.0),
                    "forcas": "Execução completa para o cliente, equipe especializada, resultados diretos sem esforço do cliente.",
                    "fraquezas": "Custo mensal muito alto (R$ 5.000+), cliente não aprende o processo, falta de controle, não desenvolve capacidade interna.",
                    "oportunidade_diferenciacao": "Ensinar o cliente a ser independente, oferecer ferramentas e processos, capacitação da equipe interna do cliente."
                }
            ],
            "lacunas_mercado": [
                f"Ausência de metodologia estruturada para {nicho} com foco no mercado brasileiro específico",
                "Falta de programas que combinem teoria + prática + acompanhamento + comunidade em um só lugar",
                "Carência de garantias reais de resultado em programas de {nicho}",
                "Pouco foco em mentalidade empreendedora e superação de crenças limitantes específicas do mercado brasileiro"
            ],
            "benchmarking_melhores_praticas": [
                "Modelo de mentoria em grupo com sessões semanais ao vivo (inspirado em programas americanos de alto ticket)",
                "Comunidade exclusiva no Discord/Telegram com networking ativo e troca de experiências",
                "Sistema de implementação assistida com templates, checklists e ferramentas prontas para usar"
            ]
        },
        "marketing": {
            "landing_page_headlines": [
                f"A Metodologia Que Está Transformando Empreendedores em Autoridades de {nicho} (Resultados em 90 Dias)",
                f"Como Dominar {nicho} e Faturar 6 Dígitos Sem Trabalhar 12 Horas Por Dia",
                f"O Sistema Completo Para Você Se Tornar Referência em {nicho} e Construir Um Negócio de Alto Impacto"
            ],
            "pagina_vendas_estrutura": [
                {
                    "titulo": "A Frustração Que Todo Empreendedor de {nicho} Conhece",
                    "resumo_conteudo": "Abrir com a dor específica: excesso de informação, falta de resultados práticos, sensação de estar sempre correndo atrás. Usar dados e estatísticas sobre o mercado."
                },
                {
                    "titulo": "A Descoberta Que Mudou Tudo",
                    "resumo_conteudo": "História do criador do método, como descobriu a fórmula que funciona, primeiros resultados e validação da metodologia."
                },
                {
                    "titulo": "Apresentando {produto} - O Sistema Definitivo",
                    "resumo_conteudo": "Apresentação da solução, pilares da metodologia, diferencial competitivo e por que funciona especificamente no Brasil."
                },
                {
                    "titulo": "Prova Social Irrefutável - Resultados Reais",
                    "resumo_conteudo": "Depoimentos em vídeo, cases de sucesso com números reais, antes e depois dos alunos, dados de performance."
                },
                {
                    "titulo": "O Que Você Vai Receber (Valor Entregue)",
                    "resumo_conteudo": "Detalhamento completo dos módulos, bônus, ferramentas, templates, acesso à comunidade, sessões de mentoria."
                },
                {
                    "titulo": "Garantia Blindada de Resultados",
                    "resumo_conteudo": "Garantia de 90 dias, condições claras, como funciona o processo de reembolso, redução de risco para o cliente."
                },
                {
                    "titulo": "Oferta Especial Por Tempo Limitado",
                    "resumo_conteudo": "Preço promocional, bônus exclusivos, condições de pagamento, comparação de valor vs investimento."
                },
                {
                    "titulo": "Perguntas Frequentes",
                    "resumo_conteudo": "Quebra de objeções principais: tempo, dinheiro, experiência, resultados, suporte técnico."
                },
                {
                    "titulo": "Última Chance - Garanta Sua Vaga",
                    "resumo_conteudo": "CTA final com urgência, escassez real (vagas limitadas), resumo dos benefícios, botão de compra destacado."
                }
            ],
            "emails_assuntos": [
                f"[REVELADO] O segredo dos top 1% em {nicho} que ninguém te conta",
                f"🚀 {produto} - Vagas abertas para a turma mais exclusiva do ano",
                f"Por que 97% dos empreendedores falham em {nicho} (e como estar nos 3%)",
                f"⚠️ URGENTE: Últimas 12 vagas para {produto} - Encerra amanhã",
                f"⏰ FINAL: {produto} encerra hoje às 23:59 - Não perca sua chance"
            ],
            "anuncios_roteiros": [
                {
                    "angulo": "Dor + Solução + Prova Social",
                    "roteiro": f"Cansado de estudar {nicho} mas não ver resultados? Conheça {produto}, a metodologia que já transformou mais de 500 empreendedores em autoridades do mercado. João saiu do zero e faturou R$ 80.000 em 4 meses. Clique e descubra como!"
                },
                {
                    "angulo": "Autoridade + Transformação",
                    "roteiro": f"Sou [Nome do Criador], e nos últimos 8 anos ajudei centenas de pessoas a dominarem {nicho}. Se você quer sair da teoria e partir para resultados reais, {produto} é para você. Vagas limitadas - clique agora!"
                },
                {
                    "angulo": "Urgência + Benefício Claro",
                    "roteiro": f"ÚLTIMAS VAGAS: {produto} está encerrando e pode ser sua última chance de dominar {nicho} com quem realmente entende do mercado brasileiro. Não fique para trás enquanto seus concorrentes avançam. Garante sua vaga!"
                }
            ]
        },
        "metrics": {
            "leads_necessarios": leads_projetados,
            "taxa_conversao_realista": f"{conversao}%",
            "projecao_faturamento_3_meses": f"R$ {int(faturamento * 0.4):,}".replace(',', '.'),
            "projecao_faturamento_6_meses": f"R$ {int(faturamento * 0.7):,}".replace(',', '.'),
            "projecao_faturamento_12_meses": f"R$ {faturamento:,}".replace(',', '.'),
            "roi_otimista": f"{int(((faturamento * 1.8 - investimento_total) / investimento_total) * 100)}%",
            "roi_realista": f"{roi}%",
            "distribuicao_investimento": [
                {
                    "canal": "Meta Ads (Facebook + Instagram)",
                    "percentual": "45%",
                    "valor": f"R$ {int(investimento_total * 0.45):,}".replace(',', '.')
                },
                {
                    "canal": "Google Ads (Search + YouTube)",
                    "percentual": "25%",
                    "valor": f"R$ {int(investimento_total * 0.25):,}".replace(',', '.')
                },
                {
                    "canal": "Conteúdo Orgânico + SEO",
                    "percentual": "15%",
                    "valor": f"R$ {int(investimento_total * 0.15):,}".replace(',', '.')
                },
                {
                    "canal": "E-mail Marketing + Automação",
                    "percentual": "10%",
                    "valor": f"R$ {int(investimento_total * 0.10):,}".replace(',', '.')
                },
                {
                    "canal": "Parcerias + Afiliados",
                    "percentual": "5%",
                    "valor": f"R$ {int(investimento_total * 0.05):,}".replace(',', '.')
                }
            ]
        },
        "funnel": {
            "fases": [
                {
                    "nome": "Consciência e Atração (Awareness)",
                    "objetivo": "Atrair o público-alvo qualificado e gerar reconhecimento da marca como autoridade em {nicho}.",
                    "acoes_marketing": "Conteúdo de valor no blog e redes sociais, anúncios de topo de funil, SEO para palavras-chave do nicho, participação em podcasts e eventos.",
                    "metricas_acompanhamento": [
                        "Alcance e impressões dos anúncios",
                        "Tráfego orgânico e pago para o site",
                        "Engajamento nas redes sociais",
                        "Menções da marca e share of voice"
                    ]
                },
                {
                    "nome": "Interesse e Educação (Interest)",
                    "objetivo": "Educar o lead sobre os problemas de {nicho} e posicionar nossa solução como a mais adequada.",
                    "acoes_marketing": "Webinars educativos, e-books e guias gratuitos, sequência de e-mails com conteúdo de valor, retargeting para visitantes do site.",
                    "metricas_acompanhamento": [
                        "Taxa de conversão de visitante para lead",
                        "Taxa de abertura e clique dos e-mails",
                        "Participação nos webinars",
                        "Download de materiais gratuitos"
                    ]
                },
                {
                    "nome": "Consideração e Avaliação (Consideration)",
                    "objetivo": "Demonstrar credibilidade, quebrar objeções e posicionar o produto como a melhor escolha.",
                    "acoes_marketing": "Cases de sucesso detalhados, depoimentos em vídeo, demonstrações do produto, comparações com concorrentes, FAQ completo.",
                    "metricas_acompanhamento": [
                        "Tempo gasto na página de vendas",
                        "Visualizações dos depoimentos",
                        "Interações com o FAQ",
                        "Solicitações de informações adicionais"
                    ]
                },
                {
                    "nome": "Intenção de Compra (Intent)",
                    "objetivo": "Converter leads qualificados em clientes, removendo últimas objeções e criando urgência.",
                    "acoes_marketing": "Ofertas por tempo limitado, bônus exclusivos, garantias estendidas, remarketing agressivo, e-mails de carrinho abandonado.",
                    "metricas_acompanhamento": [
                        "Adições ao carrinho",
                        "Início do processo de checkout",
                        "Taxa de abandono de carrinho",
                        "Conversões por fonte de tráfego"
                    ]
                },
                {
                    "nome": "Compra e Conversão (Purchase)",
                    "objetivo": "Facilitar o processo de compra e maximizar o valor do pedido.",
                    "acoes_marketing": "Checkout otimizado, múltiplas opções de pagamento, upsells e cross-sells, suporte em tempo real durante a compra.",
                    "metricas_acompanhamento": [
                        "Taxa de conversão final",
                        "Ticket médio",
                        "Taxa de sucesso de upsells",
                        "Tempo médio de checkout"
                    ]
                },
                {
                    "nome": "Pós-Venda e Fidelização (Retention)",
                    "objetivo": "Garantir satisfação, maximizar LTV e transformar clientes em promotores da marca.",
                    "acoes_marketing": "Onboarding estruturado, suporte proativo, programa de fidelidade, solicitação de depoimentos, programa de indicações.",
                    "metricas_acompanhamento": [
                        "Taxa de satisfação (NPS)",
                        "Taxa de retenção",
                        "Lifetime Value (LTV)",
                        "Número de indicações geradas"
                    ]
                }
            ],
            "cronograma_execucao": "**Semana 1-2: Pré-aquecimento** (Conteúdo de valor, construção de audiência). **Semana 3: Lançamento** (Webinar de lançamento, abertura de carrinho). **Semana 4: Intensificação** (Depoimentos, quebra de objeções, casos de sucesso). **Semana 5: Urgência** (Bônus finais, escassez real, últimos avisos). **Semana 6: Fechamento** (Encerramento oficial, últimas horas). **Pós-lançamento:** Onboarding e entrega de valor contínuo.",
            "metricas_criticas": [
                "Custo por Lead Qualificado (CPL) - Meta: R$ 15-25",
                "Taxa de Conversão do Funil Completo - Meta: 2-3%",
                "Custo por Aquisição (CPA) - Meta: R$ 300-500",
                "Retorno sobre Investimento (ROI) - Meta: 300-500%",
                "Lifetime Value (LTV) - Meta: R$ 2.000-3.000"
            ]
        }
    }

