const express = require('express');
const path = require('path');
const { Pool } = require('pg');  // PostgreSQL client

const app = express();
const PORT = process.env.PORT || 3000;

// Database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// API endpoint to fetch movies
app.get('/movies', async (req, res) => {
  try {
    const result = await pool.query('select title, director, year FROM movies');
    res.json(result.rows);
  } catch (err) {
    console.error('Database error:', err);
    res.status(500).json({ error: 'Database connection failed' });
  }
});

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname)));

// Default route → index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/dbtest', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.send('DB connection OK');
  } catch (err) {
    console.error('DB connection failed:', err.message);
    res.status(500).send('DB connection failed: ' + err.message);
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
