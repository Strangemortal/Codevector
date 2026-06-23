/**
 * categories.js
 * -------------
 * Manages category filters and state selection on the directory interface.
 * Responsibilities:
 * 1. Fetches the active categories checklist from '/api/categories'.
 * 2. Renders selectable pills in the sidebar panel.
 * 3. Handles selection transitions and clears pagination cursors when the active category changes.
 */

window.fetchCategories = async function() {
    try {
        const res = await fetch('/api/categories');
        const categories = await res.json();
        const container = document.getElementById('categoryList');
        if (!container) return;
        
        const allPill = document.getElementById('cat-all');
        container.innerHTML = '';
        container.appendChild(allPill);
        
        categories.forEach(cat => {
            const pill = document.createElement('div');
            pill.className = `category-pill ${window.currentCategory === cat ? 'active' : ''}`;
            pill.id = `cat-${cat.replace(/\s+/g, '-')}`;
            pill.onclick = () => window.selectCategory(cat);
            pill.innerHTML = `
                <span>${cat}</span>
                <i data-lucide="chevron-right" size="16"></i>
            `;
            container.appendChild(pill);
        });
        
        if (window.lucide) {
            window.lucide.createIcons();
        }
    } catch (err) {
        console.error("Error loading categories", err);
    }
};

window.selectCategory = function(cat) {
    window.currentCategory = cat;
    
    document.querySelectorAll('.category-pill').forEach(pill => pill.classList.remove('active'));
    if (cat === null) {
        const allPill = document.getElementById('cat-all');
        if (allPill) allPill.classList.add('active');
    } else {
        const activePill = document.getElementById(`cat-${cat.replace(/\s+/g, '-')}`);
        if (activePill) activePill.classList.add('active');
    }
    
    window.currentCursor = null;
    window.nextCursor = null;
    window.prevCursor = null;
    
    if (window.fetchProducts) {
        window.fetchProducts();
    }
};
