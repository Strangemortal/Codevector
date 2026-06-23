/**
 * products.js
 * -----------
 * Coordinates the product catalog feed, skeleton loads, and keyset-based page transitions.
 * Responsibilities:
 * 1. Fetches item sets from '/api/products' using category and cursor parameters.
 * 2. Visualizes skeleton load placeholder states during transit.
 * 3. Decodes and displays active keyset cursor timestamps for execution tracing.
 * 4. Enables/disables pagination buttons and renders grid cards representing products.
 */

window.fetchProducts = async function(cursorStr = null) {
    const grid = document.getElementById('productGrid');
    if (!grid) return;
    
    grid.innerHTML = Array(8).fill(0).map(() => 
        `<div class="product-card skeleton" style="height: 180px;"></div>`
    ).join('');

    let url = `/api/products?limit=12`;
    if (window.currentCategory) {
        url += `&category=${encodeURIComponent(window.currentCategory)}`;
    }
    if (cursorStr) {
        url += `&cursor=${cursorStr}`;
    }

    try {
        const startTime = performance.now();
        const res = await fetch(url);
        const data = await res.json();
        const duration = (performance.now() - startTime).toFixed(1);

        window.nextCursor = data.next_cursor;
        window.prevCursor = data.prev_cursor;
        window.currentCursor = cursorStr;

        const infoPanel = document.getElementById('cursorInfo');
        if (infoPanel) {
            let cursorLabel = 'First Page (no cursor)';
            if (cursorStr) {
                try {
                    const decoded = atob(cursorStr.replace(/-/g, '+').replace(/_/g, '/'));
                    cursorLabel = `Cursor: ${decoded}`;
                } catch (e) {
                    cursorLabel = `Cursor: ${cursorStr.substring(0, 10)}...`;
                }
            }
            infoPanel.innerHTML = `<i data-lucide="database"></i> ${cursorLabel} <span style="opacity: 0.6; margin-left: 8px;">(${duration}ms)</span>`;
        }

        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        if (prevBtn) prevBtn.disabled = !window.prevCursor;
        if (nextBtn) nextBtn.disabled = !window.nextCursor;

        grid.innerHTML = '';
        if (data.items.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <i data-lucide="inbox" size="48" style="margin-bottom: 1rem;"></i>
                    <p>No products found matching these filters.</p>
                </div>
            `;
        } else {
            data.items.forEach(p => {
                const card = document.createElement('div');
                card.className = 'product-card';
                
                const date = new Date(p.created_at);
                const formattedTime = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
                const formattedDate = date.toLocaleDateString([], {month: 'short', day: 'numeric'});

                card.innerHTML = `
                    <div class="product-meta">
                        <div class="product-category">${p.category}</div>
                        <div class="product-name">${p.name}</div>
                    </div>
                    <div class="product-details">
                        <div class="product-price">$${p.price.toFixed(2)}</div>
                        <div class="product-time">
                            ${formattedDate}<br/>
                            <span style="opacity: 0.6;">${formattedTime}</span><br/>
                            <span style="font-size: 0.6rem; opacity: 0.4;">ID: ${p.id}</span>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
        
        if (window.lucide) {
            window.lucide.createIcons();
        }
    } catch (err) {
        console.error("Error loading products", err);
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: #ef4444;">
                <i data-lucide="alert-triangle" size="48" style="margin-bottom: 1rem;"></i>
                <p>Error loading products. Make sure the database is seeded.</p>
            </div>
        `;
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }
};

window.navigate = function(direction) {
    if (direction === 'next' && window.nextCursor) {
        window.fetchProducts(window.nextCursor);
    } else if (direction === 'prev' && window.prevCursor) {
        window.fetchProducts(window.prevCursor);
    }
};
