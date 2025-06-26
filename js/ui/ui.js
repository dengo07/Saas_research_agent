

import { ProgressManager } from './process_manager.js';
import { ResultsManager } from './results_manager.js';
import { ModalManager } from './modal_manager.js';
import { ErrorManager } from './error_manager.js';
import { BackendStatusManager } from './backend_status_manager.js';
import { DebugMetricsManager } from './debug_metrics_manager.js';
import { elements } from './dom_elements.js';

export { elements };
// Initialize progress manager
export const progressManager = new ProgressManager();
export const modalManager = new ModalManager();
// Export all UI functions for backward compatibility
export const showError = ErrorManager.show.bind(ErrorManager);
export const hideError = ErrorManager.hide.bind(ErrorManager);
export const displayResults = ResultsManager.displayResults.bind(ResultsManager);
export const clearResults = ResultsManager.clearResults.bind(ResultsManager);
export const openModal = ModalManager.open.bind(ModalManager);
export const closeModal = ModalManager.close.bind(ModalManager);
export const addProgressBar = ModalManager.addProgressBar.bind(ModalManager);
export const displayBusinessPlan = ModalManager.displayBusinessPlan.bind(ModalManager);
export const showModalError = ModalManager.showError.bind(ModalManager);
export const showBackendStatus = BackendStatusManager.show.bind(BackendStatusManager);
export const updateDebugMetrics = DebugMetricsManager.update.bind(DebugMetricsManager);
export const setResearchState = (isResearching) => {
    if (isResearching) {
        progressManager.start();
    } else {
        progressManager.stop();
    }
};

// Global access for modal close button
window.uiExports = { closeModal};

