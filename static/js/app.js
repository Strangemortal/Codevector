/**
 * app.js
 * ------
 * Serves as the main entry point and global state coordinator for the client.
 * Responsibilities:
 * 1. Declares shared state variables on the window object (cursors and category filters).
 * 2. Hooks into the DOMContentLoaded event to bootstrap lucide icons and trigger initial data loads.
 */

window.currentCategory = null;
window.nextCursor = null;
window.prevCursor = null;
window.currentCursor = null;

window.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }
    
    if (window.fetchCategories) {
        window.fetchCategories();
    }
    if (window.fetchProducts) {
        window.fetchProducts();
    }
});
