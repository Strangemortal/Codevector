/**
 * toasts.js
 * ---------
 * Manages the display and life cycle of transient toast notifications.
 * Responsibilities:
 * 1. Creates containerized HTML notification elements dynamically.
 * 2. Formats warning/success theme states.
 * 3. Instructs Lucide to bind appropriate vector icons.
 * 4. Schedules element cleanups/destructions after 4 seconds.
 */

window.showToast = function(message, isError = false) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    if (isError) {
        toast.style.background = '#ef4444';
        toast.style.borderLeftColor = '#b91c1c';
    }
    
    toast.innerHTML = `
        <i data-lucide="${isError ? 'alert-circle' : 'check-circle'}"></i>
        <span>${message}</span>
    `;
    container.appendChild(toast);
    
    if (window.lucide) {
        window.lucide.createIcons();
    }

    setTimeout(() => {
        toast.remove();
    }, 4000);
};
