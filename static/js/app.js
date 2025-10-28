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

// Pizza Menu
const pizzaMenu = [
    {
        name: 'Margherita',
        icon: '🍕',
        size: 'Medium',
        price: 9.99,
        toppings: ['Tomate', 'Mozzarella', 'Basilic']
    },
    {
        name: 'Pepperoni',
        icon: '🍕',
        size: 'Medium',
        price: 11.99,
        toppings: ['Tomate', 'Mozzarella', 'Pepperoni']
    },
    {
        name: 'Végétarienne',
        icon: '🥗',
        size: 'Medium',
        price: 10.99,
        toppings: ['Tomate', 'Mozzarella', 'Légumes frais']
    },
    {
        name: 'Quatre Fromages',
        icon: '🧀',
        size: 'Medium',
        price: 12.99,
        toppings: ['Mozzarella', 'Gorgonzola', 'Parmesan', 'Chèvre']
    },
    {
        name: 'Calzone',
        icon: '🥟',
        size: 'Large',
        price: 13.99,
        toppings: ['Tomate', 'Mozzarella', 'Jambon', 'Champignons']
    },
    {
        name: 'Hawaïenne',
        icon: '🍍',
        size: 'Medium',
        price: 11.49,
        toppings: ['Tomate', 'Mozzarella', 'Jambon', 'Ananas']
    }
];

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

    // Display Menu
    displayPizzaMenu();

    // Initialize cart
    updateCart();
});

/**
 * Display Pizza Menu
 */
function displayPizzaMenu() {
    const menuContainer = document.getElementById('pizzaMenu');
    if (!menuContainer) return;

    menuContainer.innerHTML = '';

    pizzaMenu.forEach((pizza, index) => {
        const pizzaCard = document.createElement('div');
        pizzaCard.className = 'pizza-card';
        pizzaCard.innerHTML = `
            <div class="pizza-image">
                ${pizza.icon}
            </div>
            <div class="pizza-card-content">
                <h3 class="pizza-name">${pizza.name}</h3>
                <p class="pizza-toppings">${pizza.toppings.join(' • ')}</p>
                <div class="pizza-footer">
                    <span class="pizza-price">${pizza.price.toFixed(2)} €</span>
                    <button class="btn-add-cart" onclick="addToCart(${index})">
                        Ajouter
                    </button>
                </div>
            </div>
        `;
        menuContainer.appendChild(pizzaCard);
    });
}

/**
 * Add Pizza to Cart
 */
function addToCart(pizzaIndex) {
    const pizza = pizzaMenu[pizzaIndex];
    cart.push({...pizza});
    updateCart();
    showToast('Pizza ajoutée au panier !', 'success');
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

        // 2. Add Pizzas to Order
        for (const pizza of cart) {
            await fetch(`/orders/${currentOrderId}/pizzas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: pizza.name,
                    size: pizza.size,
                    price: pizza.price,
                    toppings: pizza.toppings
                })
            });
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

