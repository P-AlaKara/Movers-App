const BASE_URL = 'http://localhost:8000';

async function request(endpoint, options = {}) {
    let token = getAccessToken();

    // Refresh token if expired before making the call
    if (token && isTokenExpired(token)) {
        token = await refreshAccessToken();
        if (!token) return null;
    }

    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    // Token rejected server-side, attempt one refresh and retry
    if (response.status === 401) {
        token = await refreshAccessToken();
        if (!token) return null;

        const retry = await fetch(`${BASE_URL}${endpoint}`, {
            ...options,
            headers: { ...headers, 'Authorization': `Bearer ${token}` },
        });
        return retry;
    }

    return response;
}

// --- Auth ---
const api = {
    auth: {
        register: (data) => request('/accounts/register/', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        login: (data) => request('/accounts/login/', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
    },

    // --- Profile ---
    profile: {
        me: () => request('/profiles/me/'),
        update: (data) => request('/profiles/me/', {
            method: 'PATCH',
            body: JSON.stringify(data)
        }),
        movers: (params = {}) => {
            const query = new URLSearchParams(params).toString();
            return request(`/profiles/movers/${query ? '?' + query : ''}`);
        },
        mover: (id) => request(`/profiles/movers/${id}/`),
    },

    // --- Jobs (customer) ---
    requests: {
        list: (params = {}) => {
            const query = new URLSearchParams(params).toString();
            return request(`/jobs/requests/${query ? '?' + query : ''}`);
        },
        create: (data) => request('/jobs/requests/', {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        detail: (id) => request(`/jobs/requests/${id}/`),
        cancel: (id) => request(`/jobs/requests/${id}/cancel/`, {
            method: 'POST'
        }),
    },

    // --- Bids ---
    bids: {
        place: (requestId, data) => request(`/jobs/requests/${requestId}/bid/`, {
            method: 'POST',
            body: JSON.stringify(data)
        }),
        accept: (bidId) => request(`/jobs/bids/${bidId}/accept/`, {
            method: 'POST'
        }),
        cancel: (bidId) => request(`/jobs/bids/${bidId}/cancel/`, {
            method: 'POST'
        }),
    },

    // --- Jobs (mover) ---
    jobs: {
        available: (params = {}) => {
            const query = new URLSearchParams(params).toString();
            return request(`/jobs/available/${query ? '?' + query : ''}`);
        },
        my: (params = {}) => {
            const query = new URLSearchParams(params).toString();
            return request(`/jobs/my/${query ? '?' + query : ''}`);
        },
        start: (id) => request(`/jobs/requests/${id}/start/`, { method: 'POST' }),
        complete: (id) => request(`/jobs/requests/${id}/complete/`, { method: 'POST' }),
    },

    // --- Dashboard ---
    dashboard: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return request(`/dashboard/${query ? '?' + query : ''}`);
    },

    // --- Notifications ---
    notifications: {
        list: () => request('/notifications/'),
        markRead: (id) => request(`/notifications/${id}/read/`, { method: 'POST' }),
        markAllRead: () => request('/notifications/read-all/', { method: 'POST' }),
    },
};
```

---

A few things to note about how these work together. Every page will include both scripts and call `requireAuth()` at the top. Role-restricted pages call `requireRole('mover')` or `requireRole('customer')` instead. All API calls go through `api.something()` which internally calls `request()` which handles the token automatically — pages never touch tokens directly.

**Commit message:**
```
feat(frontend): add auth.js and api.js as frontend foundation

- auth.js handles token storage, decoding, expiry check, 
  refresh, logout, and route protection
- api.js centralizes all fetch calls with automatic token 
  attachment and 401 retry logic
- All endpoints mapped to named methods matching backend routes