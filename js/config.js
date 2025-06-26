// js/config.js - Basitleştirilmiş konfigürasyon
// Artık API anahtarları backend'de, frontend sadece URL'leri biliyor

// Backend konfigürasyonu
export const backendConfig = {
    url: 'http://127.0.0.1:8000',
    timeout: 30000, // 30 saniye
    retries: 3
};

// Development vs Production ayarları
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1';

if (isDevelopment) {
    console.log('🔧 Development mode detected');
    console.log('🔗 Backend URL:', backendConfig.url);
} else {
    // Production'da backend URL'yi değiştir
    backendConfig.url = 'https://your-production-backend.com';
    console.log('🚀 Production mode');
}

// Debug ayarları
export const debugConfig = {
    enabled: isDevelopment || window.location.search.includes('debug=true'),
    logLevel: isDevelopment ? 'debug' : 'error'
};

// UI ayarları
export const uiConfig = {
    animationSpeed: 'normal', // 'fast', 'normal', 'slow'
    showCacheStats: isDevelopment,
    showBackendStatus: true,
    autoHealthCheck: true,
    healthCheckInterval: 60000 // 1 dakika
};

// Hata mesajları
export const errorMessages = {
    backendDown: '❌ Backend sunucusu çalışmıyor!\n\nLütfen terminal\'de "python backend.py" komutunu çalıştırın.',
    rateLimit: '⏳ Çok fazla istek gönderdiniz. Lütfen 1-2 dakika bekleyin.',
    timeout: '⏰ İstek zaman aşımına uğradı. İnternet bağlantınızı kontrol edin.',
    serverError: '🔧 Sunucu hatası. API anahtarlarını kontrol edin.',
    invalidInput: '⚠️ Geçersiz giriş. Lütfen girişinizi kontrol edin.',
    unauthorized: '🔑 Yetkilendirme hatası. API anahtarları geçersiz.',
    networkError: '🌐 Ağ bağlantı hatası. İnternet bağlantınızı kontrol edin.'
};

// Feature flags (gelecekteki özellikler için)
export const features = {
    enableCaching: true,
    enableRealTimeUpdates: false,
    enableAdvancedFilters: false,
    enableExportFeature: false,
    enableCollaboration: false
};

// Export everything as default for easier import
export default {
    backend: backendConfig,
    debug: debugConfig,
    ui: uiConfig,
    errors: errorMessages,
    features
};

// Debugging için global erişim
if (debugConfig.enabled) {
    window.appConfig = {
        backend: backendConfig,
        debug: debugConfig,
        ui: uiConfig,
        errors: errorMessages,
        features
    };
    
    console.log('🐛 Config loaded in debug mode:', window.appConfig);
}