/**
 * Express.js Integration for API Firewall
 * Usage: app.use(apiFirewallMiddleware)
 */

const fs = require('fs');
const path = require('path');

// Simple threat detection patterns (JavaScript version)
const SQL_PATTERNS = [
    /\bunion\s+(all\s+)?select\b/i,
    /\bdrop\s+(table|database|schema)\b/i,
    /\binsert\s+into\b/i,
    /\bdelete\s+from\b/i,
    /\bor\s+['"]?1['"]?\s*=\s*['"]?1['"]?\b/i
];

const XSS_PATTERNS = [
    /<script[^>]*>.*?<\/script[^>]*>/i,
    /on\w+\s*=\s*['"]?[^'"]*['"]?/i,
    /javascript:\s*[^\s]/i,
    /<iframe[^>]*>/i
];

function detectThreat(data) {
    const dataStr = typeof data === 'string' ? data : JSON.stringify(data);
    
    for (const pattern of SQL_PATTERNS) {
        if (pattern.test(dataStr)) return 'SQL Injection';
    }
    
    for (const pattern of XSS_PATTERNS) {
        if (pattern.test(dataStr)) return 'XSS Attack';
    }
    
    return null;
}

function getClientIP(req) {
    return req.headers['x-forwarded-for']?.split(',')[0] || 
           req.connection.remoteAddress || 
           req.socket.remoteAddress ||
           req.ip;
}

// Rate limiting storage
const requestCounts = new Map();
const RATE_LIMIT = parseInt(process.env.RATE_LIMIT) || 10;
const API_KEYS = process.env.API_KEYS ? process.env.API_KEYS.split(',').map(k => k.trim()) : [];

function apiFirewallMiddleware(req, res, next) {
    const clientIP = getClientIP(req);
    const currentTime = Date.now();
    
    // Rate limiting
    if (!requestCounts.has(clientIP)) {
        requestCounts.set(clientIP, []);
    }
    
    const requests = requestCounts.get(clientIP);
    const validRequests = requests.filter(time => currentTime - time < 60000); // 1 minute
    
    if (validRequests.length >= RATE_LIMIT) {
        return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    validRequests.push(currentTime);
    requestCounts.set(clientIP, validRequests);
    
    // API key validation
    if (API_KEYS.length > 0 && req.method === 'POST') {
        const apiKey = req.headers['x-api-key'];
        if (!apiKey || !API_KEYS.includes(apiKey)) {
            return res.status(401).json({ error: 'Invalid API key' });
        }
    }
    
    // Threat detection
    if (req.body) {
        const threat = detectThreat(req.body);
        if (threat) {
            // Log the threat
            const logEntry = {
                timestamp: new Date().toISOString(),
                clientIP,
                method: req.method,
                url: req.url,
                threat,
                userAgent: req.headers['user-agent']
            };
            
            fs.appendFileSync('firewall_logs.json', JSON.stringify(logEntry) + '\n');
            
            return res.status(400).json({ error: `Blocked: ${threat}` });
        }
    }
    
    next();
}

module.exports = {
    apiFirewallMiddleware,
    detectThreat,
    getClientIP
};

/* Usage Example:
const express = require('express');
const { apiFirewallMiddleware } = require('./integrations/express_integration');

const app = express();
app.use(express.json());
app.use(apiFirewallMiddleware);

app.post('/api/test', (req, res) => {
    res.json({ message: 'Success' });
});

app.listen(3000, () => {
    console.log('Server running on port 3000 with API Firewall protection');
});
*/