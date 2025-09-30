const express = require('express');
const app = express();
require('dotenv').config();

app.use(express.json());
app.use('/api/farmers', require('./routes/farmers'));
app.use('/api/admin', require('./routes/admin'));

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
