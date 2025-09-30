const express = require('express');
const router = express.Router();
const { connectDB } = require('../../database');
const { ObjectId } = require('mongodb');

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

// Login Farmer (simple, add password hashing in production)
router.post('/login', async (req, res) => {
  try {
    const db = await connectDB();
    const farmer = await db.collection('farmers').findOne({ email: req.body.email, password: req.body.password });
    if (!farmer) return res.status(401).json({ success: false, message: 'Invalid credentials' });
    res.json({ success: true, farmer });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Login failed', error: err.message });
  }
});

// Get Farmer Profile
router.get('/:farmerId', async (req, res) => {
  try {
    const db = await connectDB();
    const farmer = await db.collection('farmers').findOne({ _id: new ObjectId(req.params.farmerId) });
    res.json(farmer);
  } catch (err) {
    res.status(500).json({ success: false, message: 'Profile fetch failed', error: err.message });
  }
});

// Update Farmer Profile
router.put('/:farmerId', async (req, res) => {
  try {
    const db = await connectDB();
    const result = await db.collection('farmers').updateOne(
      { _id: new ObjectId(req.params.farmerId) },
      { $set: req.body }
    );
    res.json({ success: true, updated: result.modifiedCount });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Update failed', error: err.message });
  }
});

// Get Farmer Dashboard (example: return crops)
router.get('/:farmerId/dashboard', async (req, res) => {
  try {
    const db = await connectDB();
    const farmer = await db.collection('farmers').findOne({ _id: new ObjectId(req.params.farmerId) });
    res.json({ crops: farmer.crops || [] });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Dashboard fetch failed', error: err.message });
  }
});

// Save Crop Data
router.post('/:farmerId/crops', async (req, res) => {
  try {
    const db = await connectDB();
    const result = await db.collection('farmers').updateOne(
      { _id: new ObjectId(req.params.farmerId) },
      { $push: { crops: req.body } }
    );
    res.json({ success: true, updated: result.modifiedCount });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Crop save failed', error: err.message });
  }
});

module.exports = router;
