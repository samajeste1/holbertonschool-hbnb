/**
 * HBnB Web Client - Main JavaScript
 * Handles authentication, API interactions, and dynamic page content
 */

// API Base URL - Update this to match your API server
const API_BASE_URL = 'http://localhost:5000/api/v1';

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get a cookie value by name
 * @param {string} name - The cookie name
 * @returns {string|null} - The cookie value or null if not found
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

/**
 * Set a cookie
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Days until expiration (default: 7)
 */
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

/**
 * Delete a cookie by name
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
}

/**
 * Check if user is authenticated
 * @returns {boolean} - True if authenticated
 */
function isAuthenticated() {
    return getCookie('token') !== null;
}

/**
 * Get the authentication token
 * @returns {string|null} - The JWT token or null
 */
function getToken() {
    return getCookie('token');
}

/**
 * Get place ID from URL query parameters
 * @returns {string|null} - The place ID or null
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// ============================================
// AUTHENTICATION HANDLING
// ============================================

/**
 * Check authentication status and update UI accordingly
 */
function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');

    if (token) {
        // User is authenticated - hide login link
        if (loginLink) {
            loginLink.style.display = 'none';
        }
    } else {
        // User is not authenticated - show login link
        if (loginLink) {
            loginLink.style.display = 'block';
        }
    }

    return token;
}

// ============================================
// LOGIN PAGE FUNCTIONS
// ============================================

/**
 * Initialize the login page
 */
function initLoginPage() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }

            await loginUser(email, password);
        });
    }
}

/**
 * Login user via API
 * @param {string} email - User email
 * @param {string} password - User password
 */
async function loginUser(email, password) {
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
            // Store JWT token in cookie
            document.cookie = `token=${data.access_token}; path=/`;
            // Redirect to main page
            window.location.href = 'index.html';
        } else {
            const error = await response.json().catch(() => ({}));
            alert('Login failed: ' + (error.message || error.error || 'Invalid credentials'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

// ============================================
// INDEX PAGE FUNCTIONS
// ============================================

/**
 * Initialize the index page (list of places)
 */
function initIndexPage() {
    const token = checkAuthentication();

    // Fetch and display places
    fetchPlaces(token);

    // Initialize price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
    }
}

/**
 * Fetch places from the API
 * @param {string|null} token - JWT token for authentication
 */
async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            // Display empty state or error message
            const placesList = document.getElementById('places-list');
            if (placesList) {
                placesList.innerHTML = '<p>Unable to load places. Please try again later.</p>';
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<p>Unable to load places. Please try again later.</p>';
        }
    }
}

/**
 * Display places in the places list
 * @param {Array} places - Array of place objects
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    // Clear current content
    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    // Create place cards
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price || 0);

        placeCard.innerHTML = `
            <h3>${place.title || place.name || 'Unnamed Place'}</h3>
            <p class="price">$${place.price || 'N/A'} per night</p>
            <p>${place.description ? place.description.substring(0, 100) + '...' : 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

/**
 * Filter places by selected price
 * @param {Event} event - Change event from price filter
 */
function filterPlacesByPrice(event) {
    const selectedPrice = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseInt(card.getAttribute('data-price')) || 0;

        if (selectedPrice === 'all' || price <= parseInt(selectedPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================
// PLACE DETAILS PAGE FUNCTIONS
// ============================================

/**
 * Initialize the place details page
 */
function initPlacePage() {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = '<p>Place ID not found in URL.</p>';
        }
        return;
    }

    // Show/hide add review section based on authentication
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block';
            // Initialize review form for this page
            initReviewFormOnPlacePage(token, placeId);
        } else {
            addReviewSection.style.display = 'none';
        }
    }

    // Fetch and display place details
    fetchPlaceDetails(token, placeId);
}

/**
 * Fetch place details from the API
 * @param {string|null} token - JWT token
 * @param {string} placeId - Place ID
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            const placeDetails = document.getElementById('place-details');
            if (placeDetails) {
                placeDetails.innerHTML = '<p>Unable to load place details.</p>';
            }
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = '<p>Unable to load place details.</p>';
        }
    }
}

/**
 * Display place details on the page
 * @param {Object} place - Place object
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    // Build host name
    const hostName = place.owner
        ? `${place.owner.first_name || ''} ${place.owner.last_name || ''}`.trim() || 'Unknown'
        : (place.host || 'Unknown');

    // Build amenities list
    let amenitiesHtml = '';
    if (place.amenities && place.amenities.length > 0) {
        const amenityItems = place.amenities.map(a =>
            `<li>${typeof a === 'string' ? a : (a.name || 'Unknown')}</li>`
        ).join('');
        amenitiesHtml = `
            <div class="amenities">
                <h4>Amenities</h4>
                <ul>${amenityItems}</ul>
            </div>
        `;
    }

    // Display place info
    placeDetails.innerHTML = `
        <div class="place-info">
            <h2>${place.title || place.name || 'Unnamed Place'}</h2>
            <p><strong>Host:</strong> ${hostName}</p>
            <p><strong>Price:</strong> $${place.price || 'N/A'} per night</p>
            <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
            ${amenitiesHtml}
        </div>
    `;

    // Display reviews
    displayReviews(place.reviews);
}

/**
 * Display reviews for a place
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    // Keep the header
    reviewsSection.innerHTML = '<h3>Reviews</h3>';

    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';

        // Build user name
        const userName = review.user
            ? `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim() || 'Anonymous'
            : (review.user_name || 'Anonymous');

        reviewCard.innerHTML = `
            <p><strong>${userName}</strong></p>
            <p>${review.text || review.comment || 'No comment'}</p>
            <p class="rating">Rating: ${review.rating || 'N/A'}/5</p>
        `;

        reviewsSection.appendChild(reviewCard);
    });
}

/**
 * Initialize review form on the place details page
 * @param {string} token - JWT token
 * @param {string} placeId - Place ID
 */
function initReviewFormOnPlacePage(token, placeId) {
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value.trim();
            const rating = document.getElementById('review-rating').value;

            if (!reviewText || !rating) {
                alert('Please fill in both review and rating.');
                return;
            }

            await submitReview(token, placeId, reviewText, parseInt(rating));
        });
    }
}

// ============================================
// ADD REVIEW PAGE FUNCTIONS
// ============================================

/**
 * Initialize the add review page
 */
function initAddReviewPage() {
    const token = checkAuthentication();

    // Redirect to index if not authenticated
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        alert('Place ID not found in URL.');
        window.location.href = 'index.html';
        return;
    }

    // Fetch place name to display
    fetchPlaceNameForReview(token, placeId);

    // Setup form submission
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (!reviewText || !rating) {
                alert('Please fill in both review and rating.');
                return;
            }

            await submitReview(token, placeId, reviewText, parseInt(rating));
        });
    }
}

/**
 * Fetch place name to display on add review page
 * @param {string} token - JWT token
 * @param {string} placeId - Place ID
 */
async function fetchPlaceNameForReview(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            const placeNameElement = document.getElementById('place-name');
            if (placeNameElement) {
                placeNameElement.textContent = place.title || place.name || 'Unknown Place';
            }
        }
    } catch (error) {
        console.error('Error fetching place name:', error);
    }
}

/**
 * Submit a review to the API
 * @param {string} token - JWT token
 * @param {string} placeId - Place ID
 * @param {string} reviewText - Review text
 * @param {number} rating - Rating (1-5)
 */
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: rating,
                place_id: placeId
            })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
            // Redirect back to place details
            window.location.href = `place.html?id=${placeId}`;
        } else {
            const error = await response.json().catch(() => ({}));
            alert('Failed to submit review: ' + (error.message || error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting your review.');
    }
}

// ============================================
// PAGE INITIALIZATION
// ============================================

/**
 * Main initialization - runs when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    // Determine which page we're on and initialize accordingly
    if (path.endsWith('login.html')) {
        initLoginPage();
    } else if (path.endsWith('place.html')) {
        initPlacePage();
    } else if (path.endsWith('add_review.html')) {
        initAddReviewPage();
    } else if (path.endsWith('index.html') || path.endsWith('/') || path === '') {
        initIndexPage();
    }
});
