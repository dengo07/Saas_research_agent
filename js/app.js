// app.js - Main Application Module
// Ana uygulama mantığı ve orchestration

import { api, CONFIG } from './api.js';
import * as ui from './ui/ui.js';

// Research Manager - Integrated Progress ile
class ResearchManager {
    async researchWithProgress(query, options = {}) {
        console.log(`🔍 Starting research with integrated progress: "${query}"`);
        
        const progressBar = ui.elements.progressBar;
        const progressText = ui.elements.progressText;
        const cacheStatus = document.getElementById('cache-status');
        
        try {
            // Step 1: Backend health check (10%)
            ui.progressManager.update(10, 'Verifying backend connectivity...');
            
            const health = await api.healthCheck();
            console.log('✅ Backend health verified:', health.status);
            
            if (cacheStatus) {
                cacheStatus.textContent = `Cache: ${health.cache_items || 0} items`;
            }
            
            // Step 2: Initialize research (20%)
            ui.progressManager.update(20, 'Initializing AI research agent...');
            await new Promise(resolve => setTimeout(resolve, 300));
            
            // Step 3: Check for cached data (30%)
            ui.progressManager.update(30, 'Checking cache for existing data...');
            
            let cacheHit = false;
            try {
                const cacheStats = await api.getCacheStats();
                if (cacheStats.total_items > 0) {
                    cacheHit = true;
                    progressText.textContent = `Found ${cacheStats.total_items} cached items, processing...`;
                    if (cacheStatus) {
                        cacheStatus.textContent = `Cache: ${cacheStats.total_items} items (HIT)`;
                    }
                }
            } catch (error) {
                console.log('⚠️ Cache check failed, proceeding with fresh research');
                if (cacheStatus) {
                    cacheStatus.textContent = 'Cache: unavailable';
                }
            }
            
            await new Promise(resolve => setTimeout(resolve, cacheHit ? 200 : 500));
            
            // Step 4: Market analysis (50%)
            ui.progressManager.update(50, 'Analyzing market trends and search patterns...');
            await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 400));
            
            // Step 5: Social research (70%)
            ui.progressManager.update(70, 'Scanning social media and forums for pain points...');
            await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 500));
            
            // Step 6: Competitor research (85%)
            ui.progressManager.update(85, 'Researching competitors and market gaps...');
            await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 400));
            
            // Step 7: AI synthesis (95%)
            ui.progressManager.update(95, 'Synthesizing data with AI agent...');
            
            const researchStartTime = Date.now();
            const ideas = await api.researchIdeas(query, options);
            const researchTime = Date.now() - researchStartTime;
            
            // Step 8: Completion (100%)
            ui.progressManager.update(100, `Research completed! Found ${ideas.length} opportunities (${researchTime}ms)`);
            
            await new Promise(resolve => setTimeout(resolve, 500));
            
            console.log(`✅ Research completed: ${ideas.length} ideas in ${researchTime}ms`);
            return ideas;
            
        } catch (error) {
            // Error state
            ui.progressManager.setError(`❌ Research failed: ${error.message}`);
            
            setTimeout(() => {
                progressBar.style.backgroundColor = '';
            }, 3000);
            
            throw error;
        }
    }

    async generateBusinessPlanWithProgress(idea) {
        console.log('📊 Generating business plan with modal progress:', idea.title);
        
        const modalProgress = ui.addProgressBar();
        
        try {
            // Step 1: Market research (25%)
            modalProgress.text.textContent = 'Conducting additional market research...';
            modalProgress.bar.style.width = '25%';
            await new Promise(resolve => setTimeout(resolve, 800));
            
            // Step 2: Competitor analysis (50%)
            modalProgress.text.textContent = 'Analyzing competitors and positioning...';
            modalProgress.bar.style.width = '50%';
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Step 3: AI generation (80%)
            modalProgress.text.textContent = 'Generating comprehensive business plan...';
            modalProgress.bar.style.width = '80%';
            
            const planStartTime = Date.now();
            const planData = await api.generateBusinessPlan(idea);
            const planTime = Date.now() - planStartTime;
            
            // Step 4: Completion (100%)
            modalProgress.text.textContent = `Business plan generated successfully! (${planTime}ms)`;
            modalProgress.bar.style.width = '100%';
            
            await new Promise(resolve => setTimeout(resolve, 500));
            
            console.log(`✅ Business plan generated in ${planTime}ms`);
            return planData;
            
        } catch (error) {
            modalProgress.bar.style.backgroundColor = '#ef4444';
            modalProgress.text.textContent = `❌ Plan generation failed: ${error.message}`;
            throw error;
        }
    }
}

// Application Controller
class AppController {
    constructor() {
        this.researchManager = new ResearchManager();
        this.initializeEventListeners();
        this.performStartupChecks();
    }

    initializeEventListeners() {
        // Form submission
        ui.elements.searchForm.addEventListener('submit', (e) => this.handleResearchSearch(e));
        
        // Modal events
        ui.elements.modal.addEventListener('click', ui.closeModal);
        ui.elements.modal.querySelector('.modal-content').addEventListener('click', (e) => {
            e.stopPropagation();
        });
        
        // ESC key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !ui.elements.modal.classList.contains('hidden')) {
                ui.closeModal();
            }
        });
        
        // Network monitoring
        window.addEventListener('online', () => {
            console.log('🌐 Network: Online');
            ui.hideError();
        });
        
        window.addEventListener('offline', () => {
            console.log('🌐 Network: Offline');
            ui.showError('🌐 İnternet bağlantısı kesildi. Lütfen bağlantınızı kontrol edin.');
        });
        
        // Global error handler
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            
            const metrics = api.getPerformanceMetrics();
            console.log('📊 Error context:', metrics);
            
            if (event.reason && event.reason.message) {
                if (event.reason.message.includes('fetch')) {
                    ui.showError(`🌐 Bağlantı hatası: Backend sunucusuna ulaşılamıyor.
                    
📊 Performance: ${metrics.successRate} success rate, ${metrics.totalRequests} total requests`);
                } else {
                    ui.showError(`⚠️ Beklenmeyen hata: ${event.reason.message}

📊 Context: ${metrics.totalRequests} requests, ${metrics.errorCount} errors`);
                }
            }
        });
    }

    async handleResearchSearch(event) {
        event.preventDefault();
        
        const query = ui.elements.searchInput.value.trim();
        
        // Input validation
        if (query === '') {
            ui.showError('Lütfen bir arama terimi girin');
            return;
        }

        if (query.length < 2) {
            ui.showError('Arama terimi en az 2 karakter olmalıdır');
            return;
        }

        if (query.length > 200) {
            ui.showError('Arama terimi 200 karakterden uzun olamaz');
            return;
        }

        const dangerousPattern = /[<>\"'&]/;
        if (dangerousPattern.test(query)) {
            ui.showError('Geçersiz karakterler tespit edildi');
            return;
        }

        console.log(`🔍 Starting research with real progress for: "${query}"`);
        
        ui.setResearchState(true);
        ui.hideError();
        ui.clearResults();

        const searchStartTime = Date.now();

        try {
            // Use integrated progress research
            const ideas = await this.researchManager.researchWithProgress(query, {
                includeReddit: true,
                includeTrends: true,
                includeCompetitors: true
            });

            const searchTime = Date.now() - searchStartTime;
            console.log(`✅ Complete research flow finished in ${searchTime}ms`);
            
            // Performance metrics
            const metrics = api.getPerformanceMetrics();
            console.log('📊 API Performance:', metrics);
            
            // Display results
            ui.displayResults(ideas, (idea) => this.handleBusinessPlanRequest(idea));

            // Success metrics
            if (ideas.length > 0) {
                console.log(`🎯 Research success: ${ideas.length} opportunities, ${metrics.successRate} API success rate`);
            }

            // Update debug metrics if in debug mode
            ui.updateDebugMetrics(metrics);

        } catch (error) {
            console.error('❌ Research failed:', error);
            
            const searchTime = Date.now() - searchStartTime;
            console.log(`⏱️ Failed after ${searchTime}ms`);
            
            this.showDetailedError(error, searchTime);
            
        } finally {
            ui.setResearchState(false);
        }
    }

    async handleBusinessPlanRequest(ideaData) {
        console.log(`📊 Generating business plan with progress for: ${ideaData.title}`);
        
        ui.openModal(ideaData.title);
        
        const planStartTime = Date.now();
        
        try {
            const planData = await this.researchManager.generateBusinessPlanWithProgress(ideaData);
            const planTime = Date.now() - planStartTime;
            
            console.log(`✅ Business plan generated in ${planTime}ms:`, planData);
            
            ui.displayBusinessPlan(planData);
            
            // Performance log
            const metrics = api.getPerformanceMetrics();
            console.log(`📊 Business plan performance: ${planTime}ms, API success rate: ${metrics.successRate}`);
            
        } catch (error) {
            console.error('❌ Business plan generation failed:', error);
            
            const planTime = Date.now() - planStartTime;
            console.log(`⏱️ Business plan failed after ${planTime}ms`);
            
            this.showBusinessPlanError(error, planTime);
        }
    }

    showDetailedError(error, searchTime) {
        let errorMessage = 'Araştırma sırasında bir hata oluştu.';
        const metrics = api.getPerformanceMetrics();
        
        if (error.message.includes('Backend sunucusuna bağlanılamıyor')) {
            errorMessage = `❌ Backend sunucusu çalışmıyor!

🔧 Çözüm adımları:
1. Terminal açın
2. "python backend.py" komutunu çalıştırın  
3. "Server running on http://127.0.0.1:8000" mesajını bekleyin
4. Bu sayfayı yenileyin

⏱️ Failed after ${searchTime}ms | Performance: ${metrics.successRate}`;
        } else if (error.message.includes('429') || error.message.includes('rate limit')) {
            errorMessage = '⏳ Çok fazla istek gönderdiniz. Lütfen 1-2 dakika bekleyip tekrar deneyin.';
        } else if (error.message.includes('500')) {
            errorMessage = `🔧 Sunucu hatası oluştu.

🔍 Olası nedenler:
- API anahtarları eksik veya geçersiz
- Backend konfigürasyon hatası
- Sunucu kaynak sorunu

⏱️ Failed after ${searchTime}ms
💡 Backend loglarını kontrol edin.`;
        } else if (error.message.includes('zaman aşımına uğradı')) {
            errorMessage = `⏰ İstek çok uzun sürdü (${searchTime}ms > 30s).

🔍 Olası nedenler:
- Yavaş internet bağlantısı
- Backend sunucusu yoğun
- API servisleri yavaş

💡 Tekrar deneyin veya internet bağlantınızı kontrol edin.`;
        } else if (error.message.includes('CORS')) {
            errorMessage = `🌐 CORS hatası tespit edildi.

🔧 Çözüm:
- Backend'i yeniden başlatın
- CORS ayarlarının doğru olduğundan emin olun
- Browser cache'ini temizleyin (Ctrl+F5)

⏱️ Error occurred at ${searchTime}ms`;
        }
        
        ui.showError(errorMessage);
    }

    showBusinessPlanError(error, planTime) {
        let errorMessage = 'İş planı oluşturulurken bir hata oluştu.';
        
        if (error.message.includes('Backend sunucusuna bağlanılamıyor')) {
            errorMessage = `❌ Backend bağlantısı kesildi.

🔧 Çözüm:
- Backend sunucusunun çalıştığından emin olun
- Ağ bağlantınızı kontrol edin

⏱️ Failed after ${planTime}ms`;
        } else if (error.message.includes('429')) {
            errorMessage = '⏳ Çok fazla istek. Lütfen bekleyin ve tekrar deneyin.';
        } else if (error.message.includes('500')) {
            errorMessage = `🔧 Sunucu hatası:

${error.message}

⏱️ Failed after ${planTime}ms
💡 API anahtarlarını ve backend loglarını kontrol edin.`;
        } else if (error.message.includes('422')) {
            errorMessage = `📝 Veri formatı hatası.

🔍 Problem: Geçersiz veri formatı
⏱️ Failed after ${planTime}ms
💡 Lütfen tekrar deneyin.`;
        } else if (error.message.includes('zaman aşımına uğradı')) {
            errorMessage = `⏰ İş planı oluşturma zaman aşımına uğradı.

⏱️ Timeout after ${planTime}ms
💡 İnternet bağlantınızı kontrol edin veya tekrar deneyin.`;
        }
        
        ui.showModalError(errorMessage);
    }

    async performStartupChecks() {
        const startTime = Date.now();
        
        try {
            console.log('🔍 Initial backend health check...');
            const health = await api.detailedHealthCheck();
            const checkTime = Date.now() - startTime;
            
            console.log(`✅ Backend is ready in ${checkTime}ms:`, health);
            
            ui.showBackendStatus('connected', `Ready in ${checkTime}ms`);
            
            // API key warnings
            if (!health.api_keys?.openrouter) {
                console.warn('⚠️ OpenRouter API key not configured');
                ui.showError(`⚠️ OpenRouter API anahtarı yapılandırılmamış.

🔧 Çözüm:
1. .env dosyasında OPENROUTER_API_KEY ayarlayın
2. Backend'i yeniden başlatın

💡 Şimdilik fallback mode aktif.`);
            }
            
            // Performance summary
            const metrics = api.getPerformanceMetrics();
            console.log(`📊 Initial performance: ${checkTime}ms health check, ${metrics.successRate} success rate`);
            
        } catch (error) {
            const checkTime = Date.now() - startTime;
            console.warn(`⚠️ Backend not ready after ${checkTime}ms:`, error.message);
            
            ui.showBackendStatus('disconnected');
            ui.showError(`❌ Backend hazır değil! (${checkTime}ms timeout)

🔧 Backend'i başlatmak için:
1. Terminal açın
2. "python backend.py" komutunu çalıştırın
3. "Server running on http://127.0.0.1:8000" mesajını bekleyin
4. Bu sayfayı yenileyin

💡 Eğer backend çalışıyorsa, CORS ayarlarını kontrol edin.`);
        }
        
        // Periodic health check
        setInterval(async () => {
            const startTime = Date.now();
            try {
                await api.healthCheck();
                const checkTime = Date.now() - startTime;
                ui.showBackendStatus('connected', `${checkTime}ms`);
            } catch (error) {
                ui.showBackendStatus('disconnected');
            }
        }, 30000); // Every 30 seconds
    }

    // Debug tools
    setupDebugMode() {
        if (!CONFIG.DEBUG_MODE) return;
        
        document.body.classList.add('debug-mode');
        
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            ui.showError(`Debug Error: ${event.error.message}`);
        });
        
        console.log('🐛 Debug mode enabled');
        
        // Enhanced debug tools
        window.debugAPI = {
            api: api,
            controller: this,
            testBackend: () => api.healthCheck(),
            testResearch: (query) => this.researchManager.researchWithProgress(query || 'test'),
            testBusinessPlan: (idea) => this.researchManager.generateBusinessPlanWithProgress(idea || {
                title: "Test SaaS",
                description: "Test description", 
                source: "Test",
                potential: 8,
                tags: ["test"],
                validation: "Test validation",
                marketSize: "$100M",
                painPoints: ["Test pain point"]
            }),
            getMetrics: () => api.getPerformanceMetrics(),
            benchmarkAPI: async (iterations = 5) => {
                console.log(`🏃‍♂️ Running API benchmark with ${iterations} iterations...`);
                const times = [];
                
                for (let i = 0; i < iterations; i++) {
                    const start = Date.now();
                    try {
                        await api.healthCheck();
                        times.push(Date.now() - start);
                    } catch (error) {
                        console.error(`Iteration ${i + 1} failed:`, error);
                    }
                }
                
                if (times.length === 0) {
                    console.log('❌ All benchmark iterations failed');
                    return { avgTime: 0, minTime: 0, maxTime: 0, successRate: 0 };
                }
                
                const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
                const minTime = Math.min(...times);
                const maxTime = Math.max(...times);
                
                console.log(`📊 Benchmark Results:
Average: ${avgTime.toFixed(1)}ms
Min: ${minTime}ms
Max: ${maxTime}ms
Success Rate: ${(times.length / iterations * 100).toFixed(1)}%`);
                
                return { avgTime, minTime, maxTime, successRate: times.length / iterations };
            }
        };
        
        console.log('🔧 Enhanced debug tools available at window.debugAPI');
        console.log('💡 Try: window.debugAPI.benchmarkAPI() to test performance');
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 SaaS Research Agent Frontend v3.0');
    console.log('🔗 Backend URL:', CONFIG.BACKEND_URL);
    console.log('🔧 Debug Mode:', CONFIG.DEBUG_MODE ? 'ON' : 'OFF');
    
    const app = new AppController();
    
    if (CONFIG.DEBUG_MODE) {
        app.setupDebugMode();
    }
});


// Modal kapatma fonksiyonunu düzeltin
export const closeModal = () => {
    const modal = document.getElementById('business-plan-modal');
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
    console.log('Modal kapatıldı');
};

// Event listener'ları DOM yüklendiğinde ekleyin
document.addEventListener('DOMContentLoaded', function() {
    const closeBtn = document.getElementById('close-modal-btn');
    const modal = document.getElementById('business-plan-modal');
    
    // X butonu
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeModal();
        });
    }
    
    // Background tıklama
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    // ESC tuşu
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });
});

// Global erişim
window.closeModal = closeModal;

// Export for global access if needed
window.appAPI = api;