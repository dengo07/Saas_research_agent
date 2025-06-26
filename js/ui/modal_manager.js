import { elements } from './dom_elements.js';

export class ModalManager {
    static open(title) {
        elements.modalTitle.textContent = `Research-Backed Plan: ${title}`;
        elements.modalBody.innerHTML = '';
        elements.modalBody.appendChild(elements.modalLoader);
        elements.modalLoader.classList.remove('hidden');
        elements.modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    static close() {
        elements.modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }

    // --- YENİ GRAFİK OLUŞTURMA FONKSİYONLARI ---

    /**
     * Plan Güvenilirliğini gösteren bir donut grafiği oluşturur.
     * @param {number} confidenceScore - 0 ile 100 arasında bir güven skoru.
     */
    static renderConfidenceChart(confidenceScore = 90) {
    try {
        const canvas = document.getElementById('confidenceChart');
        if (!canvas) {
            console.warn('Confidence chart canvas not found');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.warn('Could not get 2D context for confidence chart');
            return;
        }

        // Önceki chart'ı temizle
        if (canvas.chart) {
            canvas.chart.destroy();
        }

        const gradient = ctx.createLinearGradient(0, 0, 0, 200);
        gradient.addColorStop(0, '#4ade80');
        gradient.addColorStop(1, '#22c55e');

        canvas.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Confidence', 'Remaining'],
                datasets: [{
                    data: [Math.max(0, Math.min(100, confidenceScore)), 100 - Math.max(0, Math.min(100, confidenceScore))],
                    backgroundColor: [gradient, '#374151'],
                    borderColor: '#1f2937',
                    borderWidth: 4,
                    cutout: '75%',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                animation: {
                    animateRotate: true,
                    duration: 2000
                }
            }
        });
    } catch (error) {
        console.error('Error creating confidence chart:', error);
    }
}

static renderCompetitiveRadarChart(competitiveData) {
    try {
        const canvas = document.getElementById('competitiveRadarChart');
        if (!canvas) {
            console.warn('Competitive radar chart canvas not found');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.warn('Could not get 2D context for competitive radar chart');
            return;
        }

        // Önceki chart'ı temizle
        if (canvas.chart) {
            canvas.chart.destroy();
        }

        // Default data validation
        const data = competitiveData || {
            labels: ['Price', 'Features', 'Quality', 'Marketing', 'Innovation'],
            yourBusiness: [85, 90, 75, 70, 95],
            competitorAvg: [70, 75, 80, 85, 70],
        };

        // Data validation
        if (!data.labels || !Array.isArray(data.labels) || data.labels.length === 0) {
            console.warn('Invalid labels for competitive radar chart');
            return;
        }

        canvas.chart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Your Business',
                        data: Array.isArray(data.yourBusiness) ? data.yourBusiness : [85, 90, 75, 70, 95],
                        fill: true,
                        backgroundColor: 'rgba(79, 70, 229, 0.3)',
                        borderColor: 'rgba(79, 70, 229, 1)',
                        pointBackgroundColor: 'rgba(79, 70, 229, 1)',
                        pointBorderColor: '#fff',
                        pointRadius: 6,
                        pointHoverRadius: 8,
                    },
                    {
                        label: 'Competitor Average',
                        data: Array.isArray(data.competitorAvg) ? data.competitorAvg : [70, 75, 80, 85, 70],
                        fill: true,
                        backgroundColor: 'rgba(107, 114, 128, 0.3)',
                        borderColor: 'rgba(107, 114, 128, 1)',
                        pointBackgroundColor: 'rgba(107, 114, 128, 1)',
                        pointBorderColor: '#fff',
                        pointRadius: 6,
                        pointHoverRadius: 8,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(255, 255, 255, 0.2)' },
                        grid: { color: 'rgba(255, 255, 255, 0.2)' },
                        pointLabels: {
                            color: '#cbd5e1',
                            font: { size: 12 }
                        },
                        ticks: {
                            color: '#94a3b8',
                            backdropColor: 'transparent',
                            stepSize: 20,
                            min: 0,
                            max: 100
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#cbd5e1' }
                    }
                },
                animation: {
                    duration: 2000
                }
            }
        });
    } catch (error) {
        console.error('Error creating competitive radar chart:', error);
    }
}

    /**
     * Gelir projeksiyonu için line chart oluşturur
     */
    static renderRevenueProjectionChart(revenueData) {
    try {
        const canvas = document.getElementById('revenueChart');
        if (!canvas) {
            console.warn('Revenue chart canvas not found');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.warn('Could not get 2D context for revenue chart');
            return;
        }

        // Önceki chart'ı temizle
        if (canvas.chart) {
            canvas.chart.destroy();
        }

        // Default data
        const defaultData = {
            labels: ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'],
            revenue: [50000, 120000, 250000, 450000, 700000]
        };

        const data = {
            labels: (revenueData && revenueData.labels) ? revenueData.labels : defaultData.labels,
            revenue: (revenueData && revenueData.revenue) ? revenueData.revenue : defaultData.revenue
        };

        // Veri doğrulama
        if (!Array.isArray(data.revenue) || data.revenue.length === 0) {
            console.warn('Invalid revenue data');
            return;
        }

        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(34, 197, 94, 0.3)');
        gradient.addColorStop(1, 'rgba(34, 197, 94, 0.05)');

        canvas.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Projected Revenue',
                    data: data.revenue,
                    borderColor: '#22c55e',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#22c55e',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: {
                            color: '#94a3b8',
                            callback: function(value) {
                                if (value >= 1000000) {
                                    return '$' + (value / 1000000).toFixed(1) + 'M';
                                } else if (value >= 1000) {
                                    return '$' + (value / 1000).toFixed(0) + 'K';
                                }
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    }
                },
                animation: {
                    duration: 3000,
                    easing: 'easeInOutQuart'
                }
            }
        });
        
        console.log('✅ Revenue chart created successfully');
    } catch (error) {
        console.error('❌ Error creating revenue chart:', error);
    }
}

    /**
     * Market büyüklüğü için bar chart oluşturur
     */
    static renderMarketSizeChart(marketData) {
    try {
        const canvas = document.getElementById('marketSizeChart');
        if (!canvas) {
            console.warn('Market size chart canvas not found');
            return;
        }
        
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.warn('Could not get 2D context for market size chart');
            return;
        }

        // Önceki chart'ı temizle
        if (canvas.chart) {
            canvas.chart.destroy();
        }

        // Default data ve colors oluştur
        const defaultData = {
            labels: ['TAM (Total Addressable)', 'SAM (Serviceable Addressable)', 'SOM (Serviceable Obtainable)'],
            values: [1000000000, 100000000, 10000000],
            colors: ['#8b5cf6', '#a855f7', '#c084fc']
        };

        // marketData'dan gelen verileri kullan, eksikse default kullan
        const data = {
            labels: (marketData && marketData.labels) ? marketData.labels : defaultData.labels,
            values: (marketData && marketData.values) ? marketData.values : defaultData.values,
            colors: (marketData && marketData.colors) ? marketData.colors : defaultData.colors
        };

        // Veri doğrulama
        if (!Array.isArray(data.values) || data.values.length === 0) {
            console.warn('Invalid market data values');
            return;
        }

        canvas.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: data.colors,
                    borderColor: data.colors.map(color => color + '80'), // Transparanlık ekle
                    borderWidth: 2,
                    borderRadius: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: {
                            color: '#94a3b8',
                            callback: function(value) {
                                if (value >= 1000000000) {
                                    return '$' + (value / 1000000000).toFixed(1) + 'B';
                                } else if (value >= 1000000) {
                                    return '$' + (value / 1000000).toFixed(0) + 'M';
                                } else if (value >= 1000) {
                                    return '$' + (value / 1000).toFixed(0) + 'K';
                                }
                                return '$' + value;
                            }
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                },
                animation: {
                    duration: 2500,
                    delay: 500
                }
            }
        });
        
        console.log('✅ Market size chart created successfully');
    } catch (error) {
        console.error('❌ Error creating market size chart:', error);
    }
}

    /**
     * Animasyonlu progress bar oluşturur
     */
    static createProgressBar(percentage, label, color = 'bg-indigo-500') {
        return `
            <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-slate-300">${label}</span>
                    <span class="text-sm text-slate-400">${percentage}%</span>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2.5">
                    <div class="${color} h-2.5 rounded-full progress-bar-animate" 
                         style="width: 0%" data-width="${percentage}%"></div>
                </div>
            </div>
        `;
    }

    /**
     * Animasyonlu metric card oluşturur
     */
    static createMetricCard(title, displayValue, rawValue, icon, color = 'text-indigo-400', bgColor = 'bg-indigo-900/30') {
    // rawValue'dan sadece sayıları al
    const numericValue = String(rawValue).replace(/[^0-9.]/g, '');

    return `
        <div class="metric-card ${bgColor} p-4 rounded-lg border border-indigo-700/50 hover:border-indigo-600/50 transition-all duration-300 hover:scale-105">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-slate-400">${title}</p>
                    <p class="text-2xl font-bold ${color} metric-value" data-numeric-value="${numericValue}">${displayValue}</p>
                </div>
                <div class="text-3xl ${color}">${icon}</div>
            </div>
        </div>
    `;
}

    /**
     * Risk level indicator oluşturur
     */
    static createRiskIndicator(level) {
        const colors = {
            low: { bg: 'bg-green-900/30', border: 'border-green-700/50', text: 'text-green-400', dot: 'bg-green-400' },
            medium: { bg: 'bg-yellow-900/30', border: 'border-yellow-700/50', text: 'text-yellow-400', dot: 'bg-yellow-400' },
            high: { bg: 'bg-red-900/30', border: 'border-red-700/50', text: 'text-red-400', dot: 'bg-red-400' }
        };
        
        const color = colors[level] || colors.medium;
        
        return `
            <div class="flex items-center space-x-2">
                <div class="flex space-x-1">
                    <div class="w-2 h-2 rounded-full ${color.dot} animate-pulse"></div>
                    <div class="w-2 h-2 rounded-full ${color.dot} animate-pulse" style="animation-delay: 0.2s"></div>
                    <div class="w-2 h-2 rounded-full ${color.dot} animate-pulse" style="animation-delay: 0.4s"></div>
                </div>
                <span class="${color.text} font-medium capitalize">${level} Risk</span>
            </div>
        `;
    }

    // --- DISPLAYBUSINESSPLAN FONKSİYONUNUN GELİŞTİRİLMİŞ HALİ ---
    
static displayBusinessPlan(planData) {
    elements.modalLoader.classList.add('hidden');

    // CSS animasyonları için stil ekle
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        .fade-in { animation: fadeIn 0.8s ease-out; }
        .slide-up { animation: slideUp 0.6s ease-out; }
        .progress-bar-animate { transition: width 2s ease-out; }
        .metric-card { 
            animation: slideUp 0.6s ease-out; 
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        .pulse-glow { animation: pulseGlow 2s infinite; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.3); }
            50% { box-shadow: 0 0 30px rgba(79, 70, 229, 0.6); }
        }
    `;
    document.head.appendChild(styleSheet);

    // Helper fonksiyonlar
    const formatToList = (data) => {
    if (!data) return '<em class="text-slate-400">Not specified</em>';

    // 1. Dizi (Array) ise, liste yap (Bu kısım zaten doğruydu)
    if (Array.isArray(data)) {
        const items = data.filter(item => String(item).trim() !== '');
        if (items.length === 0) return '<em class="text-slate-400">Not specified</em>';
        return `<ul class="list-disc list-inside space-y-2">${items.map(item => `<li class="text-slate-300">${item}</li>`).join('')}</ul>`;
    }

    // 2. String ise, paragraf yap (Bu kısım da doğruydu)
    if (typeof data === 'string') {
        if (data.trim() === '') return '<em class="text-slate-400">Not specified</em>';
        return `<p class="text-slate-300 leading-relaxed">${data}</p>`;
    }
    
    // 3. YENİ EKLENEN KISIM: Genel bir obje ise
    if (typeof data === 'object' && data !== null) {
        const entries = Object.entries(data);
        if (entries.length === 0) return '<em class="text-slate-400">Not specified</em>';
        
        // Objenin anahtar-değer çiftlerini liste olarak formatla
        return `<ul class="space-y-3">
            ${entries.map(([key, value]) => `
                <li>
                    <strong class="font-semibold text-indigo-300">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong>
                    <div class="text-slate-300 pl-4">${formatToList(value)}</div> 
                </li>
            `).join('')}
        </ul>`;
    }

    // Diğer tüm durumlar için (pek olası değil)
    return String(data);
};

    // Özellikle formatFeatures fonksiyonu
    const formatFeatures = (data) => {
    // 1. Veri obje değilse veya boşsa, "Belirtilmemiş" döndür.
    if (!data || typeof data !== 'object' || Object.keys(data).length === 0) {
        return '<em class="text-slate-400">Not specified</em>';
    }

    // 2. Objenin anahtar-değer çiftlerini al ve her biri için bir kart oluştur.
    return `<div class="space-y-4">
        ${Object.entries(data).map(([key, feature], index) => {
            // 'feature' artık { name: "...", description: "..." } gibi bir obje olabilir
            // veya basit bir metin de olabilir. İki durumu da kontrol edelim.
            const featureName = typeof feature === 'object' ? feature.name : key;
            const featureDesc = typeof feature === 'object' ? feature.description : feature;
            const featureNumber = index + 1;

            return `<div class="bg-slate-800/30 p-4 rounded-lg border border-slate-700/30 hover:border-indigo-600/50 transition-all duration-300">
                <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0 w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        ${featureNumber}
                    </div>
                    <div class="flex-1">
                        <h5 class="font-semibold text-indigo-300 mb-1">${featureName || `Feature ${featureNumber}`}</h5>
                        <div class="text-slate-300 leading-relaxed">${featureDesc || 'No description provided.'}</div>
                    </div>
                </div>
            </div>`;
        }).join('')}
    </div>`;
};
    
    // MVP Yol Haritası için geliştirilmiş görsel formatlayıcı
    const formatRoadmap = (data) => {
        if (!data || !Array.isArray(data) || data.length === 0) {
            return '<em class="text-slate-400">Not specified</em>';
        }
        return `
            <div class="relative pl-8">
                <div class="absolute left-0 top-0 h-full w-1 bg-gradient-to-b from-indigo-500 to-purple-500 rounded-full"></div>
                <div class="space-y-8">
                    ${data.map((item, index) => `
                        <div class="relative slide-up" style="animation-delay: ${index * 0.2}s">
                            <div class="absolute -left-[35px] top-1 h-6 w-6 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 border-2 border-slate-900 flex items-center justify-center">
                                <div class="h-2 w-2 rounded-full bg-white"></div>
                            </div>
                            <div class="bg-slate-800/30 p-4 rounded-lg border border-slate-700/50 hover:border-indigo-600/50 transition-all duration-300">
                                <h5 class="font-semibold text-indigo-300 mb-2">${item.split(':')[0] || `Phase ${index + 1}`}</h5>
                                <p class="text-slate-300 text-sm">${item.split(':')[1]?.trim() || ''}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    };
    
    const getSafeNumber = (value, defaultValue = 0) => {
        const num = Number(value);
        return isNaN(num) ? defaultValue : num;
    };

    // Metric card helper fonksiyonu
    const createMetricCard = (title, value, icon, textColor = 'text-indigo-400', bgColor = 'bg-indigo-900/30') => {
        return `
            <div class="metric-card bg-slate-800/60 p-6 rounded-xl border border-slate-700/50 hover:border-indigo-600/70 transition-all duration-300 ${bgColor}">
                <div class="flex items-center justify-between mb-3">
                    <div class="text-2xl">${icon}</div>
                    <div class="text-xs text-slate-500 font-medium">${title}</div>
                </div>
                <div class="text-2xl font-bold ${textColor} mb-1">${value}</div>
                <div class="h-1 bg-slate-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full progress-bar-animate" style="width: 85%"></div>
                </div>
            </div>
        `;
    };

    // Progress bar helper fonksiyonu
    const createProgressBar = (percentage, label, colorClass) => {
        return `
            <div class="mb-4">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm text-slate-300">${label}</span>
                    <span class="text-sm font-semibold text-slate-200">${percentage}%</span>
                </div>
                <div class="w-full bg-slate-700 rounded-full h-2">
                    <div class="${colorClass} h-2 rounded-full progress-bar-animate" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    };

    // Risk indicator helper fonksiyonu
    const createRiskIndicator = (riskLevel) => {
        const riskColors = {
            low: { bg: 'bg-green-900/30', text: 'text-green-300', border: 'border-green-700/50' },
            medium: { bg: 'bg-yellow-900/30', text: 'text-yellow-300', border: 'border-yellow-700/50' },
            high: { bg: 'bg-red-900/30', text: 'text-red-300', border: 'border-red-700/50' }
        };
        
        const risk = riskColors[riskLevel] || riskColors.medium;
        
        return `
            <div class="mt-4 p-3 ${risk.bg} border ${risk.border} rounded-lg">
                <div class="flex items-center">
                    <div class="w-3 h-3 ${risk.bg} rounded-full mr-2"></div>
                    <span class="${risk.text} text-sm font-medium">Risk Level: ${riskLevel.toUpperCase()}</span>
                </div>
            </div>
        `;
    };

    const safeMarketSize = getSafeNumber(planData.marketSize, 100000000);
    const safeTargetRevenue = getSafeNumber(planData.targetRevenue, 1000000);
    const safeCompetitorCount = getSafeNumber(planData.competitorCount, 0);
    const safeMvpTimeframe = getSafeNumber(planData.mvpTimeframe, 6);

    const planHtml = `
        <div class="fade-in">
            <!-- Executive Summary Bölümü -->
            <div class="bg-gradient-to-r from-indigo-900/40 to-purple-900/40 p-6 rounded-xl mb-8 border border-indigo-700/50 pulse-glow">
                <h3 class="text-2xl font-bold text-indigo-300 mb-6 flex items-center">
                    <span class="mr-3">🔍</span>Executive Summary & Key Metrics
                </h3>
                
                <!-- Metric Cards - Düzeltilmiş -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                    ${createMetricCard(
                        'Market Size', 
                        '$' + Math.round(safeMarketSize / 1000000) + 'M', 
                        '📊'
                    )}
                    ${createMetricCard(
                        'Target Revenue', 
                        '$' + Math.round(safeTargetRevenue / 1000) + 'K', 
                        '💰', 
                        'text-green-400', 
                        'bg-green-900/30'
                    )}
                    ${createMetricCard(
                        'Competitors', 
                        safeCompetitorCount, 
                        '⚔️', 
                        'text-yellow-400', 
                        'bg-yellow-900/30'
                    )}
                    ${createMetricCard(
                        'Time to MVP', 
                        safeMvpTimeframe + ' months', 
                        '🚀', 
                        'text-purple-400', 
                        'bg-purple-900/30'
                    )}
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 space-y-6">
                        <div class="slide-up">
                            <h5 class="text-indigo-200 font-semibold mb-3 flex items-center">
                                <span class="mr-2">🎯</span>Market Opportunity
                            </h5>
                            <div class="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
                                <div class="text-slate-300 text-sm leading-relaxed">${formatToList(planData.marketOpportunity)}</div>
                            </div>
                        </div>
                        <div class="slide-up" style="animation-delay: 0.2s">
                            <h5 class="text-indigo-200 font-semibold mb-3 flex items-center">
                                <span class="mr-2">💡</span>Problem-Solution Fit
                            </h5>
                            <div class="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
                                <div class="text-slate-300 text-sm leading-relaxed">${formatToList(planData.painPointsAddressed)}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex flex-col items-center justify-center text-center slide-up" style="animation-delay: 0.4s">
                        <h5 class="text-indigo-200 font-semibold mb-4">Plan Confidence</h5>
                        <div class="relative w-36 h-36 mb-4">
                            <canvas id="confidenceChart"></canvas>
                            <div class="absolute inset-0 flex items-center justify-center text-4xl font-bold text-green-400">
                                ${planData.confidenceScore || 90}%
                            </div>
                        </div>
                        <p class="text-xs text-slate-400">Based on ${planData.competitorCount || 12}+ competitors analyzed</p>
                        ${createRiskIndicator(planData.riskLevel || 'medium')}
                    </div>
                </div>
            </div>

            <!-- Market Analysis Section -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 slide-up">
                    <h4 class="font-bold text-purple-300 mb-4 text-xl flex items-center">
                        <span class="mr-3">📈</span>Market Size Breakdown
                    </h4>
                    <div class="h-64 mb-4">
                        <canvas id="marketSizeChart"></canvas>
                    </div>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between"><span class="text-slate-400">TAM (Total Addressable):</span><span class="text-purple-300">$${((planData.marketData?.values?.[0] || 1000000000) / 1000000000).toFixed(1)}B</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">SAM (Serviceable Addressable):</span><span class="text-purple-400">$${((planData.marketData?.values?.[1] || 100000000) / 1000000).toFixed(0)}M</span></div>
                        <div class="flex justify-between"><span class="text-slate-400">SOM (Serviceable Obtainable):</span><span class="text-purple-500">$${((planData.marketData?.values?.[2] || 10000000) / 1000000).toFixed(0)}M</span></div>
                    </div>
                </div>
                
                <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 slide-up" style="animation-delay: 0.2s">
                    <h4 class="font-bold text-green-300 mb-4 text-xl flex items-center">
                        <span class="mr-3">💵</span>Revenue Projection
                    </h4>
                    <div class="h-64">
                        <canvas id="revenueChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Target Audience & Competitive Advantage -->
            <div class="space-y-8">
                <div class="bg-gradient-to-r from-slate-800/50 to-slate-700/50 p-6 rounded-xl border border-slate-700/50 slide-up">
                    <h4 class="font-bold text-indigo-300 mb-6 text-xl flex items-center">
                        <span class="mr-3">🎯</span>Target Audience Analysis
                    </h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h5 class="text-indigo-200 font-semibold mb-3">Primary Segments</h5>
                            <div class="text-slate-300 leading-relaxed">${formatToList(planData.targetAudience)}</div>
                        </div>
                        <div>
                            <h5 class="text-indigo-200 font-semibold mb-4">Market Penetration Goals</h5>
                            ${createProgressBar(15, 'Year 1 Target', 'bg-indigo-500')}
                            ${createProgressBar(35, 'Year 2 Target', 'bg-indigo-600')}
                            ${createProgressBar(60, 'Year 3 Target', 'bg-indigo-700')}
                        </div>
                    </div>
                </div>
                
                <div class="bg-gradient-to-r from-slate-800/50 to-slate-700/50 p-6 rounded-xl border border-slate-700/50 slide-up" style="animation-delay: 0.2s">
                    <h4 class="font-bold text-indigo-300 mb-6 text-xl flex items-center">
                        <span class="mr-3">⚔️</span>Competitive Advantage Matrix
                    </h4>
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
                        <div>
                            <div class="text-slate-300 leading-relaxed mb-6">${formatToList(planData.competitiveAdvantage)}</div>
                            <div class="space-y-3">
                                ${createProgressBar(planData.competitiveScores?.innovation || 85, 'Innovation Score', 'bg-purple-500')}
                                ${createProgressBar(planData.competitiveScores?.quality || 78, 'Quality Score', 'bg-blue-500')}
                                ${createProgressBar(planData.competitiveScores?.pricing || 72, 'Pricing Advantage', 'bg-green-500')}
                            </div>
                        </div>
                        <div class="w-full h-80">
                            <canvas id="competitiveRadarChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- MVP Roadmap with enhanced visuals -->
                <div class="bg-gradient-to-r from-slate-800/50 to-slate-700/50 p-6 rounded-xl border border-slate-700/50 slide-up" style="animation-delay: 0.4s">
                    <h4 class="font-bold text-indigo-300 mb-6 text-xl flex items-center">
                        <span class="mr-3">🗓️</span>6-Month MVP Development Roadmap
                    </h4>
                    <div class="text-slate-300 leading-relaxed">${formatRoadmap(planData.mvpRoadmap)}</div>
                </div>
                
                <!-- Features, Revenue, Marketing, Risk Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-gradient-to-br from-slate-800/50 to-slate-700/50 p-6 rounded-xl border border-slate-700/50 slide-up">
                        <h4 class="font-bold text-indigo-300 mb-4 text-lg flex items-center">
                            <span class="mr-3">✨</span>Core Features & MVP
                        </h4>
                        <div class="text-slate-300 leading-relaxed">${formatFeatures(planData.coreFeatures)}</div>
                    </div>
                    
                    <div class="bg-gradient-to-br from-slate-800/50 to-slate-700/50 p-6 rounded-xl border border-slate-700/50 slide-up" style="animation-delay: 0.1s">
                        <h4 class="font-bold text-green-300 mb-4 text-lg flex items-center">
                            <span class="mr-3">💰</span>Revenue Model
                        </h4>
                        <div class="text-slate-300 leading-relaxed">${formatToList(planData.monetizationModel)}</div>
                    </div>
                    
                    <div class="bg-gradient-to-br from-slate-800/50 to-slate-700/50 p-6 rounded-xl border border-slate-700/50 slide-up" style="animation-delay: 0.2s">
                        <h4 class="font-bold text-blue-300 mb-4 text-lg flex items-center">
                            <span class="mr-3">🚀</span>Go-to-Market Strategy
                        </h4>
                        <div class="text-slate-300 leading-relaxed">${formatToList(planData.marketingStrategy)}</div>
                    </div>
                    
                    <div class="bg-gradient-to-br from-red-900/20 to-yellow-900/20 p-6 rounded-xl border border-red-700/50 slide-up" style="animation-delay: 0.3s">
                        <h4 class="font-bold text-yellow-300 mb-4 text-lg flex items-center">
                            <span class="mr-3">⚠️</span>Risk Analysis
                        </h4>
                        <div class="text-slate-300 leading-relaxed">${formatToList(planData.riskAnalysis)}</div>
                        <div class="mt-4">
                            ${createRiskIndicator(planData.riskLevel || 'medium')}
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-8 text-center">
                <p class="text-slate-400 text-sm">Business plan generated with AI analysis</p>
            </div>
        </div>
    `;
    
    elements.modalBody.innerHTML = planHtml;
    
    // Grafikleri ve animasyonları başlat
    setTimeout(() => {
        try {
            if (typeof this.renderConfidenceChart === 'function') {
                this.renderConfidenceChart(planData.confidenceScore);
            }
            if (typeof this.renderCompetitiveRadarChart === 'function') {
                this.renderCompetitiveRadarChart(planData.competitiveData);
            }
            if (typeof this.renderRevenueProjectionChart === 'function') {
                this.renderRevenueProjectionChart(planData.revenueData);
            }
            if (typeof this.renderMarketSizeChart === 'function') {
                this.renderMarketSizeChart(planData.marketData);
            }
            if (typeof this.animateProgressBars === 'function') {
                this.animateProgressBars();
            }
            if (typeof this.animateMetricValues === 'function') {
                this.animateMetricValues();
            }
            console.log('✅ All charts and animations initialized successfully');
        } catch (error) {
            console.error('❌ Error initializing charts:', error);
        }
    }, 100);
}
    
    static showError(message) {
        elements.modalLoader.classList.add('hidden');
        elements.modalBody.innerHTML += `
            <div class="text-center p-8 fade-in">
                <div class="text-red-400 text-4xl mb-4">❌</div>
                <h3 class="text-red-400 text-lg font-semibold mb-2">İş Planı Oluşturulamadı</h3>
                <p class="text-red-300 mb-4 whitespace-pre-line">${message}</p>
                <button onclick="window.uiExports.closeModal()" class="bg-slate-700 hover:bg-slate-600 text-white px-6 py-2 rounded-lg transition-colors">
                    Kapat
                </button>
            </div>
        `;
    }

    static addProgressBar() {
        const existingProgress = elements.modalLoader.querySelector('.modal-progress');
        if (existingProgress) {
            existingProgress.remove();
        }
        
        const modalProgressContainer = document.createElement('div');
        modalProgressContainer.className = 'modal-progress mb-4';
        modalProgressContainer.innerHTML = `
            <div class="w-full bg-slate-700 rounded-full h-3 mb-2">
                <div class="modal-progress-bar bg-gradient-to-r from-indigo-500 to-cyan-500 h-3 rounded-full transition-all duration-500" style="width: 0%"></div>
            </div>
            <p class="modal-progress-text text-slate-400 text-sm">Initializing business plan generation...</p>
        `;
        
        elements.modalLoader.appendChild(modalProgressContainer);
        
        return {
            bar: modalProgressContainer.querySelector('.modal-progress-bar'),
            text: modalProgressContainer.querySelector('.modal-progress-text')
        };
    }

    // Export functionality
    static async exportToPDF(filename = 'business-plan') {
        try {
            // Simple PDF export using browser print
            const printWindow = window.open('', '_blank');
            const modalContent = elements.modalBody.innerHTML;
            
            printWindow.document.write(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Business Plan - ${filename}</title>
                    <style>
                        body { 
                            font-family: Arial, sans-serif; 
                            line-height: 1.6; 
                            color: #333; 
                            max-width: 800px; 
                            margin: 0 auto; 
                            padding: 20px; 
                        }
                        h1, h2, h3, h4 { color: #2563eb; margin-top: 30px; }
                        ul, ol { margin: 10px 0; padding-left: 30px; }
                        li { margin: 5px 0; }
                        p { margin: 10px 0; }
                        .fade-in { animation: none; }
                        button { display: none; }
                        svg { display: none; }
                        .bg-gradient-to-r, .bg-slate-800 { 
                            background: #f8f9fa !important; 
                            border: 1px solid #ddd; 
                            padding: 15px; 
                            margin: 10px 0; 
                        }
                        @media print {
                            body { margin: 0; padding: 15px; }
                            .bg-gradient-to-r, .bg-slate-800 { 
                                border: 1px solid #ccc; 
                                break-inside: avoid; 
                            }
                        }
                    </style>
                </head>
                <body>
                    <h1>Business Plan Report</h1>
                    <p><strong>Generated:</strong> ${new Date().toLocaleDateString()}</p>
                    ${modalContent}
                </body>
                </html>
            `);
            
            printWindow.document.close();
            setTimeout(() => {
                printWindow.print();
            }, 250);
            
        } catch (error) {
            console.error('PDF export failed:', error);
            alert('PDF export failed. Please try again or use your browser\'s print function.');
        }
    }

    // Copy to clipboard functionality
    static async copyToClipboard() {
        try {
            const modalContent = elements.modalBody.innerText;
            await navigator.clipboard.writeText(modalContent);
            
            // Show success feedback
            const button = document.getElementById('copyClipboardBtn');
            if (button) {
                const originalText = button.innerHTML;
                button.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Copied!
                `;
                button.classList.add('bg-green-600', 'hover:bg-green-700');
                button.classList.remove('bg-slate-600', 'hover:bg-slate-700');
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.classList.remove('bg-green-600', 'hover:bg-green-700');
                    button.classList.add('bg-slate-600', 'hover:bg-slate-700');
                }, 2000);
            }
            
        } catch (error) {
            console.error('Copy failed:', error);
            alert('Copy to clipboard failed. Please select and copy the text manually.');
        }
    }
    
    static addInteractiveEffects() {
        // Metric card hover effects
        document.querySelectorAll('.metric-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.05) translateY(-2px)';
                card.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1) translateY(0)';
                card.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
            });
        });

        // Roadmap item hover effects
        document.querySelectorAll('.slide-up').forEach((item, index) => {
            item.addEventListener('mouseenter', () => {
                item.style.transform = 'translateX(10px)';
                item.style.transition = 'all 0.3s ease';
            });
            
            item.addEventListener('mouseleave', () => {
                item.style.transform = 'translateX(0)';
            });
        });
    }

    static addScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeInUp');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.slide-up').forEach(el => observer.observe(el));
    }

    static addTypingEffect(element, text, speed = 50) {
        let i = 0;
        element.innerHTML = '';
        const timer = setInterval(() => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }

    static createParticleBackground() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particle-container';
        particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        `;

        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(79, 70, 229, 0.3);
                border-radius: 50%;
                animation: float ${5 + Math.random() * 10}s infinite ease-in-out;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 5}s;
            `;
            particleContainer.appendChild(particle);
        }

        // Float animation keyframes
        const floatKeyframes = `
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
                25% { transform: translateY(-20px) rotate(90deg); opacity: 1; }
                50% { transform: translateY(-10px) rotate(180deg); opacity: 0.8; }
                75% { transform: translateY(-30px) rotate(270deg); opacity: 0.9; }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = floatKeyframes;
        document.head.appendChild(style);

        return particleContainer;
    }
     static enhanceModalWithEffects() {
        setTimeout(() => {
            this.addInteractiveEffects();
            this.addScrollAnimations();
            
            // Particle background ekle (isteğe bağlı)
            // const particles = this.createParticleBackground();
            // elements.modal.appendChild(particles);
            
            // Success sound effect (isteğe bağlı)
            this.playSuccessSound();
        }, 1000);
    }

    /**
     * Başarı sesi çalar (isteğe bağlı)
     */
    static playSuccessSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime); // C5
            oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1); // E5
            oscillator.frequency.setValueAtTime(783.99, audioContext.currentTime + 0.2); // G5
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (e) {
            // Ses çalınamazsa sessizce devam et
        }
    }

    static animateProgressBars() {
    document.querySelectorAll('.progress-bar-animate').forEach(bar => {
        const targetWidth = bar.getAttribute('data-width');
        if (targetWidth) {
            setTimeout(() => {
                bar.style.width = targetWidth;
            }, 300);
        }
    });
}

/**
 * Metric değerlerini animasyonlu şekilde sayar
 */
    static animateMetricValues() {
    document.querySelectorAll('.metric-value').forEach(element => {
        // Ham sayısal değeri 'data-numeric-value' attribute'undan al
        const finalValue = parseFloat(element.getAttribute('data-numeric-value'));
        const displayFormat = element.textContent; // Başlangıçtaki formatı ($100M gibi) al

        if (isNaN(finalValue)) {
            // Eğer sayısal değer yoksa, animasyon yapma
            element.textContent = displayFormat;
            return;
        }

        let startValue = 0;
        const duration = 2000; // 2 saniye
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsedTime = currentTime - startTime;
            const progress = Math.min(elapsedTime / duration, 1);
            const currentValue = startValue + (finalValue - startValue) * progress;

            // Değeri orijinal formata uygun şekilde göster
            if (displayFormat.includes('M')) {
                element.textContent = '$' + (currentValue / 1000000).toFixed(1) + 'M';
            } else if (displayFormat.includes('K')) {
                element.textContent = '$' + Math.round(currentValue / 1000) + 'K';
            } else if (displayFormat.includes('months')) {
                 element.textContent = Math.round(currentValue) + ' months';
            } else {
                element.textContent = Math.round(currentValue).toLocaleString();
            }

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                 // Animasyon bittiğinde son değeri tam olarak ayarla
                 element.textContent = displayFormat;
            }
        };

        requestAnimationFrame(animate);
    });
}

}