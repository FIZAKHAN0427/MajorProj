
const express = require('express');
const app = express();
require('dotenv').config();

app.use(express.json());
app.use('/api/farmers', require('./routes/farmers'));
// Add other routes as needed

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
