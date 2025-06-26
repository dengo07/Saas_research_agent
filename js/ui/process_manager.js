// ui/progressManager.js - İlerleme Yönetimi Modülü

import { elements } from './dom_elements.js';

export class ProgressManager {
    constructor() {
        this.progressBar = elements.progressBar;
        this.progressText = elements.progressText;
        this.researchStartTime = 0;
        this.progressTimer = null;
    }

    start() {
        elements.researchProgress.classList.remove('hidden');
        elements.searchButton.disabled = true;
        elements.searchButton.innerHTML = `
            <svg class="animate-spin w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
            </svg>
            <span class="hidden md:inline ml-2">Researching...</span>
        `;
        
        this.progressBar.style.width = '0%';
        this.progressBar.style.backgroundColor = '';
        this.progressText.textContent = 'Initializing research agent...';
        
        this.researchStartTime = Date.now();
        this.startTimer();
    }

    stop() {
        setTimeout(() => {
            elements.researchProgress.classList.add('hidden');
        }, 1000);
        
        elements.searchButton.disabled = false;
        elements.searchButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 5a3 3 0 1 0-5.997.142 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 0 0 12 18Z"/>
                <path d="M12 5a3 3 0 1 1 5.997.142 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 0 1 12 18Z"/>
                <path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/>
            </svg>
            <span class="hidden md:inline ml-2">Research Ideas</span>
        `;
        
        this.stopTimer();
    }

    update(percentage, text) {
        this.progressBar.style.width = percentage + '%';
        this.progressText.textContent = text;
    }

    setError(message) {
        this.progressBar.style.backgroundColor = '#ef4444';
        this.progressText.textContent = message;
    }

    startTimer() {
        if (this.progressTimer) {
            clearInterval(this.progressTimer);
        }
        
        this.progressTimer = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.researchStartTime) / 1000);
            const timerElement = document.getElementById('research-timer');
            if (timerElement) {
                timerElement.textContent = `${elapsed}s`;
            }
            
            const progressElement = document.getElementById('progress-percentage');
            if (progressElement && this.progressBar) {
                const width = parseFloat(this.progressBar.style.width) || 0;
                progressElement.textContent = Math.round(width);
            }
        }, 100);
    }

    stopTimer() {
        if (this.progressTimer) {
            clearInterval(this.progressTimer);
            this.progressTimer = null;
        }
    }
}