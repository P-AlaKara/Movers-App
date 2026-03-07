
const TOKEN_KEY = 'access';
const REFRESH_KEY = 'refresh';

function saveTokens(access, refresh) {
    localStorage.setItem(TOKEN_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
}

function getAccessToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
}

function clearTokens() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
}

function decodeToken(token) {
    try {
        const payload = token.split('.')[1];
        return JSON.parse(atob(payload));
    } catch {
        return null;
    }
}

function getUser() {
    const token = getAccessToken();
    if (!token) return null;
    return decodeToken(token);
}

function getRole() {
    const user = getUser();
    return user ? user.role : null;
}

function isTokenExpired(token) {
    const decoded = decodeToken(token);
    if (!decoded) return true;
    // exp is in seconds, Date.now() is in milliseconds
    return decoded.exp * 1000 < Date.now();
}

async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) {
        logout();
        return null;
    }

    const response = await fetch('http://localhost:8000/accounts/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem(TOKEN_KEY, data.access);
        return data.access;
    } else {
        logout();
        return null;
    }
}

function logout() {
    clearTokens();
    window.location.href = '/frontend/login.html';
}

function requireAuth() {
    const token = getAccessToken();
    if (!token) {
        window.location.href = '/frontend/login.html';
        return false;
    }
    return true;
}

function requireRole(role) {
    if (!requireAuth()) return false;
    if (getRole() !== role) {
        window.location.href = '/frontend/dashboard.html';
        return false;
    }
    return true;
}