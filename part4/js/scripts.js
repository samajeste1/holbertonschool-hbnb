/**
 * Main JavaScript file for HBnB Web Client
 * Handles authentication, API interactions, and DOM manipulation
 */

// Utility function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Utility function to set cookie
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

// Check if user is authenticated
function isAuthenticated() {
    return getCookie('token') !== null;
}

// Get authentication token
function getAuthToken() {
    return getCookie('token');
}

// API base URL - Update this with your API URL
const API_BASE_URL = 'http://localhost:5000/api/v1';

// Make authenticated API request
async function apiRequest(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });
    
    if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
    }
    
    return response.json();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication and update UI accordingly
    checkAuthentication();
    
    // Initialize page-specific functionality
    if (document.getElementById('login-form')) {
        initLogin();
    }
    
    if (document.getElementById('places-list')) {
        initPlacesList();
    }
    
    if (document.getElementById('place-details')) {
        initPlaceDetails();
    }
    
    if (document.getElementById('review-form')) {
        initReviewForm();
    }
});

// Check authentication status
function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    const loginButton = document.querySelector('.login-button');
    
    if (isAuthenticated()) {
        if (loginLink) loginLink.style.display = 'none';
        if (loginButton) loginButton.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (loginButton) loginButton.style.display = 'block';
    }
}

// Initialize login functionality
function initLogin() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token);
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed. Please check your credentials.');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login.');
            }
        });
    }
}

// Initialize places list
function initPlacesList() {
    if (isAuthenticated()) {
        fetchPlaces();
    }
    
    // Initialize price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
    }
}

// Fetch places from API
async function fetchPlaces() {
    try {
        const places = await apiRequest('/places/');
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Display places in the list
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesList.appendChild(placeCard);
    });
}

// Create a place card element
function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = `
        <h3>${place.name || 'Unnamed Place'}</h3>
        <p>Price per night: $${place.price || 'N/A'}</p>
        <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
    `;
    return card;
}

// Filter places by price
function filterPlacesByPrice(event) {
    const maxPrice = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const priceText = card.querySelector('p').textContent;
        const price = parseInt(priceText.match(/\d+/)?.[0] || '0');
        
        if (maxPrice === 'All' || price <= parseInt(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// View place details
function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

// Initialize place details page
function initPlaceDetails() {
    const placeId = getPlaceIdFromURL();
    if (placeId && isAuthenticated()) {
        fetchPlaceDetails(placeId);
    }
}

// Get place ID from URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// Fetch place details from API
async function fetchPlaceDetails(placeId) {
    try {
        const place = await apiRequest(`/places/${placeId}`);
        displayPlaceDetails(place);
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// Display place details
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;
    
    placeDetails.innerHTML = `
        <div class="place-info">
            <h2>${place.name || 'Unnamed Place'}</h2>
            <p><strong>Price:</strong> $${place.price || 'N/A'} per night</p>
            <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
            <p><strong>Host:</strong> ${place.owner?.first_name || ''} ${place.owner?.last_name || ''}</p>
        </div>
        <div class="amenities">
            <h3>Amenities</h3>
            <ul id="amenities-list"></ul>
        </div>
        <div class="reviews">
            <h3>Reviews</h3>
            <div id="reviews-list"></div>
        </div>
    `;
    
    // Display amenities
    if (place.amenities) {
        const amenitiesList = document.getElementById('amenities-list');
        place.amenities.forEach(amenity => {
            const li = document.createElement('li');
            li.textContent = amenity.name;
            amenitiesList.appendChild(li);
        });
    }
    
    // Display reviews
    if (place.reviews) {
        const reviewsList = document.getElementById('reviews-list');
        place.reviews.forEach(review => {
            const reviewCard = createReviewCard(review);
            reviewsList.appendChild(reviewCard);
        });
    }
    
    // Show add review form if authenticated
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection && isAuthenticated()) {
        addReviewSection.style.display = 'block';
    }
}

// Create a review card element
function createReviewCard(review) {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
        <p><strong>${review.user?.first_name || ''} ${review.user?.last_name || ''}</strong></p>
        <p>${review.text || 'No text'}</p>
        <p>Rating: ${review.rating || 'N/A'}</p>
    `;
    return card;
}

// Initialize review form
function initReviewForm() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }
    
    const reviewForm = document.getElementById('review-form');
    const placeId = getPlaceIdFromURL();
    
    if (reviewForm && placeId) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const text = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;
            
            try {
                await apiRequest('/reviews/', {
                    method: 'POST',
                    body: JSON.stringify({
                        text,
                        rating: parseInt(rating),
                        place_id: placeId
                    })
                });
                
                alert('Review submitted successfully!');
                reviewForm.reset();
                window.location.href = `place.html?id=${placeId}`;
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('Failed to submit review. Please try again.');
            }
        });
    }
}



