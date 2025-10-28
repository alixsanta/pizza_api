/**
 * Application JavaScript pour la commande de pizzas
 */

// État de l'application
let currentStep = 1;
let customerInfo = {
    name: '',
    address: ''
};
let cart = [];
let currentOrderId = null;

// Menu de pizzas disponibles
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
        toppings: ['Tomate', 'Mozzarella', 'Légumes']
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

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('🍕 Application Pizza Delivery initialisée');
    
    // Gérer le passage à l'étape 2
    document.getElementById('continueToMenu').addEventListener('click', handleContinueToMenu);
    
    // Gérer la commande
    document.getElementById('placeOrder').addEventListener('click', handlePlaceOrder);
    
    // Gérer nouvelle commande
    document.getElementById('newOrder').addEventListener('click', handleNewOrder);
    
    // Afficher le menu
    displayPizzaMenu();
    
    // Mettre à jour l'interface
    updateStepIndicators();
});

/**
 * Affiche le menu des pizzas
 */
function displayPizzaMenu() {
    const menuContainer = document.getElementById('pizzaMenu');
    menuContainer.innerHTML = '';
    
    pizzaMenu.forEach((pizza, index) => {
        const pizzaCard = document.createElement('div');
        pizzaCard.className = 'pizza-card';
        pizzaCard.innerHTML = `
            <div class="pizza-icon">${pizza.icon}</div>
            <h3>${pizza.name}</h3>
            <div class="price">${pizza.price.toFixed(2)} EUR</div>
            <div class="toppings">${pizza.toppings.join(', ')}</div>
            <button class="btn btn-primary" onclick="addToCart(${index})">
                🛒 Ajouter au panier
            </button>
        `;
        menuContainer.appendChild(pizzaCard);
    });
}

/**
 * Ajoute une pizza au panier
 */
function addToCart(pizzaIndex) {
    const pizza = pizzaMenu[pizzaIndex];
    cart.push({...pizza});
    updateCart();
    showMessage('Pizza ajoutée au panier ! 🎉', 'success');
}

/**
 * Retire une pizza du panier
 */
function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
    showMessage('Pizza retirée du panier', 'info');
}

/**
 * Met à jour l'affichage du panier
 */
function updateCart() {
    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');
    const placeOrderButton = document.getElementById('placeOrder');
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="text-align: center; color: #7f8c8d;">Votre panier est vide</p>';
        cartTotalElement.textContent = '0.00';
        placeOrderButton.disabled = true;
    } else {
        cartItemsContainer.innerHTML = '';
        let total = 0;
        
        cart.forEach((pizza, index) => {
            total += pizza.price;
            
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <div class="cart-item-info">
                    <div class="cart-item-name">${pizza.icon} ${pizza.name}</div>
                    <div class="cart-item-details">${pizza.size} - ${pizza.toppings.join(', ')}</div>
                </div>
                <div class="cart-item-price">${pizza.price.toFixed(2)} EUR</div>
                <button class="remove-btn" onclick="removeFromCart(${index})">❌</button>
            `;
            cartItemsContainer.appendChild(cartItem);
        });
        
        cartTotalElement.textContent = total.toFixed(2);
        placeOrderButton.disabled = false;
    }
}

/**
 * Gère le passage à l'étape 2 (menu)
 */
function handleContinueToMenu() {
    const name = document.getElementById('customerName').value.trim();
    const address = document.getElementById('customerAddress').value.trim();
    
    if (!name || !address) {
        showMessage('⚠️ Veuillez remplir tous les champs', 'error');
        return;
    }
    
    customerInfo.name = name;
    customerInfo.address = address;
    
    goToStep(2);
    showMessage('Bienvenue ' + name + ' ! Choisissez vos pizzas 🍕', 'success');
}

/**
 * Gère la validation de la commande
 */
async function handlePlaceOrder() {
    if (cart.length === 0) {
        showMessage('⚠️ Votre panier est vide', 'error');
        return;
    }
    
    try {
        // 1. Créer la commande
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
        
        // 2. Ajouter les pizzas à la commande
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
        
        // 3. Mettre à jour le statut de la commande
        await fetch(`/orders/${currentOrderId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: 'preparing'
            })
        });
        
        // 4. Créer la livraison
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
        
        // 5. Afficher le récapitulatif
        displayOrderSummary();
        goToStep(3);
        
        showMessage('✅ Commande validée avec succès !', 'success');
        
        // 6. Démarrer le suivi de commande
        startOrderTracking();
        
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('❌ Erreur lors de la commande. Veuillez réessayer.', 'error');
    }
}

/**
 * Affiche le récapitulatif de commande
 */
function displayOrderSummary() {
    document.getElementById('orderIdDisplay').textContent = currentOrderId;
    document.getElementById('customerNameDisplay').textContent = customerInfo.name;
    document.getElementById('customerAddressDisplay').textContent = customerInfo.address;
    document.getElementById('pizzaCountDisplay').textContent = cart.length;
    
    const total = cart.reduce((sum, pizza) => sum + pizza.price, 0);
    document.getElementById('orderTotalDisplay').textContent = total.toFixed(2) + ' EUR';
}

/**
 * Démarre le suivi de commande
 */
function startOrderTracking() {
    const orderStatusElement = document.getElementById('orderStatus');
    const statuses = [
        { text: '👨‍🍳 Votre pizza est en préparation...', delay: 0 },
        { text: '🔥 Votre pizza est au four...', delay: 3000 },
        { text: '📦 Votre pizza est prête !', delay: 6000 },
        { text: '🚗 Votre livreur est en route !', delay: 9000 },
        { text: '🎉 Votre pizza est livrée ! Bon appétit !', delay: 12000 }
    ];
    
    statuses.forEach(status => {
        setTimeout(() => {
            orderStatusElement.textContent = status.text;
            orderStatusElement.classList.add('fade-in');
            
            if (status.delay === 12000) {
                // Afficher le bouton nouvelle commande
                document.getElementById('newOrder').classList.remove('hidden');
            }
        }, status.delay);
    });
}

/**
 * Gère une nouvelle commande
 */
function handleNewOrder() {
    currentStep = 1;
    customerInfo = { name: '', address: '' };
    cart = [];
    currentOrderId = null;
    
    // Réinitialiser les champs
    document.getElementById('customerName').value = '';
    document.getElementById('customerAddress').value = '';
    
    // Réinitialiser le panier
    updateCart();
    
    // Cacher le bouton nouvelle commande
    document.getElementById('newOrder').classList.add('hidden');
    
    // Retourner à l'étape 1
    goToStep(1);
    
    showMessage('✨ Prêt pour une nouvelle commande !', 'info');
}

/**
 * Change d'étape
 */
function goToStep(step) {
    currentStep = step;
    
    // Masquer toutes les étapes
    document.getElementById('step1').classList.add('hidden');
    document.getElementById('step2').classList.add('hidden');
    document.getElementById('step3').classList.add('hidden');
    
    // Afficher l'étape courante
    document.getElementById(`step${step}`).classList.remove('hidden');
    
    // Mettre à jour les indicateurs
    updateStepIndicators();
}

/**
 * Met à jour les indicateurs d'étape
 */
function updateStepIndicators() {
    const steps = document.querySelectorAll('.step');
    
    steps.forEach((stepElement, index) => {
        const stepNumber = index + 1;
        
        if (stepNumber < currentStep) {
            stepElement.classList.add('completed');
            stepElement.classList.remove('active');
        } else if (stepNumber === currentStep) {
            stepElement.classList.add('active');
            stepElement.classList.remove('completed');
        } else {
            stepElement.classList.remove('active', 'completed');
        }
    });
}

/**
 * Affiche un message
 */
function showMessage(text, type = 'info') {
    const messageContainer = document.getElementById('messageContainer');
    
    const message = document.createElement('div');
    message.className = `message ${type} fade-in`;
    message.textContent = text;
    
    messageContainer.appendChild(message);
    
    // Supprimer le message après 5 secondes
    setTimeout(() => {
        message.remove();
    }, 5000);
}

