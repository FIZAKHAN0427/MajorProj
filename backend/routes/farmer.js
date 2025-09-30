const express = require('express');
const router = express.Router();
const { connectDB } = require('../../database');

// Register Farmer
router.post('/register', async (req, res) => {
  try {
    const db = await connectDB();
    const result = await db.collection('farmers').insertOne(req.body);
    res.json({ success: true, farmerId: result.insertedId });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Registration failed', error: err.message });
  }
});

// Login Farmer (simple example, add password hashing in production)
router.post('/login', async (req, res) => {
  try {
    const db = await connectDB();
    const farmer = await db.collection('farmers').findOne({ email: req.body.email, password: req.body.password });
    if (!farmer) return res.status(401).json({ success: false, message: 'Invalid credentials' });
    // Generate token here for real app
    res.json({ success: true, farmer });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Login failed', error: err.message });
  }
});

// Get Farmer Profile
router.get('/:farmerId', async (req, res) => {
  try {
    const db = await connectDB();
    const farmer = await db.collection('farmers').findOne({ _id: new require('mongodb').ObjectId(req.params.farmerId) });
    res.json(farmer);
  } catch (err) {
    res.status(500).json({ success: false, message: 'Profile fetch failed', error: err.message });
  }
});

// ...add other routes for dashboard, crops, weather, predictions, etc.
module.exports = router;