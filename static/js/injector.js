/**
 * injector.js
 * -----------
 * Manages UI interactions with the product injection form simulator.
 * Responsibilities:
 * 1. Collects name, category, and price details from the simulation form.
 * 2. dispatches POST creation requests to '/api/products'.
 * 3. Triggers success toast notifications with details of the inserted product.
 * 4. Automatically refreshes page 1 listings to visualize the newly added item instantly.
 */

window.injectProduct = async function() {
    const nameInput = document.getElementById('simName');
    const categorySelect = document.getElementById('simCategory');
    const priceInput = document.getElementById('simPrice');
    const injectBtn = document.getElementById('injectBtn');
    if (!nameInput || !categorySelect || !priceInput || !injectBtn) return;

    const name = nameInput.value.trim() || `Injected Custom Gadget #${Math.floor(Math.random() * 10000)}`;
    const category = categorySelect.value;
    const price = parseFloat(priceInput.value) || 29.99;

    injectBtn.disabled = true;
    const originalContent = injectBtn.innerHTML;
    injectBtn.innerText = "Injecting...";

    try {
        const res = await fetch(`/api/products?name=${encodeURIComponent(name)}&category=${encodeURIComponent(category)}&price=${price}`, {
            method: 'POST'
        });
        const product = await res.json();
        
        if (window.showToast) {
            window.showToast(`Product Injected: ${product.name} (ID: ${product.id})`);
        }
        
        nameInput.value = '';
        
        if (!window.currentCursor && (!window.currentCategory || window.currentCategory === category)) {
            if (window.fetchProducts) {
                window.fetchProducts();
            }
        }
    } catch (err) {
        console.error("Failed to inject product", err);
        if (window.showToast) {
            window.showToast("Failed to inject product", true);
        }
    } finally {
        injectBtn.disabled = false;
        injectBtn.innerHTML = originalContent;
        if (window.lucide) {
            window.lucide.createIcons();
        }
    }
};
