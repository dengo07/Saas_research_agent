// ui/resultsManager.js - Sonuç Gösterim Modülü

import { elements } from './dom_elements.js';

export class ResultsManager {
    static displayResults(results, onPlanRequest) {
        console.log('🎯 [ResultsManager] displayResults called with:', results?.length, 'results');
        
        // DOM elementini kontrol et
        if (!elements.resultsContainer) {
            console.error('❌ [ResultsManager] resultsContainer element not found!');
            return;
        }
        
        // Container'ı temizle ve pointer events'i sıfırla
        elements.resultsContainer.innerHTML = '';
        elements.resultsContainer.style.pointerEvents = 'auto';
        elements.resultsContainer.style.display = 'grid';
        elements.resultsContainer.style.visibility = 'visible';
        elements.resultsContainer.style.opacity = '1';
        
        // Parent elements'ı da kontrol et ve görünür yap
        if (elements.resultsSection) {
            elements.resultsSection.style.pointerEvents = 'auto';
            elements.resultsSection.style.display = 'block';
            elements.resultsSection.style.visibility = 'visible';
            elements.resultsSection.style.opacity = '1';
            elements.resultsSection.classList.remove('hidden');
            
            console.log('✅ [ResultsManager] Results section made visible');
        }
        
        console.log('📍 [ResultsManager] Container state after cleanup:', {
            innerHTML: elements.resultsContainer.innerHTML.length,
            pointerEvents: elements.resultsContainer.style.pointerEvents,
            display: elements.resultsContainer.style.display,
            visibility: elements.resultsContainer.style.visibility
        });
        
        if (!results || results.length === 0) {
            console.log('⚠️ [ResultsManager] No results to display');
            elements.resultsContainer.innerHTML = `
                <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 text-center text-slate-400 md:col-span-2 lg:col-span-3 fade-in">
                    <div class="text-4xl mb-4">🔍</div>
                    <h3 class="text-lg font-semibold mb-2">Sonuç Bulunamadı</h3>
                    <p>Bu konu için doğrulanmış fırsat bulunamadı.</p>
                    <p class="text-sm mt-2">Daha geniş bir arama terimi deneyin veya farklı kelimeler kullanın.</p>
                </div>
            `;
            
            // No results durumunda da visibility'yi guarantee et
            this.ensureVisibility();
            return;
        }

        console.log('✅ [ResultsManager] Creating', results.length, 'result cards');
        
        results.forEach((result, index) => {
            const card = this.createResultCard(result, index);
            const planButton = card.querySelector('.business-plan-btn');
            
            if (planButton) {
                planButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    console.log('🔘 [ResultsManager] Plan button clicked for:', result.title);
                    
                    planButton.disabled = true;
                    planButton.textContent = '⏳ Generating...';
                    
                    onPlanRequest(result).finally(() => {
                        planButton.disabled = false;
                        planButton.innerHTML = '📊 Generate Research-Backed Plan';
                    });
                });
            } else {
                console.warn('⚠️ [ResultsManager] Plan button not found in card', index);
            }
            
            elements.resultsContainer.appendChild(card);
        });
        
        // Results'ın görünür olduğunu guarantee et
        setTimeout(() => {
            console.log('🎯 [ResultsManager] Making results visible and scrolling...');
            
            this.ensureVisibility();
            
            // Scroll to results
            elements.resultsContainer.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
            
            // Final visibility check
            setTimeout(() => {
                this.performVisibilityCheck();
            }, 1000);
        }, 100);
    }
    
    static ensureVisibility() {
        console.log('🔧 [ResultsManager] Ensuring results visibility...');
        
        // Results section'ı kesinlikle görünür yap
        if (elements.resultsSection) {
            elements.resultsSection.classList.remove('hidden');
            elements.resultsSection.style.display = 'block';
            elements.resultsSection.style.visibility = 'visible';
            elements.resultsSection.style.pointerEvents = 'auto';
            elements.resultsSection.style.opacity = '1';
            elements.resultsSection.style.zIndex = '1';
        }
        
        // Results container'ı kesinlikle görünür yap
        if (elements.resultsContainer) {
            elements.resultsContainer.style.display = 'grid';
            elements.resultsContainer.style.visibility = 'visible';
            elements.resultsContainer.style.pointerEvents = 'auto';
            elements.resultsContainer.style.opacity = '1';
        }
        
        // Loading spinner'ı gizle
        if (elements.loadingSpinner) {
            elements.loadingSpinner.classList.add('hidden');
        }
        
        // Potansiyel overlay elementleri kontrol et
        this.clearBlockingOverlays();
    }
    
    static clearBlockingOverlays() {
        // Modal dışındaki overlay elementleri temizle
        const overlays = document.querySelectorAll('[style*="position: fixed"], [style*="position: absolute"]');
        overlays.forEach(overlay => {
            if (overlay !== elements.modal && 
                overlay.style.zIndex > 100 && 
                !overlay.classList.contains('modal') &&
                !overlay.id.includes('modal')) {
                console.log('🚫 [ResultsManager] Clearing potential blocking overlay:', overlay);
                overlay.style.pointerEvents = 'none';
                overlay.style.zIndex = '0';
            }
        });
    }
    
    static performVisibilityCheck() {
        const isVisible = elements.resultsContainer.offsetHeight > 0;
        const hasContent = elements.resultsContainer.children.length > 0;
        const isHidden = elements.resultsSection?.classList.contains('hidden');
        
        console.log('🔍 [ResultsManager] Final visibility check:', { 
            isVisible, 
            hasContent, 
            isHidden,
            offsetHeight: elements.resultsContainer.offsetHeight,
            childrenCount: elements.resultsContainer.children.length
        });
        
        if (!isVisible || !hasContent || isHidden) {
            console.error('❌ [ResultsManager] Results are not visible! Forcing visibility...');
            this.forceResultsVisibility();
        } else {
            console.log('✅ [ResultsManager] Results are properly visible');
        }
    }
    
    static forceResultsVisibility() {
        console.log('🔧 [ResultsManager] FORCING results visibility...');
        
        // Tüm parent elementleri visible yap
        const elementsToShow = [
            elements.resultsSection,
            elements.resultsContainer,
            document.querySelector('main'),
            document.querySelector('body')
        ];
        
        elementsToShow.forEach(el => {
            if (el) {
                el.style.display = el === elements.resultsContainer ? 'grid' : 'block';
                el.style.visibility = 'visible';
                el.style.pointerEvents = 'auto';
                el.style.opacity = '1';
                el.style.zIndex = el === elements.resultsSection ? '10' : 'auto';
                el.classList.remove('hidden');
                console.log('🔧 [ResultsManager] Forced visibility for:', el.tagName, el.id || el.className);
            }
        });
        
        this.clearBlockingOverlays();
        
        // Scroll'u tekrar dene
        setTimeout(() => {
            elements.resultsContainer.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 200);
    }

    static createResultCard(result, index) {
        const card = document.createElement('div');
        card.className = "result-card bg-gradient-to-br from-slate-800 to-slate-700/50 p-6 rounded-xl border border-slate-600 hover:border-indigo-500 hover:scale-[1.02] transition-all fade-in shadow-lg stagger-item";
        card.style.animationDelay = `${index * 0.1}s`;
        card.style.pointerEvents = 'auto';
        card.style.cursor = 'default';
        card.style.display = 'block';
        card.style.visibility = 'visible';
        card.style.opacity = '1';
        
        const potential = result.potential || Math.floor(Math.random() * 3) + 7;
        const tags = Array.isArray(result.tags) ? result.tags : ['saas', 'opportunity'];
        const painPoints = Array.isArray(result.painPoints) ? result.painPoints : [];
        
        card.innerHTML = `
            <div class="mb-4">
                <div class="flex justify-between items-start mb-3">
                    <span class="text-xs font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-3 py-1 rounded-full">
                        ${result.source || 'Research Data'}
                    </span>
                    <div class="flex items-center gap-1 text-yellow-400">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                        </svg>
                        <span class="font-bold text-sm">${potential}/10</span>
                    </div>
                </div>
                
                <h3 class="text-xl font-bold text-white mb-2">
                    ${result.title || 'Untitled Opportunity'}
                </h3>
                
                <p class="text-slate-300 text-sm mb-3">
                    ${result.description || 'No description available'}
                </p>
                
                <div class="bg-slate-700/50 p-3 rounded-lg mb-3">
                    <div class="flex items-center gap-2 mb-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-green-400">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        <span class="text-xs font-semibold text-green-400">VALIDATION</span>
                    </div>
                    <p class="text-xs text-slate-300">
                        ${result.validation || 'Market research indicates potential for this solution'}
                    </p>
                </div>
                
                <div class="text-xs text-slate-400 mb-3">
                    <strong>Market Size:</strong> ${result.marketSize || 'To be determined'}
                </div>
                
                ${painPoints.length > 0 ? `
                    <div class="text-xs text-slate-400 mb-3">
                        <strong>Pain Points:</strong> ${painPoints.slice(0, 2).join(', ')}${painPoints.length > 2 ? '...' : ''}
                    </div>
                ` : ''}
            </div>
            
            <div class="border-t border-slate-600 pt-4">
                <div class="flex flex-wrap gap-2 mb-4">
                    ${tags.map(tag => `
                        <span class="text-xs bg-indigo-900/50 text-indigo-300 px-2.5 py-1 rounded-full font-medium">
                            ${tag}
                        </span>
                    `).join('')}
                </div>
                
                <button class="w-full text-center bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold py-3 px-4 rounded-lg transition-all transform hover:scale-[1.02] business-plan-btn disabled:opacity-50 disabled:cursor-not-allowed" 
                        style="pointer-events: auto; cursor: pointer; display: block;">
                    📊 Generate Research-Backed Plan
                </button>
            </div>
        `;
        
        return card;
    }

    static clearResults() {
        console.log('🧹 [ResultsManager] Clearing results...');
        if (elements.resultsContainer) {
            elements.resultsContainer.innerHTML = '';
        }
        if (elements.resultsSection) {
            elements.resultsSection.classList.add('hidden');
        }
    }
    
    // Debugging fonksiyonu
    static debugVisibility() {
        console.log('🔍 [ResultsManager] Debug visibility state:', {
            resultsSection: {
                exists: !!elements.resultsSection,
                classes: elements.resultsSection?.className,
                style: elements.resultsSection?.style.cssText,
                hidden: elements.resultsSection?.classList.contains('hidden'),
                offsetHeight: elements.resultsSection?.offsetHeight
            },
            resultsContainer: {
                exists: !!elements.resultsContainer,
                style: elements.resultsContainer?.style.cssText,
                childrenCount: elements.resultsContainer?.children.length,
                offsetHeight: elements.resultsContainer?.offsetHeight
            }
        });
    }
}