// backend/server.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());

// Master Admin System - Health Check Route
app.get('/api/health', (req, res) => {
    res.json({ 
        system: 'ARM TechBridge AI', 
        status: 'Online',
        modules: ['Master Admin', 'User System', 'IT Ticketing'] 
    });
});

app.listen(PORT, () => {
    console.log(`ARM TechBridge Backend running on port ${PORT}`);
});
