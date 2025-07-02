-- Análise de Avatar - Schema Completo
-- Criado para suportar análises ultra-detalhadas com DeepSeek AI

-- Remover tabelas existentes se houver
DROP TABLE IF EXISTS analyses CASCADE;
DROP TABLE IF EXISTS analysis_templates CASCADE;

-- Criar tabela principal de análises
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    
    -- Dados básicos do produto/serviço
    nicho VARCHAR(255) NOT NULL,
    produto VARCHAR(255),
    descricao TEXT,
    preco DECIMAL(10,2),
    publico VARCHAR(500),
    concorrentes TEXT,
    dados_adicionais TEXT,
    
    -- Novos campos para análise completa
    objetivo_receita DECIMAL(15,2),
    orcamento_marketing DECIMAL(15,2),
    prazo_lancamento VARCHAR(100),
    
    -- Resultados da análise em formato JSON
    avatar_data JSONB,
    positioning_data JSONB,
    competition_data JSONB,
    marketing_data JSONB,
    metrics_data JSONB,
    funnel_data JSONB,
    market_intelligence JSONB,
    action_plan JSONB,
    
    -- Análise completa do DeepSeek
    comprehensive_analysis JSONB,
    
    -- Metadados
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar tabela de templates de análise
CREATE TABLE analysis_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nicho VARCHAR(255) NOT NULL,
    template_data JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para performance
CREATE INDEX idx_analyses_nicho ON analyses(nicho);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX idx_analyses_status ON analyses(status);
CREATE INDEX idx_analysis_templates_nicho ON analysis_templates(nicho);
CREATE INDEX idx_analyses_comprehensive ON analyses USING GIN (comprehensive_analysis);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para updated_at
CREATE TRIGGER update_analyses_updated_at 
    BEFORE UPDATE ON analyses 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Habilitar Row Level Security
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_templates ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso (ajustar conforme necessário)
CREATE POLICY "Allow all operations on analyses" ON analyses
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on analysis_templates" ON analysis_templates
    FOR ALL USING (true);

-- Inserir templates de exemplo
INSERT INTO analysis_templates (name, nicho, template_data) VALUES 
('Template Neuroeducação Avançado', 'Neuroeducação', '{
    "avatar_base": {
        "faixa_etaria": "32-45 anos",
        "genero": "85% mulheres",
        "renda": "R$ 8.000 - R$ 25.000",
        "escolaridade": "Superior completo",
        "localizacao": "Região Sudeste e Sul"
    },
    "dores_principais": [
        "Gestão de birras e comportamentos desafiadores",
        "Preocupação com desenvolvimento emocional dos filhos",
        "Falta de conexão e comunicação familiar",
        "Sobrecarga emocional e culpa materna",
        "Insegurança sobre métodos educacionais"
    ],
    "mercado": {
        "tam": "R$ 2.8 bilhões",
        "sam": "R$ 420 milhões",
        "som": "R$ 28 milhões"
    }
}'),
('Template Marketing Digital Pro', 'Marketing Digital', '{
    "avatar_base": {
        "faixa_etaria": "28-42 anos",
        "genero": "55% homens, 45% mulheres",
        "renda": "R$ 5.000 - R$ 20.000",
        "escolaridade": "Superior completo",
        "localizacao": "Grandes centros urbanos"
    },
    "dores_principais": [
        "Dificuldade para gerar leads qualificados",
        "Baixo ROI em campanhas de tráfego pago",
        "Falta de conhecimento técnico atualizado",
        "Concorrência acirrada no mercado",
        "Mudanças constantes nos algoritmos"
    ],
    "mercado": {
        "tam": "R$ 4.2 bilhões",
        "sam": "R$ 630 milhões",
        "som": "R$ 42 milhões"
    }
}'),
('Template Fitness e Bem-estar', 'Fitness', '{
    "avatar_base": {
        "faixa_etaria": "25-45 anos",
        "genero": "70% mulheres, 30% homens",
        "renda": "R$ 3.000 - R$ 15.000",
        "escolaridade": "Ensino médio/Superior",
        "localizacao": "Centros urbanos e subúrbios"
    },
    "dores_principais": [
        "Falta de tempo para exercitar-se regularmente",
        "Dificuldade para manter consistência nos treinos",
        "Resultados lentos e desmotivação",
        "Falta de conhecimento sobre nutrição",
        "Não saber por onde começar a mudança"
    ],
    "mercado": {
        "tam": "R$ 1.8 bilhões",
        "sam": "R$ 270 milhões",
        "som": "R$ 18 milhões"
    }
}')
ON CONFLICT DO NOTHING;

-- Comentários para documentação
COMMENT ON TABLE analyses IS 'Tabela principal para armazenar análises de avatar ultra-detalhadas';
COMMENT ON COLUMN analyses.comprehensive_analysis IS 'Análise completa gerada pelo DeepSeek AI em formato JSON';
COMMENT ON TABLE analysis_templates IS 'Templates pré-configurados para diferentes nichos de mercado';