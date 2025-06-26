
export class BackendStatusManager {
    static show(status, message = '') {
        const existingStatus = document.querySelector('.backend-status');
        if (existingStatus) existingStatus.remove();
        
        const statusElement = document.createElement('div');
        statusElement.className = 'backend-status flex items-center justify-center gap-2 text-sm py-2 px-4 rounded-lg mx-auto mt-4 max-w-md';
        
        if (status === 'connected') {
            statusElement.className += ' bg-green-900/30 border border-green-700 text-green-300';
            statusElement.innerHTML = `
                <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>Backend Connected</span>
                ${message ? `<span class="text-xs opacity-75">- ${message}</span>` : ''}
            `;
        } else {
            statusElement.className += ' bg-red-900/30 border border-red-700 text-red-300';
            statusElement.innerHTML = `
                <div class="w-2 h-2 bg-red-400 rounded-full"></div>
                <span>Backend Disconnected</span>
            `;
        }
        
        const header = document.querySelector('header');
        if (header) {
            header.appendChild(statusElement);
            
            if (status === 'connected') {
                setTimeout(() => {
                    if (statusElement.parentNode) {
                        statusElement.remove();
                    }
                }, 5000);
            }
        }
    }
}