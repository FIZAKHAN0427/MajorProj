const { MongoClient } = require('mongodb');
require('dotenv').config();

const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/fasalneeti';
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
let dbInstance;

async function connectDB() {
  if (!dbInstance) {
    await client.connect();
    dbInstance = client.db();
  }
  return dbInstance;
}

module.exports = { connectDB };