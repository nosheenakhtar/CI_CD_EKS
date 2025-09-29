const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:5000';

app.get('/', async (_req, res) => {
  try {
    const r = await axios.get(`${BACKEND_URL}/`);
    res.json({ service: 'frontend', backend: r.data });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/healthz', (_req, res) => res.send('ok'));

app.listen(PORT, () => console.log(`Frontend on :${PORT}`));
