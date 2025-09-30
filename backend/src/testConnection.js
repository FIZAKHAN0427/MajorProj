const { connectDB } = require('./database');

async function testConnection() {
  try {
    const db = await connectDB();
    const collections = await db.listCollections().toArray();
    console.log('Connected! Collections:', collections);
  } catch (err) {
    console.error('Connection failed:', err.message);
    console.error(err); // This will show the full error and stack trace
  }
}

testConnection();