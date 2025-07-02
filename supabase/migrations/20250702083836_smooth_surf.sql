-- Corrigir schema para incluir todas as colunas necessárias
-- Adicionar colunas que estão faltando na tabela analyses

-- Verificar se as colunas existem antes de adicionar
DO $$
BEGIN
    -- Adicionar objetivo_receita se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' AND column_name = 'objetivo_receita'
    ) THEN
        ALTER TABLE analyses ADD COLUMN objetivo_receita DECIMAL(15,2);
    END IF;

    -- Adicionar orcamento_marketing se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' AND column_name = 'orcamento_marketing'
    ) THEN
        ALTER TABLE analyses ADD COLUMN orcamento_marketing DECIMAL(15,2);
    END IF;

    -- Adicionar prazo_lancamento se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' AND column_name = 'prazo_lancamento'
    ) THEN
        ALTER TABLE analyses ADD COLUMN prazo_lancamento VARCHAR(100);
    END IF;

    -- Adicionar comprehensive_analysis se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' AND column_name = 'comprehensive_analysis'
    ) THEN
        ALTER TABLE analyses ADD COLUMN comprehensive_analysis JSONB;
    END IF;

    -- Adicionar market_intelligence se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' AND column_name = 'market_intelligence'
    ) THEN
        ALTER TABLE analyses ADD COLUMN market_intelligence JSONB;
    END IF;

    -- Adicionar action_plan se não existir
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'analyses' AND column_name = 'action_plan'
    ) THEN
        ALTER TABLE analyses ADD COLUMN action_plan JSONB;
    END IF;
END $$;

-- Adicionar comentários para documentação
COMMENT ON COLUMN analyses.objetivo_receita IS 'Meta de receita para o lançamento';
COMMENT ON COLUMN analyses.orcamento_marketing IS 'Orçamento disponível para marketing';
COMMENT ON COLUMN analyses.prazo_lancamento IS 'Prazo desejado para o lançamento';
COMMENT ON COLUMN analyses.comprehensive_analysis IS 'Análise completa gerada pelo DeepSeek AI';

-- Criar índice para a nova coluna comprehensive_analysis se não existir
CREATE INDEX IF NOT EXISTS idx_analyses_comprehensive_analysis 
ON analyses USING GIN (comprehensive_analysis);

-- Atualizar função de trigger se necessário
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';