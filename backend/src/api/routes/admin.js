const express = require('express');
const router = express.Router();
const { connectDB } = require('../../database');
const { ObjectId } = require('mongodb');

// Get all farmers
router.get('/farmers', async (req, res) => {
  try {
    const db = await connectDB();
    const farmers = await db.collection('farmers').find().toArray();
    res.json(farmers);
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to fetch farmers', error: err.message });
  }
});

// Delete farmer
router.delete('/farmers/:farmerId', async (req, res) => {
  try {
    const db = await connectDB();
    const result = await db.collection('farmers').deleteOne({ _id: new ObjectId(req.params.farmerId) });
    res.json({ success: true, deleted: result.deletedCount });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to delete farmer', error: err.message });
  }
});

module.exports = router;
