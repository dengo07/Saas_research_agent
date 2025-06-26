// api.js - Enhanced API Client Module
// Tüm backend iletişimini yöneten geliştirilmiş modül

export const CONFIG = {
    BACKEND_URL: 'http://127.0.0.1:8000',
    API_TIMEOUT: 365000,
    DEBUG_MODE: window.location.search.includes('debug=true') || localStorage.getItem('debugMode') === 'true'
};

export class SaaSResearchAPI {
    constructor() {
        this.baseUrl = CONFIG.BACKEND_URL;
        this.timeout = CONFIG.API_TIMEOUT;
        this.requestCount = 0;
        this.errorCount = 0;
        this.responseTimes = [];
        this.lastError = null;
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        this.requestCount++;
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        const config = {
            signal: controller.signal,
            mode: 'cors',
            credentials: 'omit',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Request-ID': this.requestCount.toString(),
                ...options.headers
            },
            ...options
        };

        const startTime = Date.now();

        try {
            if (CONFIG.DEBUG_MODE) {
                console.log(`🌐 Request #${this.requestCount}: ${options.method || 'GET'} ${url}`);
                console.log('📦 Request config:', config);
                if (config.body) {
                    console.log('📝 Request body:', config.body);
                }
            }
            
            const response = await fetch(url, config);
            clearTimeout(timeoutId);
            
            const responseTime = Date.now() - startTime;
            this.responseTimes.push(responseTime);
            
            if (CONFIG.DEBUG_MODE) {
                console.log(`📡 Response #${this.requestCount}: ${response.status} ${response.statusText} (${responseTime}ms)`);
                console.log('📋 Response headers:', Object.fromEntries(response.headers.entries()));
            }
            
            // Get response text first
            const responseText = await response.text();
            
            if (CONFIG.DEBUG_MODE) {
                console.log(`📄 Raw response (${responseText.length} chars):`, 
                    responseText.length > 500 ? responseText.substring(0, 500) + '...' : responseText);
            }
            
            if (!response.ok) {
                this.errorCount++;
                const error = this.createErrorFromResponse(response, responseText);
                this.lastError = error;
                throw error;
            }
            
            // Handle empty responses
            if (!responseText || responseText.trim() === '') {
                if (CONFIG.DEBUG_MODE) {
                    console.warn('⚠️ Empty response received');
                }
                return {}; // Return empty object for empty responses
            }
            
            // Parse JSON safely
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (parseError) {
                console.error('❌ JSON Parse Error:', parseError);
                console.error('🔍 Raw response that failed to parse:', responseText);
                
                // Check if response looks like HTML (error page)
                if (responseText.trim().startsWith('<')) {
                    throw new Error(`Server returned HTML instead of JSON. Status: ${response.status}`);
                }
                
                // Check if response is plain text error message
                if (responseText.length < 200 && !responseText.includes('{')) {
                    throw new Error(`Server error: ${responseText}`);
                }
                
                throw new Error(`Invalid JSON response from server. Parse error: ${parseError.message}`);
            }
            
            if (CONFIG.DEBUG_MODE) {
                console.log(`✅ Success #${this.requestCount}: ${endpoint} (${responseTime}ms)`);
                console.log('📊 Parsed data:', data);
            }
            
            return data;
            
        } catch (error) {
            clearTimeout(timeoutId);
            this.errorCount++;
            
            const responseTime = Date.now() - startTime;
            this.responseTimes.push(responseTime);
            
            if (CONFIG.DEBUG_MODE) {
                console.error(`❌ Error #${this.requestCount}: ${endpoint} (${responseTime}ms)`, error);
                console.error('🔍 Error details:', {
                    name: error.name,
                    message: error.message,
                    stack: error.stack
                });
            }
            
            // Categorize and enhance error messages
            const enhancedError = this.enhanceError(error, endpoint, options);
            this.lastError = enhancedError;
            throw enhancedError;
        }
    }

    createErrorFromResponse(response, responseText) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        let errorType = 'api';
        
        try {
            const errorData = JSON.parse(responseText);
            errorMessage = errorData.detail || errorData.message || errorMessage;
            
            // Detect specific error types from backend
            if (errorData.type) {
                errorType = errorData.type;
            } else if (errorMessage.includes('validation')) {
                errorType = 'validation';
            } else if (errorMessage.includes('timeout')) {
                errorType = 'timeout';
            }
        } catch (e) {
            if (responseText.includes('<html>')) {
                errorMessage = `Server returned HTML error page (${response.status})`;
                errorType = 'server';
            } else if (responseText.trim()) {
                errorMessage = responseText.trim();
            }
        }
        
        const error = new Error(errorMessage);
        error.status = response.status;
        error.type = errorType;
        error.response = response;
        error.responseText = responseText;
        
        return error;
    }

    enhanceError(error, endpoint, options) {
        let enhancedMessage = error.message;
        let errorType = error.type || 'general';
        
        if (error.name === 'AbortError') {
            enhancedMessage = `Request timeout (${this.timeout/1000}s): ${endpoint}`;
            errorType = 'timeout';
        } else if (error.message.includes('Failed to fetch')) {
            enhancedMessage = `Cannot connect to backend server at ${this.baseUrl}. Please check if the server is running.`;
            errorType = 'network';
        } else if (error.message.includes('CORS')) {
            enhancedMessage = `CORS error: Backend server needs to allow requests from ${window.location.origin}`;
            errorType = 'cors';
        } else if (error.message.includes('NetworkError')) {
            enhancedMessage = 'Network connection error. Please check your internet connection.';
            errorType = 'network';
        } else if (error.status === 500) {
            enhancedMessage = `Internal server error: ${error.message}`;
            errorType = 'server';
        } else if (error.status === 422) {
            enhancedMessage = `Validation error: ${error.message}`;
            errorType = 'validation';
        } else if (error.status === 404) {
            enhancedMessage = `API endpoint not found: ${endpoint}`;
            errorType = 'api';
        }
        
        const enhancedError = new Error(enhancedMessage);
        enhancedError.originalError = error;
        enhancedError.type = errorType;
        enhancedError.endpoint = endpoint;
        enhancedError.options = options;
        enhancedError.status = error.status;
        
        return enhancedError;
    }

    // Ana API metodları
    async researchIdeas(query, options = {}) {
        try {
            if (!query || typeof query !== 'string' || query.trim() === '') {
                throw new Error('Query parameter is required and must be a non-empty string');
            }

            const payload = {
                query: query.trim(),
                include_reddit: options.includeReddit ?? true,
                include_trends: options.includeTrends ?? true,
                include_competitors: options.includeCompetitors ?? true
            };

            if (CONFIG.DEBUG_MODE) {
                console.log('🔍 Research request payload:', payload);
            }

            const result = await this.makeRequest('/api/research', {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            // Validate response structure
            if (!result || typeof result !== 'object') {
                throw new Error('Invalid response format from research API');
            }

            return result;
        } catch (error) {
            console.error('❌ Research API Error:', error);
            throw error;
        }
    }

    async generateBusinessPlan(idea) {
        try {
            if (!idea || typeof idea !== 'object') {
                throw new Error('Idea parameter is required and must be an object');
            }

            // Validate required idea fields
            const requiredFields = ['title', 'description'];
            for (const field of requiredFields) {
                if (!idea[field] || typeof idea[field] !== 'string' || idea[field].trim() === '') {
                    throw new Error(`Idea.${field} is required and must be a non-empty string`);
                }
            }

            const payload = { idea: idea };

            if (CONFIG.DEBUG_MODE) {
                console.log('📊 Business plan request payload:', payload);
            }

            const result = await this.makeRequest('/api/business-plan', {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            // Validate response structure
            if (!result || typeof result !== 'object') {
                throw new Error('Invalid response format from business plan API');
            }

            return result;
        } catch (error) {
            console.error('❌ Business Plan API Error:', error);
            throw error;
        }
    }

    async healthCheck() {
        try {
            const result = await this.makeRequest('/');
            return result;
        } catch (error) {
            console.error('❌ Health Check Error:', error);
            throw error;
        }
    }

    async detailedHealthCheck() {
        try {
            const result = await this.makeRequest('/api/health');
            return result;
        } catch (error) {
            console.error('❌ Detailed Health Check Error:', error);
            throw error;
        }
    }

    async getCacheStats() {
        try {
            const result = await this.makeRequest('/api/cache-stats');
            return result;
        } catch (error) {
            console.error('❌ Cache Stats Error:', error);
            throw error;
        }
    }

    // Test connection method
    async testConnection() {
        try {
            if (CONFIG.DEBUG_MODE) {
                console.log('🔧 Testing backend connection...');
            }
            
            const response = await this.healthCheck();
            
            if (CONFIG.DEBUG_MODE) {
                console.log('✅ Backend connection successful:', response);
            }
            
            return { 
                status: 'connected', 
                response: response,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            if (CONFIG.DEBUG_MODE) {
                console.error('❌ Backend connection failed:', error);
            }
            
            return { 
                status: 'disconnected', 
                error: error.message,
                type: error.type,
                timestamp: new Date().toISOString()
            };
        }
    }

    // Performance metrics
    getPerformanceMetrics() {
        const avgTime = this.responseTimes.length > 0 
            ? Math.round(this.responseTimes.reduce((a, b) => a + b, 0) / this.responseTimes.length)
            : 0;
            
        return {
            totalRequests: this.requestCount,
            errorCount: this.errorCount,
            successCount: this.requestCount - this.errorCount,
            successRate: this.requestCount > 0 
                ? ((this.requestCount - this.errorCount) / this.requestCount * 100).toFixed(1) + '%' 
                : '0%',
            avgTime: avgTime,
            lastError: this.lastError?.message || null,
            connectionStatus: this.errorCount === this.requestCount ? 'disconnected' : 'connected'
        };
    }

    // Reset metrics
    resetMetrics() {
        this.requestCount = 0;
        this.errorCount = 0;
        this.responseTimes = [];
        this.lastError = null;
    }

    // Get debug info
    getDebugInfo() {
        return {
            baseUrl: this.baseUrl,
            timeout: this.timeout,
            metrics: this.getPerformanceMetrics(),
            lastError: this.lastError,
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
    }
}

// Singleton instance
export const api = new SaaSResearchAPI();

// Auto-test connection on load (in debug mode)
if (CONFIG.DEBUG_MODE) {
    setTimeout(async () => {
        const connectionTest = await api.testConnection();
        console.log('🔗 Initial connection test:', connectionTest);
    }, 1000);
}