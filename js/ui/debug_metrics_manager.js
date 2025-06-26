export class DebugMetricsManager {
    static update(metrics) {
        if (!window.location.search.includes('debug=true')) return;
        
        const requestsElement = document.getElementById('debug-requests');
        const errorsElement = document.getElementById('debug-errors');
        const successRateElement = document.getElementById('debug-success-rate');
        const avgTimeElement = document.getElementById('debug-avg-time');
        
        if (requestsElement) requestsElement.textContent = metrics.totalRequests || 0;
        if (errorsElement) errorsElement.textContent = metrics.errorCount || 0;
        if (successRateElement) successRateElement.textContent = metrics.successRate || '0%';
        if (avgTimeElement) avgTimeElement.textContent = `${metrics.avgTime || 0}ms`;
    }
}