// Global variables
let currentAnalysis = null;
let analysisInProgress = false;

// DOM Elements
const sections = {
    home: document.getElementById('home'),
    analyzer: document.getElementById('analyzer'),
    dashboard: document.getElementById('dashboard')
};

const navLinks = document.querySelectorAll('.neo-nav-link');
const analyzerForm = document.getElementById('analyzerForm');
const loadingState = document.getElementById('loadingState');
const resultsContainer = document.getElementById('resultsContainer');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const loadingText = document.getElementById('loadingText');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeForm();
    initializeHeader();
    initializeSearch();
});

// Navigation functionality
function initializeNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            showSection(targetId);
            updateActiveNav(this);
        });
    });
}

function showSection(sectionId) {
    // Hide all sections
    Object.values(sections).forEach(section => {
        if (section) section.style.display = 'none';
    });
    
    // Show target section
    if (sections[sectionId]) {
        sections[sectionId].style.display = 'block';
    }
}

function updateActiveNav(activeLink) {
    navLinks.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

function showAnalyzer() {
    showSection('analyzer');
    updateActiveNav(document.querySelector('a[href="#analyzer"]'));
}

// Header scroll effect
function initializeHeader() {
    const header = document.getElementById('header');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// Form functionality
function initializeForm() {
    if (analyzerForm) {
        analyzerForm.addEventListener('submit', handleFormSubmit);
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (analysisInProgress) return;
    
    const formData = new FormData(analyzerForm);
    const data = Object.fromEntries(formData.entries());
    
    // Validate required fields
    if (!data.nicho.trim()) {
        showNotification('Por favor, informe o nicho de atuação.', 'error');
        return;
    }
    
    analysisInProgress = true;
    showDashboard();
    showLoading();
    
    try {
        await performAnalysis(data);
    } catch (error) {
        console.error('Erro na análise:', error);
        showNotification('Erro ao realizar análise. Tente novamente.', 'error');
        analysisInProgress = false;
        hideLoading();
    }
}

function showDashboard() {
    showSection('dashboard');
    updateActiveNav(document.querySelector('a[href="#dashboard"]'));
}

function showLoading() {
    loadingState.style.display = 'block';
    resultsContainer.style.display = 'none';
    
    // Simulate progress
    simulateProgress();
}

function simulateProgress() {
    const steps = [
        { progress: 10, text: 'Conectando com DeepSeek AI...' },
        { progress: 20, text: 'Analisando nicho de mercado...' },
        { progress: 35, text: 'Mapeando avatar ideal...' },
        { progress: 50, text: 'Pesquisando concorrência...' },
        { progress: 65, text: 'Calculando métricas de mercado...' },
        { progress: 80, text: 'Gerando estratégias de aquisição...' },
        { progress: 95, text: 'Finalizando análise ultra-detalhada...' },
        { progress: 100, text: 'Análise concluída com sucesso!' }
    ];
    
    let currentStep = 0;
    
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            updateProgress(step.progress, step.text);
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 1800);
}

function updateProgress(percentage, text) {
    progressBar.style.width = percentage + '%';
    progressText.textContent = percentage + '%';
    loadingText.textContent = text;
}

async function performAnalysis(data) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentAnalysis = result;
        
        // Wait for progress simulation to complete
        setTimeout(() => {
            hideLoading();
            displayResults(result);
            analysisInProgress = false;
        }, 15000); // 15 seconds total for progress simulation
        
    } catch (error) {
        console.error('Erro na análise:', error);
        hideLoading();
        showNotification('Erro ao realizar análise: ' + error.message, 'error');
        analysisInProgress = false;
    }
}

function hideLoading() {
    loadingState.style.display = 'none';
    resultsContainer.style.display = 'block';
}

function displayResults(analysis) {
    resultsContainer.innerHTML = generateResultsHTML(analysis);
    
    // Initialize interactive elements
    initializeResultsInteractions();
}

function generateResultsHTML(analysis) {
    return `
        <div class="results-header">
            <div class="neo-enhanced-card">
                <div class="neo-card-header">
                    <div class="neo-card-icon">
                        <i class="fas fa-trophy"></i>
                    </div>
                    <h3 class="neo-card-title">Análise Ultra-Detalhada Concluída</h3>
                </div>
                <div class="neo-card-content">
                    <p>Sua análise de avatar foi processada pelo DeepSeek AI com neurociência aplicada. Explore os insights profundos abaixo.</p>
                    <div class="results-actions">
                        <button class="neo-cta-button" onclick="downloadReport()">
                            <i class="fas fa-download"></i>
                            <span>Baixar Relatório Completo</span>
                        </button>
                        <button class="neo-cta-button" onclick="shareResults()" style="background: var(--neo-bg); color: var(--text-primary); box-shadow: var(--neo-shadow-1);">
                            <i class="fas fa-share"></i>
                            <span>Compartilhar</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="results-grid">
            ${generateEscopoSection(analysis.escopo)}
            ${generateAvatarSection(analysis.avatar)}
            ${generateDoresSection(analysis.dores_desejos)}
            ${generateConcorrenciaSection(analysis.concorrencia)}
            ${generateMercadoSection(analysis.mercado)}
            ${generatePalavrasChaveSection(analysis.palavras_chave)}
            ${generateMetricasSection(analysis.metricas)}
            ${generateVozMercadoSection(analysis.voz_mercado)}
            ${generateProjecoesSection(analysis.projecoes)}
            ${generatePlanoAcaoSection(analysis.plano_acao)}
        </div>
    `;
}

function generateEscopoSection(escopo) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-bullseye"></i>
                </div>
                <h3 class="neo-card-title">Definição do Escopo</h3>
            </div>
            <div class="neo-card-content">
                <div class="escopo-content">
                    <div class="detail-item">
                        <strong>Nicho Principal:</strong>
                        <p>${escopo.nicho_principal}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Subnichos Identificados:</strong>
                        <ul>
                            ${escopo.subnichos.map(sub => `<li>${sub}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Produto Ideal:</strong>
                        <p>${escopo.produto_ideal}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Proposta de Valor:</strong>
                        <blockquote>${escopo.proposta_valor}</blockquote>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateAvatarSection(avatar) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-user-circle"></i>
                </div>
                <h3 class="neo-card-title">Avatar Ultra-Detalhado</h3>
            </div>
            <div class="neo-card-content">
                <div class="avatar-profile">
                    <div class="avatar-section">
                        <h4>Demografia</h4>
                        <div class="detail-grid">
                            <div class="detail-item">
                                <strong>Faixa Etária:</strong>
                                <p>${avatar.demografia.faixa_etaria}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Gênero:</strong>
                                <p>${avatar.demografia.genero}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Localização:</strong>
                                <p>${avatar.demografia.localizacao}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Renda:</strong>
                                <p>${avatar.demografia.renda}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Escolaridade:</strong>
                                <p>${avatar.demografia.escolaridade}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Profissões:</strong>
                                <ul>
                                    ${avatar.demografia.profissoes.map(prof => `<li>${prof}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="avatar-section">
                        <h4>Psicografia</h4>
                        <div class="detail-item">
                            <strong>Valores Principais:</strong>
                            <ul>
                                ${avatar.psicografia.valores.map(valor => `<li>${valor}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="detail-item">
                            <strong>Estilo de Vida:</strong>
                            <p>${avatar.psicografia.estilo_vida}</p>
                        </div>
                        <div class="detail-item">
                            <strong>Aspirações:</strong>
                            <ul>
                                ${avatar.psicografia.aspiracoes.map(asp => `<li>${asp}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="detail-item">
                            <strong>Medos:</strong>
                            <ul>
                                ${avatar.psicografia.medos.map(medo => `<li>${medo}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="detail-item">
                            <strong>Frustrações:</strong>
                            <ul>
                                ${avatar.psicografia.frustracoes.map(frust => `<li>${frust}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                    
                    <div class="avatar-section">
                        <h4>Comportamento Digital</h4>
                        <div class="detail-item">
                            <strong>Plataformas Principais:</strong>
                            <ul>
                                ${avatar.comportamento_digital.plataformas.map(plat => `<li>${plat}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="detail-item">
                            <strong>Horários de Pico:</strong>
                            <p>${avatar.comportamento_digital.horarios_pico}</p>
                        </div>
                        <div class="detail-item">
                            <strong>Conteúdo Preferido:</strong>
                            <ul>
                                ${avatar.comportamento_digital.conteudo_preferido.map(cont => `<li>${cont}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="detail-item">
                            <strong>Influenciadores:</strong>
                            <ul>
                                ${avatar.comportamento_digital.influenciadores.map(inf => `<li>${inf}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateDoresSection(dores) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-heart-broken"></i>
                </div>
                <h3 class="neo-card-title">Mapeamento de Dores e Desejos</h3>
            </div>
            <div class="neo-card-content">
                <div class="dores-content">
                    <div class="detail-item">
                        <strong>Principais Dores:</strong>
                        <div class="dores-list">
                            ${dores.principais_dores.map((dor, index) => `
                                <div class="dor-item">
                                    <h5>Dor ${index + 1} - Urgência: ${dor.urgencia}</h5>
                                    <p><strong>Descrição:</strong> ${dor.descricao}</p>
                                    <p><strong>Impacto:</strong> ${dor.impacto}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Estado Atual vs Desejado:</strong>
                        <p><strong>Atual:</strong> ${dores.estado_atual}</p>
                        <p><strong>Desejado:</strong> ${dores.estado_desejado}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Obstáculos Percebidos:</strong>
                        <ul>
                            ${dores.obstaculos.map(obs => `<li>${obs}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Sonho Secreto:</strong>
                        <blockquote>${dores.sonho_secreto}</blockquote>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateConcorrenciaSection(concorrencia) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-chess"></i>
                </div>
                <h3 class="neo-card-title">Análise da Concorrência</h3>
            </div>
            <div class="neo-card-content">
                <div class="concorrencia-content">
                    <div class="detail-item">
                        <strong>Concorrentes Diretos:</strong>
                        ${concorrencia.diretos.map(conc => `
                            <div class="competitor-item">
                                <h5>${conc.nome} - ${conc.preco}</h5>
                                <p><strong>USP:</strong> ${conc.usp}</p>
                                <p><strong>Forças:</strong> ${conc.forcas.join(', ')}</p>
                                <p><strong>Fraquezas:</strong> ${conc.fraquezas.join(', ')}</p>
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="detail-item">
                        <strong>Concorrentes Indiretos:</strong>
                        ${concorrencia.indiretos.map(ind => `
                            <div class="competitor-item">
                                <h5>${ind.nome}</h5>
                                <p><strong>Tipo:</strong> ${ind.tipo}</p>
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="detail-item">
                        <strong>Gaps do Mercado:</strong>
                        <ul>
                            ${concorrencia.gaps_mercado.map(gap => `<li>${gap}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateMercadoSection(mercado) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-chart-pie"></i>
                </div>
                <h3 class="neo-card-title">Análise de Mercado</h3>
            </div>
            <div class="neo-card-content">
                <div class="mercado-content">
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-value">${mercado.tam}</div>
                            <div class="metric-label">TAM (Total Addressable Market)</div>
                        </div>
                        
                        <div class="metric-item">
                            <div class="metric-value">${mercado.sam}</div>
                            <div class="metric-label">SAM (Serviceable Addressable Market)</div>
                        </div>
                        
                        <div class="metric-item">
                            <div class="metric-value">${mercado.som}</div>
                            <div class="metric-label">SOM (Serviceable Obtainable Market)</div>
                        </div>
                        
                        <div class="metric-item">
                            <div class="metric-value">${mercado.volume_busca}</div>
                            <div class="metric-label">Volume de Busca Mensal</div>
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Tendências em Alta:</strong>
                        <ul>
                            ${mercado.tendencias_alta.map(tend => `<li>${tend}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Tendências em Baixa:</strong>
                        <ul>
                            ${mercado.tendencias_baixa.map(tend => `<li>${tend}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Sazonalidade:</strong>
                        <p><strong>Melhores meses:</strong> ${mercado.sazonalidade.melhores_meses.join(', ')}</p>
                        <p><strong>Piores meses:</strong> ${mercado.sazonalidade.piores_meses.join(', ')}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generatePalavrasChaveSection(palavras) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-search"></i>
                </div>
                <h3 class="neo-card-title">Análise de Palavras-Chave</h3>
            </div>
            <div class="neo-card-content">
                <div class="palavras-content">
                    <div class="detail-item">
                        <strong>Principais Palavras-Chave:</strong>
                        <div class="keywords-table">
                            ${palavras.principais.map(kw => `
                                <div class="keyword-row">
                                    <span class="keyword">${kw.termo}</span>
                                    <span class="volume">${kw.volume}/mês</span>
                                    <span class="cpc">${kw.cpc}</span>
                                    <span class="difficulty ${kw.dificuldade.toLowerCase()}">${kw.dificuldade}</span>
                                    <span class="intent">${kw.intencao}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Custos por Plataforma:</strong>
                        <div class="platform-costs">
                            ${Object.entries(palavras.custos_plataforma).map(([platform, costs]) => `
                                <div class="platform-item">
                                    <h5>${platform.charAt(0).toUpperCase() + platform.slice(1)}</h5>
                                    <p>CPM: ${costs.cpm} | CPC: ${costs.cpc} | CPL: ${costs.cpl} | Conversão: ${costs.conversao}</p>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateMetricasSection(metricas) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h3 class="neo-card-title">Métricas de Performance</h3>
            </div>
            <div class="neo-card-content">
                <div class="metricas-content">
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-value">${metricas.cac_medio}</div>
                            <div class="metric-label">CAC Médio</div>
                        </div>
                        
                        <div class="metric-item">
                            <div class="metric-value">${metricas.ltv_medio}</div>
                            <div class="metric-label">LTV Médio</div>
                        </div>
                        
                        <div class="metric-item">
                            <div class="metric-value">${metricas.ltv_cac_ratio}</div>
                            <div class="metric-label">LTV:CAC Ratio</div>
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Funil de Conversão:</strong>
                        <div class="funnel-steps">
                            ${metricas.funil_conversao.map(step => `<div class="funnel-step">${step}</div>`).join('')}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>ROI por Canal:</strong>
                        <div class="roi-channels">
                            ${Object.entries(metricas.roi_canais).map(([channel, roi]) => `
                                <div class="roi-item">
                                    <span class="channel">${channel.charAt(0).toUpperCase() + channel.slice(1)}</span>
                                    <span class="roi">${roi}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateVozMercadoSection(voz) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-comments"></i>
                </div>
                <h3 class="neo-card-title">Voz do Mercado</h3>
            </div>
            <div class="neo-card-content">
                <div class="voz-content">
                    <div class="detail-item">
                        <strong>Principais Objeções:</strong>
                        ${voz.objecoes.map(obj => `
                            <div class="objecao-item">
                                <h5>Objeção: "${obj.objecao}"</h5>
                                <p><strong>Contorno:</strong> ${obj.contorno}</p>
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="detail-item">
                        <strong>Linguagem do Mercado:</strong>
                        <p><strong>Termos:</strong> ${voz.linguagem.termos.join(', ')}</p>
                        <p><strong>Gírias:</strong> ${voz.linguagem.girias.join(', ')}</p>
                        <p><strong>Gatilhos:</strong> ${voz.linguagem.gatilhos.join(', ')}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Crenças Limitantes:</strong>
                        <ul>
                            ${voz.crencas_limitantes.map(crenca => `<li>${crenca}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateProjecoesSection(projecoes) {
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <h3 class="neo-card-title">Projeções de Resultados</h3>
            </div>
            <div class="neo-card-content">
                <div class="projecoes-content">
                    <div class="scenarios-grid">
                        <div class="scenario-item conservador">
                            <h4>Cenário Conservador</h4>
                            <p><strong>Conversão:</strong> ${projecoes.conservador.conversao}</p>
                            <p><strong>Faturamento:</strong> ${projecoes.conservador.faturamento}</p>
                            <p><strong>ROI:</strong> ${projecoes.conservador.roi}</p>
                        </div>
                        
                        <div class="scenario-item realista">
                            <h4>Cenário Realista</h4>
                            <p><strong>Conversão:</strong> ${projecoes.realista.conversao}</p>
                            <p><strong>Faturamento:</strong> ${projecoes.realista.faturamento}</p>
                            <p><strong>ROI:</strong> ${projecoes.realista.roi}</p>
                        </div>
                        
                        <div class="scenario-item otimista">
                            <h4>Cenário Otimista</h4>
                            <p><strong>Conversão:</strong> ${projecoes.otimista.conversao}</p>
                            <p><strong>Faturamento:</strong> ${projecoes.otimista.faturamento}</p>
                            <p><strong>ROI:</strong> ${projecoes.otimista.roi}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generatePlanoAcaoSection(plano) {
    return `
        <div class="neo-enhanced-card result-card full-width">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-tasks"></i>
                </div>
                <h3 class="neo-card-title">Plano de Ação</h3>
            </div>
            <div class="neo-card-content">
                <div class="plano-content">
                    <div class="action-timeline">
                        ${plano.map(item => `
                            <div class="action-item">
                                <div class="action-number">${item.passo}</div>
                                <div class="action-content">
                                    <h4>${item.acao}</h4>
                                    <p><strong>Prazo:</strong> ${item.prazo}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
}

function initializeResultsInteractions() {
    // Add any interactive functionality for results
    console.log('Results interactions initialized');
}

function downloadReport() {
    if (!currentAnalysis) {
        showNotification('Nenhuma análise disponível para download.', 'error');
        return;
    }
    
    // Create and download report
    const reportData = generateReportData(currentAnalysis);
    const blob = new Blob([reportData], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `analise-avatar-deepseek-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Relatório baixado com sucesso!', 'success');
}

function generateReportData(analysis) {
    return `
RELATÓRIO DE ANÁLISE DE AVATAR - DEEPSEEK AI
============================================

ESCOPO
------
Nicho Principal: ${analysis.escopo.nicho_principal}
Produto Ideal: ${analysis.escopo.produto_ideal}
Proposta de Valor: ${analysis.escopo.proposta_valor}

AVATAR DETALHADO
----------------
Demografia:
- Faixa Etária: ${analysis.avatar.demografia.faixa_etaria}
- Gênero: ${analysis.avatar.demografia.genero}
- Localização: ${analysis.avatar.demografia.localizacao}
- Renda: ${analysis.avatar.demografia.renda}
- Escolaridade: ${analysis.avatar.demografia.escolaridade}

Psicografia:
- Valores: ${analysis.avatar.psicografia.valores.join(', ')}
- Estilo de Vida: ${analysis.avatar.psicografia.estilo_vida}
- Aspirações: ${analysis.avatar.psicografia.aspiracoes.join(', ')}
- Medos: ${analysis.avatar.psicografia.medos.join(', ')}

ANÁLISE DE MERCADO
------------------
TAM: ${analysis.mercado.tam}
SAM: ${analysis.mercado.sam}
SOM: ${analysis.mercado.som}
Volume de Busca: ${analysis.mercado.volume_busca}

PROJEÇÕES
---------
Cenário Realista:
- Conversão: ${analysis.projecoes.realista.conversao}
- Faturamento: ${analysis.projecoes.realista.faturamento}
- ROI: ${analysis.projecoes.realista.roi}

PLANO DE AÇÃO
-------------
${analysis.plano_acao.map(item => `${item.passo}. ${item.acao} (${item.prazo})`).join('\n')}

Gerado em: ${new Date().toLocaleString()}
Powered by DeepSeek AI
    `;
}

function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'Análise de Avatar com DeepSeek AI - UP Lançamentos',
            text: 'Confira minha análise ultra-detalhada de avatar!',
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Link copiado para a área de transferência!', 'success');
        });
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: var(--neo-border-radius);
        color: var(--text-light);
        font-weight: 600;
        z-index: 10000;
        box-shadow: var(--neo-shadow-2);
        transition: var(--neo-transition);
        transform: translateX(100%);
        max-width: 400px;
    `;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            break;
        case 'error':
            notification.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
            break;
        default:
            notification.style.background = 'var(--brand-gradient)';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('.neo-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            if (query.length > 2) {
                searchNichos(query);
            }
        });
    }
}

async function searchNichos(query) {
    try {
        const response = await fetch(`/api/nichos?search=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        // Display search suggestions
        displaySearchSuggestions(data.nichos);
        
    } catch (error) {
        console.error('Erro na busca:', error);
    }
}

function displaySearchSuggestions(nichos) {
    // Implementation for search suggestions dropdown
    console.log('Nichos encontrados:', nichos);
}