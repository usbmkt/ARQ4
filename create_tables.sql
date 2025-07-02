-- Create analyses table
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    nicho VARCHAR(255) NOT NULL,
    produto VARCHAR(255),
    descricao TEXT,
    preco DECIMAL(10,2),
    publico VARCHAR(255),
    concorrentes TEXT,
    dados_adicionais TEXT,
    
    -- Analysis results stored as JSON
    avatar_data JSONB,
    positioning_data JSONB,
    competition_data JSONB,
    marketing_data JSONB,
    metrics_data JSONB,
    funnel_data JSONB,
    
    -- Metadata
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create analysis_templates table
CREATE TABLE IF NOT EXISTS analysis_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nicho VARCHAR(255) NOT NULL,
    template_data JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_analyses_nicho ON analyses(nicho);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_status ON analyses(status);
CREATE INDEX IF NOT EXISTS idx_analysis_templates_nicho ON analysis_templates(nicho);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_analyses_updated_at 
    BEFORE UPDATE ON analyses 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_templates ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust as needed for your security requirements)
CREATE POLICY "Allow all operations on analyses" ON analyses
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on analysis_templates" ON analysis_templates
    FOR ALL USING (true);

-- Insert some sample templates
INSERT INTO analysis_templates (name, nicho, template_data) VALUES 
('Template Neuroeducação', 'Neuroeducação', '{
    "avatar_base": {
        "faixa_etaria": "32-45 anos",
        "genero": "85% mulheres",
        "renda": "R$ 8.000 - R$ 25.000",
        "escolaridade": "Superior completo"
    },
    "dores_comuns": [
        "Gestão de birras e desobediência",
        "Preocupação com saúde emocional",
        "Falta de conexão familiar",
        "Sobrecarga e culpa",
        "Insegurança sobre o futuro"
    ]
}'),
('Template Marketing Digital', 'Marketing Digital', '{
    "avatar_base": {
        "faixa_etaria": "25-40 anos",
        "genero": "60% homens",
        "renda": "R$ 5.000 - R$ 20.000",
        "escolaridade": "Superior completo"
    },
    "dores_comuns": [
        "Dificuldade para gerar leads",
        "Baixo ROI em campanhas",
        "Falta de conhecimento técnico",
        "Concorrência acirrada",
        "Mudanças constantes no algoritmo"
    ]
}'),
('Template Fitness', 'Fitness', '{
    "avatar_base": {
        "faixa_etaria": "25-45 anos",
        "genero": "70% mulheres",
        "renda": "R$ 3.000 - R$ 15.000",
        "escolaridade": "Ensino médio/Superior"
    },
    "dores_comuns": [
        "Falta de tempo para exercitar",
        "Dificuldade para manter consistência",
        "Resultados lentos",
        "Falta de motivação",
        "Não saber por onde começar"
    ]
}')
ON CONFLICT DO NOTHING;

