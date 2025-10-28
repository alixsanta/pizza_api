/**
 * Pizza Express - Modern JavaScript Application
 */

// Application State
let currentStep = 1;
let customerInfo = {
    name: '',
    address: ''
};
let cart = [];
let currentOrderId = null;
let pizzaCatalog = []; // Catalogue chargé depuis l'API

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    console.log('🍕 Pizza Express initialized');

    // Event Listeners
    document.getElementById('continueToMenu').addEventListener('click', handleContinueToMenu);

    const placeOrderBtn = document.getElementById('placeOrder');
    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', handlePlaceOrder);
    }

    const newOrderBtn = document.getElementById('newOrder');
    if (newOrderBtn) {
        newOrderBtn.addEventListener('click', handleNewOrder);
    }

    // Cart Toggle
    const cartToggle = document.getElementById('cartToggle');
    if (cartToggle) {
        cartToggle.addEventListener('click', toggleCart);
    }

    // Back button
    const backBtn = document.getElementById('backToStep1');
    if (backBtn) {
        backBtn.addEventListener('click', () => goToStep(1));
    }

    // Load catalog and display menu
    loadPizzaCatalog();

    // Initialize cart
    updateCart();
});

/**
 * Load Pizza Catalog from API
 */
async function loadPizzaCatalog() {
    try {
        const response = await fetch('/pizzas/catalog');
        const data = await response.json();
        pizzaCatalog = data.catalog;
        console.log('📋 Catalogue chargé:', pizzaCatalog.length, 'types de pizzas');
        displayPizzaMenu();
    } catch (error) {
        console.error('❌ Erreur lors du chargement du catalogue:', error);
        showToast('Erreur lors du chargement du menu', 'error');
    }
}

/**
 * Display Pizza Menu with Size Selection
 */
function displayPizzaMenu() {
    const menuContainer = document.getElementById('pizzaMenu');
    if (!menuContainer) return;

    if (pizzaCatalog.length === 0) {
        menuContainer.innerHTML = '<p style="text-align: center; padding: 40px;">Chargement du menu...</p>';
        return;
    }

    menuContainer.innerHTML = '';

    // Icônes par type de pizza
    const icons = {
        'Margherita': '🍕',
        'Pepperoni': '🍕',
        'Végétarienne': '🥗',
        'Quatre Fromages': '🧀',
        'Calzone': '🥟',
        'Hawaïenne': '🍍',
        'Reine': '👑',
        'Savoyarde': '🏔️'
    };

    pizzaCatalog.forEach((pizza, index) => {
        const icon = icons[pizza.name] || '🍕';
        const pizzaCard = document.createElement('div');
        pizzaCard.className = 'pizza-card';
        pizzaCard.setAttribute('data-pizza-index', index);

        // Générer les options de taille
        const sizeOptions = pizza.sizes.map((size, sizeIndex) => `
            <label class="size-option ${sizeIndex === 1 ? 'selected' : ''}" data-size-index="${sizeIndex}">
                <input type="radio" name="size-${index}" value="${size.id}" ${sizeIndex === 1 ? 'checked' : ''}>
                <span class="size-label">${size.size}</span>
                <span class="size-price">${size.price.toFixed(2)} €</span>
            </label>
        `).join('');

        pizzaCard.innerHTML = `
            <div class="pizza-image">
                ${icon}
            </div>
            <div class="pizza-card-content">
                <h3 class="pizza-name">${pizza.name}</h3>
                <p class="pizza-toppings">${pizza.toppings.join(' • ')}</p>
                
                <div class="size-selector">
                    ${sizeOptions}
                </div>
                
                <button class="btn-add-cart" onclick="addToCartFromCatalog(${index})">
                    Ajouter
                </button>
            </div>
        `;

        menuContainer.appendChild(pizzaCard);

        // Gérer le changement de taille
        const sizeLabels = pizzaCard.querySelectorAll('.size-option');
        sizeLabels.forEach(label => {
            label.addEventListener('click', function() {
                sizeLabels.forEach(l => l.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    });
}

/**
 * Add Pizza to Cart from Catalog (with selected size)
 */
function addToCartFromCatalog(pizzaIndex) {
    const pizza = pizzaCatalog[pizzaIndex];
    const pizzaCard = document.querySelector(`[data-pizza-index="${pizzaIndex}"]`);
    const selectedSizeInput = pizzaCard.querySelector('input[type="radio"]:checked');

    if (!selectedSizeInput) {
        showToast('Veuillez sélectionner une taille', 'error');
        return;
    }

    const selectedSizeId = selectedSizeInput.value;
    const selectedSize = pizza.sizes.find(s => s.id === selectedSizeId);

    if (!selectedSize) {
        showToast('Erreur: taille non trouvée', 'error');
        return;
    }

    // Ajouter au panier avec l'ID de la pizza du catalogue
    cart.push({
        pizza_id: selectedSize.id,  // ID de la pizza en BDD
        name: pizza.name,
        size: selectedSize.size,
        price: selectedSize.price,
        toppings: pizza.toppings
    });

    updateCart();
    showToast(`${pizza.name} (${selectedSize.size}) ajoutée ! 🎉`, 'success');
}

/**
 * Remove from Cart
 */
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
    showToast('Pizza retirée du panier', 'info');
}

/**
 * Update Cart Display
 */
function updateCart() {
    const cartItemsContainer = document.getElementById('cartItems');
    const cartBadge = document.getElementById('cartBadge');
    const cartTotal = document.getElementById('cartTotal');
    const cartTotalWithDelivery = document.getElementById('cartTotalWithDelivery');
    const placeOrderButton = document.getElementById('placeOrder');

    // Update badge
    if (cartBadge) {
        cartBadge.textContent = cart.length;
    }

    if (!cartItemsContainer) return;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="empty-cart">
                <span class="empty-icon">🛒</span>
                <p>Votre panier est vide</p>
            </div>
        `;
        if (cartTotal) cartTotal.textContent = '0.00 €';
        if (cartTotalWithDelivery) cartTotalWithDelivery.textContent = '2.50 €';
        if (placeOrderButton) placeOrderButton.disabled = true;
    } else {
        cartItemsContainer.innerHTML = '';
        let total = 0;

        cart.forEach((pizza, index) => {
            total += pizza.price;

            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-icon">${pizza.icon}</div>
                <div class="cart-item-details">
                    <div class="cart-item-name">${pizza.name}</div>
                    <div class="cart-item-info">${pizza.size} • ${pizza.toppings.slice(0, 2).join(', ')}</div>
                    <div class="cart-item-price">${pizza.price.toFixed(2)} €</div>
                </div>
                <button class="btn-remove" onclick="removeFromCart(${index})">✕</button>
            `;
            cartItemsContainer.appendChild(cartItem);
        });

        if (cartTotal) cartTotal.textContent = total.toFixed(2) + ' €';
        if (cartTotalWithDelivery) cartTotalWithDelivery.textContent = (total + 2.50).toFixed(2) + ' €';
        if (placeOrderButton) placeOrderButton.disabled = false;
    }
}

/**
 * Toggle Cart Visibility
 */
function toggleCart() {
    const cartContent = document.getElementById('cartContent');
    const cartToggleIcon = document.getElementById('cartToggleIcon');

    if (!cartContent || !cartToggleIcon) return;

    if (cartContent.style.display === 'none') {
        cartContent.style.display = 'flex';
        cartToggleIcon.textContent = '▼';
    } else {
        cartContent.style.display = 'none';
        cartToggleIcon.textContent = '▲';
    }
}

/**
 * Handle Continue to Menu
 */
function handleContinueToMenu() {
    const name = document.getElementById('customerName').value.trim();
    const address = document.getElementById('customerAddress').value.trim();

    if (!name || !address) {
        showToast('Veuillez remplir tous les champs', 'error');
        return;
    }

    customerInfo.name = name;
    customerInfo.address = address;

    goToStep(2);
    showToast(`Bienvenue ${name} ! 👋`, 'success');
}

/**
 * Handle Place Order
 */
async function handlePlaceOrder() {
    if (cart.length === 0) {
        showToast('Votre panier est vide', 'error');
        return;
    }

    try {
        showToast('Préparation de votre commande...', 'info');

        // 1. Create Order
        const orderResponse = await fetch('/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                customer_name: customerInfo.name,
                customer_address: customerInfo.address
            })
        });

        if (!orderResponse.ok) {
            throw new Error('Erreur lors de la création de la commande');
        }

        const order = await orderResponse.json();
        currentOrderId = order.order_id;

        // 2. Add Pizzas to Order (using pizza_id from catalog)
        for (const pizza of cart) {
            const addPizzaResponse = await fetch(`/orders/${currentOrderId}/pizzas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    pizza_id: pizza.pizza_id  // ID de la pizza du catalogue
                })
            });

            if (!addPizzaResponse.ok) {
                throw new Error('Erreur lors de l\'ajout d\'une pizza');
            }
        }

        // 3. Update Order Status
        await fetch(`/orders/${currentOrderId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: 'preparing'
            })
        });

        // 4. Create Delivery
        await fetch('/deliveries', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                order_id: currentOrderId,
                driver_name: 'Mario 🚗'
            })
        });

        // 5. Display Order Summary
        displayOrderSummary();
        goToStep(3);

        showToast('Commande validée avec succès ! 🎉', 'success');

        // 6. Start Order Tracking
        startOrderTracking();

    } catch (error) {
        console.error('Erreur:', error);
        showToast('Erreur lors de la commande. Veuillez réessayer.', 'error');
    }
}

/**
 * Display Order Summary
 */
function displayOrderSummary() {
    document.getElementById('orderIdDisplay').textContent = currentOrderId.substring(0, 8);
    document.getElementById('customerNameDisplay').textContent = customerInfo.name;
    document.getElementById('customerAddressDisplay').textContent = customerInfo.address;
    document.getElementById('pizzaCountDisplay').textContent = cart.length;

    const total = cart.reduce((sum, pizza) => sum + pizza.price, 0) + 2.50;
    document.getElementById('orderTotalDisplay').textContent = total.toFixed(2) + ' €';
}

/**
 * Start Order Tracking
 */
function startOrderTracking() {
    const orderStatusElement = document.getElementById('orderStatus');

    const statuses = [
        {
            text: 'Votre commande est en préparation',
            timeline: 'timeline-preparing',
            delay: 0
        },
        {
            text: 'Votre pizza est au four 🔥',
            timeline: 'timeline-preparing',
            delay: 3000
        },
        {
            text: 'Votre commande est prête',
            timeline: 'timeline-delivery',
            delay: 6000
        },
        {
            text: 'Mario est en route vers vous 🚗',
            timeline: 'timeline-delivery',
            delay: 9000
        },
        {
            text: 'Livraison réussie ! Bon appétit 🎉',
            timeline: 'timeline-delivered',
            delay: 12000
        }
    ];

    statuses.forEach(status => {
        setTimeout(() => {
            if (orderStatusElement) {
                orderStatusElement.textContent = status.text;
            }

            // Update timeline
            const timelineItem = document.getElementById(status.timeline);
            if (timelineItem) {
                timelineItem.classList.add('active');
            }

            if (status.delay === 12000) {
                const newOrderBtn = document.getElementById('newOrder');
                if (newOrderBtn) {
                    newOrderBtn.classList.remove('hidden');
                }
            }
        }, status.delay);
    });
}

/**
 * Handle New Order
 */
function handleNewOrder() {
    currentStep = 1;
    customerInfo = { name: '', address: '' };
    cart = [];
    currentOrderId = null;

    // Reset fields
    document.getElementById('customerName').value = '';
    document.getElementById('customerAddress').value = '';

    // Reset cart
    updateCart();

    // Hide new order button
    const newOrderBtn = document.getElementById('newOrder');
    if (newOrderBtn) {
        newOrderBtn.classList.add('hidden');
    }

    // Reset timeline
    document.querySelectorAll('.timeline-item').forEach(item => {
        item.classList.remove('active');
    });
    const firstTimeline = document.querySelector('.timeline-item');
    if (firstTimeline) {
        firstTimeline.classList.add('active');
    }

    // Go to step 1
    goToStep(1);

    showToast('Prêt pour une nouvelle commande ! ✨', 'info');
}

/**
 * Go to Step
 */
function goToStep(step) {
    currentStep = step;

    console.log('Going to step:', step);

    // Hide all steps
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');

    if (step1) step1.classList.add('hidden');
    if (step2) step2.classList.add('hidden');
    if (step3) step3.classList.add('hidden');

    // Show current step
    const currentStepElement = document.getElementById(`step${step}`);
    if (currentStepElement) {
        currentStepElement.classList.remove('hidden');
    }

    // Update nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Show Toast Message
 */
function showToast(text, type = 'info') {
    const messageContainer = document.getElementById('messageContainer');
    if (!messageContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = text;

    messageContainer.appendChild(toast);

    // Remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

