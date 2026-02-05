/**
 * HBnB Web Client - Main JavaScript
 * Client Web HBnB - JavaScript Principal
 *
 * Ce fichier gere toute la logique JavaScript du frontend :
 * - Authentification des utilisateurs avec JWT
 * - Interactions avec l'API REST
 * - Generation dynamique du contenu HTML
 * - Gestion des formulaires
 * - Filtrage des lieux par prix
 */

// ============================================
// CONFIGURATION DE L'API
// ============================================

// URL de base de l'API - A modifier selon l'adresse du serveur backend
// Par defaut pointe vers le serveur part3 sur le port 5001
const API_BASE_URL = 'http://localhost:5001/api/v1';
// const API_BASE_URL : constante globale accessible partout dans le code
// 'http://localhost:5001/api/v1' : chemin vers l'API REST avec versioning v1

// ============================================
// FONCTIONS UTILITAIRES - GESTION DES COOKIES
// ============================================
// Les cookies permettent de stocker le token JWT cote client
// Le token persiste meme apres fermeture du navigateur

/**
 * Recupere la valeur d'un cookie par son nom
 * @param {string} name - Le nom du cookie a rechercher
 * @returns {string|null} - La valeur du cookie ou null si non trouve
 *
 * Exemple: getCookie('token') retourne le JWT stocke
 */
function getCookie(name) {
    // document.cookie : chaine contenant tous les cookies du site
    // Format: "cookie1=valeur1; cookie2=valeur2; cookie3=valeur3"

    const value = `; ${document.cookie}`;
    // Ajoute "; " au debut pour uniformiser le parsing
    // Permet de trouver le premier cookie aussi facilement que les autres

    const parts = value.split(`; ${name}=`);
    // split() : divise la chaine au niveau du nom du cookie recherche
    // Exemple: "; token=abc123; other=xyz".split("; token=")
    // Resultat: ["; ", "abc123; other=xyz"]

    if (parts.length === 2) {
        // Si length === 2, le cookie a ete trouve
        // parts[0] = tout avant le cookie
        // parts[1] = valeur du cookie + cookies suivants

        return parts.pop().split(';').shift();
        // pop() : prend le dernier element (valeur + suite)
        // split(';') : separe au point-virgule pour isoler la valeur
        // shift() : prend le premier element (la valeur pure)
    }

    return null;
    // Cookie non trouve, retourne null
}

/**
 * Definit (cree ou met a jour) un cookie
 * @param {string} name - Nom du cookie
 * @param {string} value - Valeur a stocker
 * @param {number} days - Nombre de jours avant expiration (defaut: 7)
 *
 * Exemple: setCookie('token', 'jwt123', 7) stocke le token pour 7 jours
 */
function setCookie(name, value, days = 7) {
    // days = 7 : valeur par defaut si non specifie

    const expires = new Date();
    // Cree un objet Date avec la date/heure actuelle

    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    // getTime() : millisecondes depuis 1970
    // days * 24 * 60 * 60 * 1000 : convertit jours en millisecondes
    // 24 heures * 60 minutes * 60 secondes * 1000 millisecondes
    // setTime() : definit la nouvelle date d'expiration

    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    // Format du cookie: "nom=valeur;expires=date;path=/"
    // toUTCString() : formate la date en UTC (format standard pour cookies)
    // path=/ : cookie accessible sur tout le site
}

/**
 * Supprime un cookie en le faisant expirer immediatement
 * @param {string} name - Nom du cookie a supprimer
 *
 * Technique: on definit une date d'expiration dans le passe
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
    // expires=Thu, 01 Jan 1970 : date epoch Unix (debut du temps informatique)
    // Le navigateur supprime automatiquement les cookies expires
    // valeur vide apres le = pour nettoyer
}

/**
 * Verifie si l'utilisateur est authentifie
 * @returns {boolean} - true si connecte, false sinon
 *
 * Un utilisateur est considere authentifie s'il possede un token JWT valide
 */
function isAuthenticated() {
    return getCookie('token') !== null;
    // Verifie simplement la presence du cookie 'token'
    // !== null : comparaison stricte (type et valeur)
    // Note: ne verifie pas si le token est encore valide cote serveur
}

/**
 * Recupere le token JWT d'authentification
 * @returns {string|null} - Le token JWT ou null si non connecte
 */
function getToken() {
    return getCookie('token');
    // Raccourci pour getCookie('token')
    // Retourne le token JWT stocke dans le cookie
}

/**
 * Extrait l'ID du lieu depuis l'URL
 * @returns {string|null} - L'ID du lieu ou null si absent
 *
 * Exemple: pour place.html?id=123, retourne "123"
 */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    // window.location.search : partie query string de l'URL (ex: "?id=123&foo=bar")
    // URLSearchParams : API moderne pour parser les parametres d'URL

    return params.get('id');
    // get('id') : recupere la valeur du parametre 'id'
    // Retourne null si le parametre n'existe pas
}

// ============================================
// GESTION DE L'AUTHENTIFICATION
// ============================================
// Fonctions pour verifier et gerer l'etat de connexion de l'utilisateur

/**
 * Verifie l'etat d'authentification et met a jour l'interface
 * @returns {string|null} - Le token si authentifie, null sinon
 *
 * Cette fonction:
 * 1. Verifie si un token existe
 * 2. Cache ou affiche le lien "Login" selon l'etat
 */
function checkAuthentication() {
    const token = getToken();
    // Recupere le token JWT (ou null)

    const loginLink = document.getElementById('login-link');
    // Selectionne l'element HTML avec id="login-link"
    // C'est le lien/bouton "Login" dans le header

    if (token) {
        // Utilisateur connecte - cache le lien de connexion
        if (loginLink) {
            loginLink.style.display = 'none';
            // display: none : rend l'element invisible et retire de la mise en page
        }
    } else {
        // Utilisateur non connecte - affiche le lien de connexion
        if (loginLink) {
            loginLink.style.display = 'block';
            // display: block : affiche l'element normalement
        }
    }

    return token;
    // Retourne le token pour utilisation ulterieure
}

// ============================================
// FONCTIONS DE LA PAGE DE CONNEXION (login.html)
// ============================================
// Gestion du formulaire de login et authentification via API

/**
 * Initialise la page de connexion
 * Configure l'ecouteur d'evenement sur le formulaire de login
 */
function initLoginPage() {
    const loginForm = document.getElementById('login-form');
    // Selectionne le formulaire de connexion par son ID

    if (loginForm) {
        // Verifie que le formulaire existe (on est bien sur login.html)

        loginForm.addEventListener('submit', async (event) => {
            // addEventListener : attache une fonction a un evenement
            // 'submit' : evenement declenche lors de la soumission du formulaire
            // async : fonction asynchrone (permet d'utiliser await)
            // event : objet contenant les informations sur l'evenement

            event.preventDefault();
            // Empeche le comportement par defaut du formulaire
            // Sans ca, la page se rechargerait et perdrait les donnees

            const email = document.getElementById('email').value.trim();
            // Recupere la valeur du champ email
            // trim() : supprime les espaces au debut et a la fin

            const password = document.getElementById('password').value;
            // Recupere le mot de passe (pas de trim pour conserver les espaces voulus)

            if (!email || !password) {
                // Validation basique cote client
                alert('Please enter both email and password.');
                // alert() : affiche une boite de dialogue native du navigateur
                return;
                // Arrete l'execution de la fonction
            }

            await loginUser(email, password);
            // Appelle la fonction de connexion API
            // await : attend la fin de l'appel avant de continuer
        });
    }
}

/**
 * Connecte l'utilisateur via l'API
 * @param {string} email - Email de l'utilisateur
 * @param {string} password - Mot de passe
 *
 * Envoie les credentials a l'API et stocke le JWT en cas de succes
 */
async function loginUser(email, password) {
    // async : fonction asynchrone pour gerer les appels reseau

    try {
        // try-catch : gestion des erreurs pour les operations risquees

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            // fetch() : API moderne pour les requetes HTTP
            // await : attend la reponse du serveur
            // Template literal pour construire l'URL: base + endpoint

            method: 'POST',
            // Methode HTTP POST pour envoyer des donnees

            headers: {
                'Content-Type': 'application/json'
                // Indique que le corps de la requete est en JSON
            },

            body: JSON.stringify({ email, password })
            // body : corps de la requete
            // JSON.stringify() : convertit l'objet JavaScript en chaine JSON
            // { email, password } : raccourci ES6 pour { email: email, password: password }
        });

        if (response.ok) {
            // response.ok : true si status HTTP 200-299

            const data = await response.json();
            // Parse la reponse JSON
            // Contient { access_token: "jwt..." }

            // Stocke le token JWT dans un cookie
            document.cookie = `token=${data.access_token}; path=/`;
            // path=/ : cookie accessible sur tout le site

            // Redirige vers la page principale
            window.location.href = 'index.html';
            // window.location.href : change l'URL et navigue vers la nouvelle page

        } else {
            // Echec de l'authentification (mauvais identifiants, etc.)

            const error = await response.json().catch(() => ({}));
            // Tente de parser le message d'erreur JSON
            // catch(() => ({})) : si le parse echoue, utilise un objet vide

            alert('Login failed: ' + (error.message || error.error || 'Invalid credentials'));
            // Affiche le message d'erreur du serveur ou un message par defaut
        }

    } catch (error) {
        // Erreur reseau (serveur inaccessible, timeout, etc.)

        console.error('Login error:', error);
        // console.error : affiche l'erreur dans la console du navigateur (F12)

        alert('An error occurred during login. Please try again.');
    }
}

// ============================================
// FONCTIONS DE LA PAGE D'ACCUEIL (index.html)
// ============================================
// Affichage de la liste des lieux et filtrage par prix

/**
 * Initialise la page d'accueil
 * Charge la liste des lieux et configure le filtre de prix
 */
function initIndexPage() {
    const token = checkAuthentication();
    // Verifie l'authentification et met a jour l'UI

    // Charge et affiche la liste des lieux
    fetchPlaces(token);

    // Configure le filtre de prix
    const priceFilter = document.getElementById('price-filter');
    // Selectionne le menu deroulant de filtre

    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
        // 'change' : evenement declenche quand la selection change
        // filterPlacesByPrice : fonction a appeler lors du changement
    }
}

/**
 * Recupere la liste des lieux depuis l'API
 * @param {string|null} token - Token JWT pour authentification optionnelle
 *
 * L'API retourne tous les lieux disponibles
 */
async function fetchPlaces(token) {
    try {
        // Construction des headers HTTP
        const headers = {
            'Content-Type': 'application/json'
            // Type de contenu JSON
        };

        if (token) {
            // Si connecte, ajoute le header d'authentification
            headers['Authorization'] = `Bearer ${token}`;
            // Format: "Bearer <token>"
            // Permet a l'API de savoir qui fait la requete
        }

        const response = await fetch(`${API_BASE_URL}/places/`, {
            // Endpoint GET /places/ pour lister tous les lieux

            method: 'GET',
            // Methode GET pour recuperer des donnees

            headers: headers
            // Headers construits ci-dessus
        });

        if (response.ok) {
            // Requete reussie

            const places = await response.json();
            // Parse la reponse JSON
            // places : tableau d'objets lieu

            displayPlaces(places);
            // Affiche les lieux dans l'interface

        } else {
            // Erreur serveur

            console.error('Failed to fetch places:', response.statusText);
            // response.statusText : message d'erreur HTTP (ex: "Not Found")

            // Affiche un message d'erreur a l'utilisateur
            const placesList = document.getElementById('places-list');
            if (placesList) {
                placesList.innerHTML = '<p>Unable to load places. Please try again later.</p>';
                // innerHTML : remplace le contenu HTML de l'element
            }
        }

    } catch (error) {
        // Erreur reseau

        console.error('Error fetching places:', error);

        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<p>Unable to load places. Please try again later.</p>';
        }
    }
}

/**
 * Affiche les lieux dans le conteneur de la liste
 * @param {Array} places - Tableau d'objets lieu
 *
 * Genere dynamiquement les cartes HTML pour chaque lieu
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    // Conteneur qui va recevoir les cartes de lieux

    if (!placesList) return;
    // Si l'element n'existe pas, on sort de la fonction

    // Vide le conteneur actuel
    placesList.innerHTML = '';
    // Supprime tout le contenu existant

    if (!places || places.length === 0) {
        // Aucun lieu a afficher
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    // Cree une carte pour chaque lieu
    places.forEach(place => {
        // forEach : itere sur chaque element du tableau
        // place : l'objet lieu courant

        const placeCard = document.createElement('div');
        // createElement : cree un nouvel element HTML
        // 'div' : type d'element a creer

        placeCard.className = 'place-card';
        // className : definit la classe CSS

        placeCard.setAttribute('data-price', place.price || 0);
        // setAttribute : ajoute un attribut personnalise
        // data-price : utilise pour le filtrage par prix
        // place.price || 0 : si pas de prix, utilise 0

        placeCard.innerHTML = `
            <h3>${place.title || place.name || 'Unnamed Place'}</h3>
            <p class="price">$${place.price || 'N/A'} per night</p>
            <p>${place.description ? place.description.substring(0, 100) + '...' : 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        // Template literal pour le HTML de la carte
        // ${} : interpolation de variables JavaScript
        // place.title || place.name : prend title, sinon name, sinon texte par defaut
        // substring(0, 100) : tronque la description a 100 caracteres
        // href="place.html?id=${place.id}" : lien vers la page de details avec l'ID

        placesList.appendChild(placeCard);
        // appendChild : ajoute l'element enfant au conteneur
    });
}

/**
 * Filtre les cartes de lieux selon le prix selectionne
 * @param {Event} event - Evenement change du select
 *
 * Affiche uniquement les lieux dont le prix <= prix selectionne
 */
function filterPlacesByPrice(event) {
    const selectedPrice = event.target.value;
    // event.target : l'element qui a declenche l'evenement (le select)
    // value : la valeur de l'option selectionnee

    const placeCards = document.querySelectorAll('.place-card');
    // querySelectorAll : selectionne tous les elements correspondant au selecteur CSS
    // '.place-card' : toutes les cartes de lieux

    placeCards.forEach(card => {
        // Parcourt chaque carte

        const price = parseInt(card.getAttribute('data-price')) || 0;
        // getAttribute : recupere la valeur de l'attribut data-price
        // parseInt : convertit en nombre entier
        // || 0 : si NaN ou undefined, utilise 0

        if (selectedPrice === 'all' || price <= parseInt(selectedPrice)) {
            // 'all' : affiche tous les lieux
            // Sinon, affiche si prix <= prix selectionne

            card.style.display = 'block';
            // Affiche la carte
        } else {
            card.style.display = 'none';
            // Cache la carte
        }
    });
}

// ============================================
// FONCTIONS DE LA PAGE DETAILS DU LIEU (place.html)
// ============================================
// Affichage des details d'un lieu et de ses avis

/**
 * Initialise la page de details d'un lieu
 * Charge les informations du lieu et gere l'affichage du formulaire d'avis
 */
function initPlacePage() {
    const token = checkAuthentication();
    // Verifie l'authentification

    const placeId = getPlaceIdFromURL();
    // Recupere l'ID du lieu depuis l'URL (ex: ?id=123)

    if (!placeId) {
        // ID manquant dans l'URL
        const placeDetails = document.getElementById('place-details');
        if (placeDetails) {
            placeDetails.innerHTML = '<p>Place ID not found in URL.</p>';
        }
        return;
    }

    // Gestion de la section "Ajouter un avis"
    const addReviewSection = document.getElementById('add-review');

    if (addReviewSection) {
        if (token) {
            // Utilisateur connecte : affiche le formulaire d'avis
            addReviewSection.style.display = 'block';

            // Configure le formulaire d'avis
            initReviewFormOnPlacePage(token, placeId);
        } else {
            // Non connecte : cache le formulaire
            addReviewSection.style.display = 'none';
        }
    }

    // Charge les details du lieu
    fetchPlaceDetails(token, placeId);
}

/**
 * Recupere les details d'un lieu depuis l'API
 * @param {string|null} token - Token JWT
 * @param {string} placeId - ID du lieu
 */
async function fetchPlaceDetails(token, placeId) {
    try {
        // Construction des headers
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
            // Authentification optionnelle
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            // Endpoint GET /places/<id> pour un lieu specifique

            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            // Parse les details du lieu

            displayPlaceDetails(place);
            // Affiche les informations

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
 * Affiche les details d'un lieu sur la page
 * @param {Object} place - Objet lieu complet avec owner, amenities, reviews
 */
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    // Conteneur pour les details du lieu

    if (!placeDetails) return;

    // Construction du nom du proprietaire
    const hostName = place.owner
        ? `${place.owner.first_name || ''} ${place.owner.last_name || ''}`.trim() || 'Unknown'
        : (place.host || 'Unknown');
    // place.owner : objet utilisateur proprietaire (si fourni par l'API)
    // Concatene prenom et nom, ou utilise 'Unknown' par defaut
    // trim() : supprime les espaces en trop

    // Construction de la liste des commodites (amenities)
    let amenitiesHtml = '';

    if (place.amenities && place.amenities.length > 0) {
        // Si le lieu a des commodites

        const amenityItems = place.amenities.map(a =>
            `<li>${typeof a === 'string' ? a : (a.name || 'Unknown')}</li>`
        ).join('');
        // map() : transforme chaque amenity en element <li>
        // typeof a === 'string' : gere les deux formats (string ou objet)
        // join('') : concatene tous les <li> en une seule chaine

        amenitiesHtml = `
            <div class="amenities">
                <h4>Amenities</h4>
                <ul>${amenityItems}</ul>
            </div>
        `;
    }

    // Affiche les informations du lieu
    placeDetails.innerHTML = `
        <div class="place-info">
            <h2>${place.title || place.name || 'Unnamed Place'}</h2>
            <p><strong>Host:</strong> ${hostName}</p>
            <p><strong>Price:</strong> $${place.price || 'N/A'} per night</p>
            <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
            ${amenitiesHtml}
        </div>
    `;
    // Template literal pour le HTML
    // <strong> : texte en gras pour les labels
    // ${amenitiesHtml} : insere la section commodites si presente

    // Affiche les avis
    displayReviews(place.reviews);
}

/**
 * Affiche les avis d'un lieu
 * @param {Array} reviews - Tableau d'objets avis
 */
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    // Section contenant les avis

    if (!reviewsSection) return;

    // Reinitialise avec le titre
    reviewsSection.innerHTML = '<h3>Reviews</h3>';

    if (!reviews || reviews.length === 0) {
        // Aucun avis
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
        // += : ajoute au contenu existant (garde le h3)
        return;
    }

    // Cree une carte pour chaque avis
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        // Nouvel element div pour l'avis

        reviewCard.className = 'review-card';
        // Classe CSS pour le style

        // Construction du nom de l'auteur
        const userName = review.user
            ? `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim() || 'Anonymous'
            : (review.user_name || 'Anonymous');
        // Meme logique que pour hostName

        reviewCard.innerHTML = `
            <p><strong>${userName}</strong></p>
            <p>${review.text || review.comment || 'No comment'}</p>
            <p class="rating">Rating: ${review.rating || 'N/A'}/5</p>
        `;
        // review.text ou review.comment : supporte les deux formats d'API
        // review.rating : note sur 5

        reviewsSection.appendChild(reviewCard);
        // Ajoute la carte au conteneur
    });
}

/**
 * Configure le formulaire d'avis sur la page de details du lieu
 * @param {string} token - Token JWT (requis pour soumettre)
 * @param {string} placeId - ID du lieu
 */
function initReviewFormOnPlacePage(token, placeId) {
    const reviewForm = document.getElementById('review-form');
    // Formulaire d'ajout d'avis

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            // Ecoute la soumission du formulaire

            event.preventDefault();
            // Empeche le rechargement de la page

            const reviewText = document.getElementById('review-text').value.trim();
            // Texte de l'avis (IDs specifiques a place.html)

            const rating = document.getElementById('review-rating').value;
            // Note selectionnee

            if (!reviewText || !rating) {
                // Validation
                alert('Please fill in both review and rating.');
                return;
            }

            await submitReview(token, placeId, reviewText, parseInt(rating));
            // Envoie l'avis a l'API
            // parseInt(rating) : convertit la note en nombre
        });
    }
}

// ============================================
// FONCTIONS DE LA PAGE D'AJOUT D'AVIS (add_review.html)
// ============================================
// Page dediee a l'ajout d'un avis (alternative au formulaire inline)

/**
 * Initialise la page d'ajout d'avis
 * Verifie l'authentification et configure le formulaire
 */
function initAddReviewPage() {
    const token = checkAuthentication();
    // Verifie si l'utilisateur est connecte

    // Redirige vers l'accueil si non connecte
    if (!token) {
        window.location.href = 'index.html';
        // Securite : seuls les utilisateurs connectes peuvent laisser un avis
        return;
    }

    const placeId = getPlaceIdFromURL();
    // Recupere l'ID du lieu depuis l'URL

    if (!placeId) {
        // ID manquant
        alert('Place ID not found in URL.');
        window.location.href = 'index.html';
        return;
    }

    // Charge le nom du lieu pour l'afficher dans le titre
    fetchPlaceNameForReview(token, placeId);

    // Configure le formulaire
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value.trim();
            // IDs specifiques a add_review.html (differents de place.html)

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
 * Recupere le nom du lieu pour l'afficher sur la page d'ajout d'avis
 * @param {string} token - Token JWT
 * @param {string} placeId - ID du lieu
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
            // Recupere les details du lieu
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();

            const placeNameElement = document.getElementById('place-name');
            // Element <span> dans le titre

            if (placeNameElement) {
                placeNameElement.textContent = place.title || place.name || 'Unknown Place';
                // textContent : definit le texte de l'element
                // Plus securise que innerHTML (pas d'interpretation HTML)
            }
        }

    } catch (error) {
        console.error('Error fetching place name:', error);
        // En cas d'erreur, le texte par defaut "Loading..." reste affiche
    }
}

/**
 * Soumet un avis a l'API
 * @param {string} token - Token JWT (requis)
 * @param {string} placeId - ID du lieu
 * @param {string} reviewText - Texte de l'avis
 * @param {number} rating - Note de 1 a 5
 *
 * Fonction partagee entre place.html et add_review.html
 */
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            // Endpoint POST /reviews/ pour creer un nouvel avis

            method: 'POST',
            // Methode POST pour creation

            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                // Token JWT requis pour identifier l'auteur de l'avis
            },

            body: JSON.stringify({
                text: reviewText,
                // Texte de l'avis

                rating: rating,
                // Note (1-5)

                place_id: placeId
                // ID du lieu concerne
            })
        });

        if (response.ok) {
            // Avis cree avec succes

            alert('Review submitted successfully!');

            // Redirige vers la page du lieu pour voir l'avis
            window.location.href = `place.html?id=${placeId}`;

        } else {
            // Erreur lors de la creation

            const errorData = await response.json().catch(() => ({}));
            // Tente de parser le message d'erreur

            const errorMsg = errorData.message || errorData.error || errorData.errors || JSON.stringify(errorData) || 'Unknown error';
            // Gere differents formats de message d'erreur possibles

            alert('Failed to submit review: ' + errorMsg);
        }

    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred while submitting your review.');
    }
}

// ============================================
// INITIALISATION DE LA PAGE
// ============================================
// Point d'entree principal - detecte la page et lance l'initialisation appropriee

/**
 * Fonction principale d'initialisation
 * Executee automatiquement quand le DOM est pret
 */
document.addEventListener('DOMContentLoaded', () => {
    // DOMContentLoaded : evenement declenche quand le HTML est completement charge
    // (n'attend pas les images, styles, etc.)
    // Alternative a window.onload (qui attend tout)

    const path = window.location.pathname;
    // pathname : chemin de l'URL sans le domaine
    // Ex: "/index.html" ou "/place.html"

    // Determine quelle page est chargee et initialise en consequence
    if (path.endsWith('login.html')) {
        // Page de connexion
        initLoginPage();

    } else if (path.endsWith('place.html')) {
        // Page de details d'un lieu
        initPlacePage();

    } else if (path.endsWith('add_review.html')) {
        // Page d'ajout d'avis
        initAddReviewPage();

    } else if (path.endsWith('index.html') || path.endsWith('/') || path === '') {
        // Page d'accueil (index.html ou racine du site)
        initIndexPage();
    }

    // Note: chaque fonction init* configure les elements et evenements
    // specifiques a sa page
});
