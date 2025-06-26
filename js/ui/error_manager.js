

import { elements } from './dom_elements.js';

export class ErrorManager {
    static show(message) {
        elements.errorMessage.innerHTML = `
            <div class="flex items-start gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-400 flex-shrink-0 mt-0.5">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="15" y1="9" x2="9" y2="15"></line>
                    <line x1="9" y1="9" x2="15" y2="15"></line>
                </svg>
                <div>
                    <h4 class="font-semibold text-red-300 mb-1">Hata Oluştu</h4>
                    <p class="text-red-200 text-sm whitespace-pre-line">${message}</p>
                </div>
            </div>
        `;
        elements.errorMessage.classList.remove('hidden');
        
        // Auto hide after 15 seconds
        setTimeout(() => {
            this.hide();
        }, 15000);
    }

    static hide() {
        elements.errorMessage.classList.add('hidden');
    }
}