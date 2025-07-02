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
        { progress: 95, text: 'Finalizando análise completa...' },
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
    }, 2000);
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
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentAnalysis = result;
        
        // Wait for progress simulation to complete
        setTimeout(() => {
            hideLoading();
            displayResults(result);
            analysisInProgress = false;
        }, 16000); // 16 seconds total for progress simulation
        
    } catch (error) {
        console.error('Erro na análise:', error);
        hideLoading();
        showNotification('Erro ao realizar análise. Verifique sua conexão e tente novamente.', 'error');
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
                    <h3 class="neo-card-title">Análise Completa Finalizada</h3>
                </div>
                <div class="neo-card-content">
                    <p>Sua análise ultra-detalhada foi processada pela IA DeepSeek. Esta é uma análise completa baseada em frameworks científicos de psicologia do consumidor e neurociência aplicada ao marketing.</p>
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
            ${generateDoresDesejos(analysis.dores_desejos)}
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
    if (!escopo) return '';
    
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
                            ${escopo.subnichos?.map(sub => `<li>${sub}</li>`).join('') || '<li>Não especificado</li>'}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Produto Ideal:</strong>
                        <p>${escopo.produto_ideal}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Proposta de Valor Única:</strong>
                        <p>${escopo.proposta_valor}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateAvatarSection(avatar) {
    if (!avatar) return '';
    
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-user-circle"></i>
                </div>
                <h3 class="neo-card-title">Análise Completa do Avatar</h3>
            </div>
            <div class="neo-card-content">
                <div class="avatar-tabs">
                    <button class="tab-btn active" onclick="showAvatarTab('demografia')">Demografia</button>
                    <button class="tab-btn" onclick="showAvatarTab('psicografia')">Psicografia</button>
                    <button class="tab-btn" onclick="showAvatarTab('comportamento')">Comportamento Digital</button>
                </div>
                
                <div class="avatar-content">
                    <div id="demografia-content" class="tab-content active">
                        <h4>Perfil Demográfico</h4>
                        <div class="avatar-details">
                            <div class="detail-item">
                                <strong>Faixa Etária:</strong>
                                <p>${avatar.demografia?.faixa_etaria || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Gênero:</strong>
                                <p>${avatar.demografia?.genero || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Localização:</strong>
                                <p>${avatar.demografia?.localizacao || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Renda:</strong>
                                <p>${avatar.demografia?.renda || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Escolaridade:</strong>
                                <p>${avatar.demografia?.escolaridade || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Profissões Principais:</strong>
                                <ul>
                                    ${avatar.demografia?.profissoes?.map(prof => `<li>${prof}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div id="psicografia-content" class="tab-content">
                        <h4>Perfil Psicográfico</h4>
                        <div class="avatar-details">
                            <div class="detail-item">
                                <strong>Valores Principais:</strong>
                                <ul>
                                    ${avatar.psicografia?.valores?.map(valor => `<li>${valor}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="detail-item">
                                <strong>Estilo de Vida:</strong>
                                <p>${avatar.psicografia?.estilo_vida || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Aspirações:</strong>
                                <ul>
                                    ${avatar.psicografia?.aspiracoes?.map(asp => `<li>${asp}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="detail-item">
                                <strong>Medos Principais:</strong>
                                <ul>
                                    ${avatar.psicografia?.medos?.map(medo => `<li>${medo}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="detail-item">
                                <strong>Frustrações:</strong>
                                <ul>
                                    ${avatar.psicografia?.frustracoes?.map(frust => `<li>${frust}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div id="comportamento-content" class="tab-content">
                        <h4>Comportamento Digital</h4>
                        <div class="avatar-details">
                            <div class="detail-item">
                                <strong>Plataformas Principais:</strong>
                                <ul>
                                    ${avatar.comportamento_digital?.plataformas?.map(plat => `<li>${plat}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="detail-item">
                                <strong>Horários de Pico:</strong>
                                <p>${avatar.comportamento_digital?.horarios_pico || 'Não especificado'}</p>
                            </div>
                            <div class="detail-item">
                                <strong>Conteúdo Preferido:</strong>
                                <ul>
                                    ${avatar.comportamento_digital?.conteudo_preferido?.map(cont => `<li>${cont}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="detail-item">
                                <strong>Influenciadores que Seguem:</strong>
                                <ul>
                                    ${avatar.comportamento_digital?.influenciadores?.map(inf => `<li>${inf}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateDoresDesejos(dores_desejos) {
    if (!dores_desejos) return '';
    
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
                        <strong>Principais Dores Identificadas:</strong>
                        <div class="dores-list">
                            ${dores_desejos.principais_dores?.map((dor, index) => `
                                <div class="dor-item">
                                    <h5>Dor ${index + 1}: ${dor.descricao}</h5>
                                    <p><strong>Impacto:</strong> ${dor.impacto}</p>
                                    <p><strong>Urgência:</strong> <span class="urgencia ${dor.urgencia?.toLowerCase()}">${dor.urgencia}</span></p>
                                </div>
                            `).join('') || '<p>Não especificado</p>'}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Estado Atual:</strong>
                        <p>${dores_desejos.estado_atual || 'Não especificado'}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Estado Desejado:</strong>
                        <p>${dores_desejos.estado_desejado || 'Não especificado'}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Obstáculos Percebidos:</strong>
                        <ul>
                            ${dores_desejos.obstaculos?.map(obs => `<li>${obs}</li>`).join('') || '<li>Não especificado</li>'}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Sonho Secreto:</strong>
                        <p class="sonho-secreto">${dores_desejos.sonho_secreto || 'Não especificado'}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateConcorrenciaSection(concorrencia) {
    if (!concorrencia) return '';
    
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
                        <div class="concorrentes-list">
                            ${concorrencia.diretos?.map(conc => `
                                <div class="concorrente-item">
                                    <h5>${conc.nome}</h5>
                                    <p><strong>Preço:</strong> ${conc.preco}</p>
                                    <p><strong>USP:</strong> ${conc.usp}</p>
                                    <p><strong>Forças:</strong> ${Array.isArray(conc.forcas) ? conc.forcas.join(', ') : conc.forcas}</p>
                                    <p><strong>Fraquezas:</strong> ${Array.isArray(conc.fraquezas) ? conc.fraquezas.join(', ') : conc.fraquezas}</p>
                                </div>
                            `).join('') || '<p>Não especificado</p>'}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Concorrentes Indiretos:</strong>
                        <div class="indiretos-list">
                            ${concorrencia.indiretos?.map(ind => `
                                <div class="indireto-item">
                                    <h5>${ind.nome}</h5>
                                    <p><strong>Tipo:</strong> ${ind.tipo}</p>
                                </div>
                            `).join('') || '<p>Não especificado</p>'}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Gaps de Mercado Identificados:</strong>
                        <ul>
                            ${concorrencia.gaps_mercado?.map(gap => `<li>${gap}</li>`).join('') || '<li>Não especificado</li>'}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateMercadoSection(mercado) {
    if (!mercado) return '';
    
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
                    <div class="tam-sam-som">
                        <div class="metric-item">
                            <div class="metric-value">${mercado.tam || 'N/A'}</div>
                            <div class="metric-label">TAM (Total Addressable Market)</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">${mercado.sam || 'N/A'}</div>
                            <div class="metric-label">SAM (Serviceable Addressable Market)</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">${mercado.som || 'N/A'}</div>
                            <div class="metric-label">SOM (Serviceable Obtainable Market)</div>
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Volume de Busca Mensal:</strong>
                        <p>${mercado.volume_busca || 'Não especificado'}</p>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Tendências em Alta:</strong>
                        <ul>
                            ${mercado.tendencias_alta?.map(tend => `<li class="trend-up">${tend}</li>`).join('') || '<li>Não especificado</li>'}
                        </ul>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Tendências em Baixa:</strong>
                        <ul>
                            ${mercado.tendencias_baixa?.map(tend => `<li class="trend-down">${tend}</li>`).join('') || '<li>Não especificado</li>'}
                        </ul>
                    </div>
                    
                    <div class="sazonalidade">
                        <div class="detail-item">
                            <strong>Melhores Meses:</strong>
                            <p class="meses-bons">${mercado.sazonalidade?.melhores_meses?.join(', ') || 'Não especificado'}</p>
                        </div>
                        <div class="detail-item">
                            <strong>Piores Meses:</strong>
                            <p class="meses-ruins">${mercado.sazonalidade?.piores_meses?.join(', ') || 'Não especificado'}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generatePalavrasChaveSection(palavras_chave) {
    if (!palavras_chave) return '';
    
    return `
        <div class="neo-enhanced-card result-card">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-search"></i>
                </div>
                <h3 class="neo-card-title">Análise de Palavras-Chave</h3>
            </div>
            <div class="neo-card-content">
                <div class="keywords-content">
                    <div class="detail-item">
                        <strong>Principais Palavras-Chave:</strong>
                        <div class="keywords-list">
                            ${palavras_chave.principais?.map(kw => `
                                <div class="keyword-item">
                                    <h5>${kw.termo}</h5>
                                    <div class="keyword-metrics">
                                        <span>Volume: ${kw.volume}</span>
                                        <span>CPC: ${kw.cpc}</span>
                                        <span>Dificuldade: ${kw.dificuldade}</span>
                                        <span>Intenção: ${kw.intencao}</span>
                                    </div>
                                </div>
                            `).join('') || '<p>Não especificado</p>'}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Custos por Plataforma:</strong>
                        <div class="platform-costs">
                            ${Object.entries(palavras_chave.custos_plataforma || {}).map(([platform, costs]) => `
                                <div class="platform-item">
                                    <h5>${platform.charAt(0).toUpperCase() + platform.slice(1)}</h5>
                                    <div class="cost-metrics">
                                        <span>CPM: ${costs.cpm}</span>
                                        <span>CPC: ${costs.cpc}</span>
                                        <span>CPL: ${costs.cpl}</span>
                                        <span>Conversão: ${costs.conversao}</span>
                                    </div>
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
    if (!metricas) return '';
    
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
                            <div class="metric-value">${metricas.cac_medio || 'N/A'}</div>
                            <div class="metric-label">CAC Médio</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">${metricas.ltv_medio || 'N/A'}</div>
                            <div class="metric-label">LTV Médio</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">${metricas.ltv_cac_ratio || 'N/A'}</div>
                            <div class="metric-label">LTV:CAC Ratio</div>
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Funil de Conversão:</strong>
                        <div class="funil-steps">
                            ${metricas.funil_conversao?.map((step, index) => `
                                <div class="funil-step">
                                    <span class="step-number">${index + 1}</span>
                                    <span class="step-text">${step}</span>
                                </div>
                            `).join('') || '<p>Não especificado</p>'}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>ROI por Canal:</strong>
                        <div class="roi-channels">
                            ${Object.entries(metricas.roi_canais || {}).map(([channel, roi]) => `
                                <div class="roi-item">
                                    <span class="channel-name">${channel.charAt(0).toUpperCase() + channel.slice(1)}</span>
                                    <span class="roi-value">${roi}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateVozMercadoSection(voz_mercado) {
    if (!voz_mercado) return '';
    
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
                        <strong>Principais Objeções e Como Contorná-las:</strong>
                        <div class="objecoes-list">
                            ${voz_mercado.objecoes?.map((obj, index) => `
                                <div class="objecao-item">
                                    <h5>Objeção ${index + 1}: ${obj.objecao}</h5>
                                    <p><strong>Como contornar:</strong> ${obj.contorno}</p>
                                </div>
                            `).join('') || '<p>Não especificado</p>'}
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Linguagem do Mercado:</strong>
                        <div class="linguagem-grid">
                            <div class="linguagem-item">
                                <h5>Termos Técnicos:</h5>
                                <ul>
                                    ${voz_mercado.linguagem?.termos?.map(termo => `<li>${termo}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="linguagem-item">
                                <h5>Gírias e Expressões:</h5>
                                <ul>
                                    ${voz_mercado.linguagem?.girias?.map(giria => `<li>${giria}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                            <div class="linguagem-item">
                                <h5>Gatilhos Emocionais:</h5>
                                <ul>
                                    ${voz_mercado.linguagem?.gatilhos?.map(gatilho => `<li>${gatilho}</li>`).join('') || '<li>Não especificado</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="detail-item">
                        <strong>Crenças Limitantes Comuns:</strong>
                        <ul>
                            ${voz_mercado.crencas_limitantes?.map(crenca => `<li>${crenca}</li>`).join('') || '<li>Não especificado</li>'}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generateProjecoesSection(projecoes) {
    if (!projecoes) return '';
    
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
                    <div class="cenarios-grid">
                        <div class="cenario-item conservador">
                            <h4>Cenário Conservador</h4>
                            <div class="cenario-metrics">
                                <div class="metric">
                                    <span class="label">Conversão:</span>
                                    <span class="value">${projecoes.conservador?.conversao || 'N/A'}</span>
                                </div>
                                <div class="metric">
                                    <span class="label">Faturamento:</span>
                                    <span class="value">${projecoes.conservador?.faturamento || 'N/A'}</span>
                                </div>
                                <div class="metric">
                                    <span class="label">ROI:</span>
                                    <span class="value">${projecoes.conservador?.roi || 'N/A'}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="cenario-item realista">
                            <h4>Cenário Realista</h4>
                            <div class="cenario-metrics">
                                <div class="metric">
                                    <span class="label">Conversão:</span>
                                    <span class="value">${projecoes.realista?.conversao || 'N/A'}</span>
                                </div>
                                <div class="metric">
                                    <span class="label">Faturamento:</span>
                                    <span class="value">${projecoes.realista?.faturamento || 'N/A'}</span>
                                </div>
                                <div class="metric">
                                    <span class="label">ROI:</span>
                                    <span class="value">${projecoes.realista?.roi || 'N/A'}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="cenario-item otimista">
                            <h4>Cenário Otimista</h4>
                            <div class="cenario-metrics">
                                <div class="metric">
                                    <span class="label">Conversão:</span>
                                    <span class="value">${projecoes.otimista?.conversao || 'N/A'}</span>
                                </div>
                                <div class="metric">
                                    <span class="label">Faturamento:</span>
                                    <span class="value">${projecoes.otimista?.faturamento || 'N/A'}</span>
                                </div>
                                <div class="metric">
                                    <span class="label">ROI:</span>
                                    <span class="value">${projecoes.otimista?.roi || 'N/A'}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function generatePlanoAcaoSection(plano_acao) {
    if (!plano_acao) return '';
    
    return `
        <div class="neo-enhanced-card result-card full-width">
            <div class="neo-card-header">
                <div class="neo-card-icon">
                    <i class="fas fa-tasks"></i>
                </div>
                <h3 class="neo-card-title">Plano de Ação Estratégico</h3>
            </div>
            <div class="neo-card-content">
                <div class="plano-content">
                    <div class="acoes-timeline">
                        ${plano_acao.map(acao => `
                            <div class="acao-item">
                                <div class="acao-number">${acao.passo}</div>
                                <div class="acao-content">
                                    <h4>${acao.acao}</h4>
                                    <p class="acao-prazo"><strong>Prazo:</strong> ${acao.prazo}</p>
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
    // Initialize tab functionality for avatar section
    window.showAvatarTab = function(tabName) {
        // Hide all avatar tab contents
        const avatarTabContents = document.querySelectorAll('.avatar-content .tab-content');
        avatarTabContents.forEach(content => content.classList.remove('active'));
        
        // Remove active class from all avatar tab buttons
        const avatarTabButtons = document.querySelectorAll('.avatar-tabs .tab-btn');
        avatarTabButtons.forEach(btn => btn.classList.remove('active'));
        
        // Show target content and activate button
        const targetContent = document.getElementById(`${tabName}-content`);
        if (targetContent) {
            targetContent.classList.add('active');
        }
        
        // Find and activate the corresponding button
        const targetButton = Array.from(avatarTabButtons).find(btn => 
            btn.textContent.toLowerCase().includes(tabName.toLowerCase())
        );
        if (targetButton) {
            targetButton.classList.add('active');
        }
    };
}

function downloadReport() {
    if (!currentAnalysis) {
        showNotification('Nenhuma análise disponível para download.', 'error');
        return;
    }
    
    // Create comprehensive report
    const reportData = generateComprehensiveReport(currentAnalysis);
    const blob = new Blob([reportData], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `analise-completa-avatar-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Relatório completo baixado com sucesso!', 'success');
}

function generateComprehensiveReport(analysis) {
    return `
RELATÓRIO COMPLETO DE ANÁLISE DE AVATAR
=======================================
Gerado em: ${new Date().toLocaleString()}
Powered by DeepSeek AI

🎯 DEFINIÇÃO DO ESCOPO
=====================
Nicho Principal: ${analysis.escopo?.nicho_principal || 'N/A'}
Subnichos: ${analysis.escopo?.subnichos?.join(', ') || 'N/A'}
Produto Ideal: ${analysis.escopo?.produto_ideal || 'N/A'}
Proposta de Valor: ${analysis.escopo?.proposta_valor || 'N/A'}

👥 ANÁLISE DO AVATAR
===================

DEMOGRAFIA:
- Faixa Etária: ${analysis.avatar?.demografia?.faixa_etaria || 'N/A'}
- Gênero: ${analysis.avatar?.demografia?.genero || 'N/A'}
- Localização: ${analysis.avatar?.demografia?.localizacao || 'N/A'}
- Renda: ${analysis.avatar?.demografia?.renda || 'N/A'}
- Escolaridade: ${analysis.avatar?.demografia?.escolaridade || 'N/A'}
- Profissões: ${analysis.avatar?.demografia?.profissoes?.join(', ') || 'N/A'}

PSICOGRAFIA:
- Valores: ${analysis.avatar?.psicografia?.valores?.join(', ') || 'N/A'}
- Estilo de Vida: ${analysis.avatar?.psicografia?.estilo_vida || 'N/A'}
- Aspirações: ${analysis.avatar?.psicografia?.aspiracoes?.join(', ') || 'N/A'}
- Medos: ${analysis.avatar?.psicografia?.medos?.join(', ') || 'N/A'}
- Frustrações: ${analysis.avatar?.psicografia?.frustracoes?.join(', ') || 'N/A'}

COMPORTAMENTO DIGITAL:
- Plataformas: ${analysis.avatar?.comportamento_digital?.plataformas?.join(', ') || 'N/A'}
- Horários de Pico: ${analysis.avatar?.comportamento_digital?.horarios_pico || 'N/A'}
- Conteúdo Preferido: ${analysis.avatar?.comportamento_digital?.conteudo_preferido?.join(', ') || 'N/A'}

💔 DORES E DESEJOS
=================
Estado Atual: ${analysis.dores_desejos?.estado_atual || 'N/A'}
Estado Desejado: ${analysis.dores_desejos?.estado_desejado || 'N/A'}
Sonho Secreto: ${analysis.dores_desejos?.sonho_secreto || 'N/A'}

💰 ANÁLISE DE MERCADO
====================
TAM: ${analysis.mercado?.tam || 'N/A'}
SAM: ${analysis.mercado?.sam || 'N/A'}
SOM: ${analysis.mercado?.som || 'N/A'}
Volume de Busca: ${analysis.mercado?.volume_busca || 'N/A'}

📊 MÉTRICAS DE PERFORMANCE
=========================
CAC Médio: ${analysis.metricas?.cac_medio || 'N/A'}
LTV Médio: ${analysis.metricas?.ltv_medio || 'N/A'}
LTV:CAC Ratio: ${analysis.metricas?.ltv_cac_ratio || 'N/A'}

📈 PROJEÇÕES
============
CONSERVADOR:
- Conversão: ${analysis.projecoes?.conservador?.conversao || 'N/A'}
- Faturamento: ${analysis.projecoes?.conservador?.faturamento || 'N/A'}
- ROI: ${analysis.projecoes?.conservador?.roi || 'N/A'}

REALISTA:
- Conversão: ${analysis.projecoes?.realista?.conversao || 'N/A'}
- Faturamento: ${analysis.projecoes?.realista?.faturamento || 'N/A'}
- ROI: ${analysis.projecoes?.realista?.roi || 'N/A'}

OTIMISTA:
- Conversão: ${analysis.projecoes?.otimista?.conversao || 'N/A'}
- Faturamento: ${analysis.projecoes?.otimista?.faturamento || 'N/A'}
- ROI: ${analysis.projecoes?.otimista?.roi || 'N/A'}

💡 PLANO DE AÇÃO
===============
${analysis.plano_acao?.map(acao => `${acao.passo}. ${acao.acao} (${acao.prazo})`).join('\n') || 'N/A'}

---
Relatório gerado pela plataforma UP Lançamentos
Análise powered by DeepSeek AI
    `;
}

function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'Análise Completa de Avatar - UP Lançamentos',
            text: 'Confira minha análise ultra-detalhada de mercado!',
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
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Additional CSS for new components
const additionalCSS = `
.results-header {
    margin-bottom: 2rem;
}

.results-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
}

.result-card.full-width {
    grid-column: 1 / -1;
}

.detail-item {
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: var(--neo-bg-dark);
    border-radius: var(--neo-border-radius-small);
}

.detail-item strong {
    color: var(--brand-primary);
    display: block;
    margin-bottom: 0.5rem;
}

.detail-item ul {
    margin-left: 1rem;
    color: var(--text-secondary);
}

.avatar-tabs {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    background: var(--neo-bg-dark);
    padding: 0.5rem;
    border-radius: var(--neo-border-radius);
}

.tab-btn {
    flex: 1;
    padding: 0.8rem 1rem;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    border-radius: var(--neo-border-radius-small);
    cursor: pointer;
    transition: var(--neo-transition);
    font-weight: 600;
}

.tab-btn.active,
.tab-btn:hover {
    background: var(--brand-gradient);
    color: var(--text-light);
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.dores-list .dor-item {
    margin-bottom: 1rem;
    padding: 1rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
    border-left: 4px solid var(--brand-primary);
}

.urgencia {
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
}

.urgencia.alta {
    background: #ef4444;
    color: white;
}

.urgencia.média {
    background: #f59e0b;
    color: white;
}

.urgencia.baixa {
    background: #10b981;
    color: white;
}

.sonho-secreto {
    font-style: italic;
    color: var(--brand-primary);
    font-weight: 600;
}

.concorrente-item, .indireto-item {
    margin-bottom: 1rem;
    padding: 1rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.tam-sam-som {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}

.metric-item {
    text-align: center;
    padding: 1.5rem;
    background: var(--neo-bg-dark);
    border-radius: var(--neo-border-radius-small);
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--brand-primary);
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.trend-up {
    color: #10b981;
}

.trend-down {
    color: #ef4444;
}

.meses-bons {
    color: #10b981;
    font-weight: 600;
}

.meses-ruins {
    color: #ef4444;
    font-weight: 600;
}

.keyword-item {
    margin-bottom: 1rem;
    padding: 1rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.keyword-metrics {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
}

.keyword-metrics span {
    background: var(--neo-bg-dark);
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

.platform-costs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.platform-item {
    padding: 1rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.cost-metrics {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.cost-metrics span {
    background: var(--neo-bg-dark);
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.funil-steps {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.funil-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.step-number {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: var(--brand-gradient);
    color: var(--text-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    flex-shrink: 0;
}

.roi-channels {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
}

.roi-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.roi-value {
    font-weight: 700;
    color: var(--brand-primary);
}

.objecao-item {
    margin-bottom: 1rem;
    padding: 1rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
    border-left: 4px solid var(--brand-secondary);
}

.linguagem-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.linguagem-item {
    padding: 1rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.cenarios-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.cenario-item {
    padding: 1.5rem;
    border-radius: var(--neo-border-radius);
    position: relative;
    overflow: hidden;
}

.cenario-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}

.cenario-item.conservador {
    background: var(--neo-bg-dark);
}

.cenario-item.conservador::before {
    background: #ef4444;
}

.cenario-item.realista {
    background: var(--neo-bg-dark);
}

.cenario-item.realista::before {
    background: #f59e0b;
}

.cenario-item.otimista {
    background: var(--neo-bg-dark);
}

.cenario-item.otimista::before {
    background: #10b981;
}

.cenario-metrics {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    margin-top: 1rem;
}

.cenario-metrics .metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    background: var(--neo-bg);
    border-radius: var(--neo-border-radius-small);
}

.cenario-metrics .value {
    font-weight: 700;
    color: var(--brand-primary);
}

.acoes-timeline {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.acao-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.acao-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--brand-gradient);
    color: var(--text-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    flex-shrink: 0;
}

.acao-content {
    flex: 1;
    background: var(--neo-bg-dark);
    padding: 1rem;
    border-radius: var(--neo-border-radius-small);
}

.acao-prazo {
    margin-top: 0.5rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

@media (max-width: 768px) {
    .results-grid {
        grid-template-columns: 1fr;
    }
    
    .results-actions {
        flex-direction: column;
    }
    
    .tam-sam-som {
        grid-template-columns: 1fr;
    }
    
    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .cenarios-grid {
        grid-template-columns: 1fr;
    }
    
    .platform-costs {
        grid-template-columns: 1fr;
    }
    
    .linguagem-grid {
        grid-template-columns: 1fr;
    }
}
`;

// Inject additional CSS
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);