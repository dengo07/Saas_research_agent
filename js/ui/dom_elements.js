// ui/dom_elements.js - DOM Elementleri Modülü
// Uygulamadaki tüm UI elementlerine referansları barındırır.

export const elements = {
    searchForm: document.getElementById('search-form'),
    searchInput: document.getElementById('search-input'),
    searchButton: document.getElementById('search-button'),
    resultsContainer: document.getElementById('results-container'),
    errorMessage: document.getElementById('error-message'),
    researchProgress: document.getElementById('research-progress'),
    progressBar: document.getElementById('progress-bar'),
    progressText: document.getElementById('progress-text'),
    modal: document.getElementById('business-plan-modal'),
    modalTitle: document.getElementById('modal-title'),
    modalBody: document.getElementById('modal-body'),
    modalLoader: document.getElementById('modal-loader')
};