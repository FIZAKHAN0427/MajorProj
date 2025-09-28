# Crop Recommendation Backend

AI-powered crop recommendation system using machine learning and satellite data to predict suitable crops based on soil and environmental conditions.

## 🌾 Features

- **Machine Learning**: RandomForest classifier trained on agricultural datasets
- **Satellite Data**: Integration with Google Earth Engine for NDVI data
- **RESTful API**: FastAPI-based web service with automatic documentation
- **Real-time Predictions**: Instant crop recommendations based on input parameters
- **Data Sources**: Kaggle agricultural datasets + Sentinel satellite imagery
- **Comprehensive Testing**: Unit tests for API and ML components

## 📊 Datasets

This project uses the following datasets:

1. **Kaggle Crop Recommendation Dataset**: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
2. **Indian Crops Dataset**: https://www.kaggle.com/code/prasadkevin/crops-prediction-indian-dataset/data
3. **Sentinel Satellite Data**: https://developers.google.com/earth-engine/datasets/catalog/sentinel

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- (Optional) Kaggle API credentials for dataset download
- (Optional) Google Earth Engine account for satellite data

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd crop-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials (optional)
   ```

### Training the Model

1. **Train with sample data:**
   ```bash
   make train
   ```

2. **Train with fresh Kaggle data:**
   ```bash
   make train-with-data
   ```

3. **Custom training:**
   ```bash
   python scripts/retrain_model.py --download-data --test-size 0.2
   ```

### Running the API

1. **Start development server:**
   ```bash
   make run
   # or
   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test the API:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/predict" \
        -H "Content-Type: application/json" \
        -d '{
          "N": 90, "P": 42, "K": 43,
          "temperature": 20.87, "humidity": 82.00,
          "ph": 6.50, "rainfall": 202.93, "ndvi": 0.65
        }'
   ```

## 📁 Project Structure

```
crop-backend/
├── data/                    # Datasets and data files
├── notebooks/               # Jupyter notebooks for analysis
├── src/                     # Source code
│   ├── __init__.py
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database operations
│   ├── preprocessing.py    # Data preprocessing
│   ├── model.py           # ML model implementation
│   ├── sentinel.py        # Satellite data fetching
│   ├── utils.py           # Utility functions
│   └── api/               # FastAPI application
│       ├── __init__.py
│       ├── main.py        # FastAPI app entry point
│       ├── routes.py      # API routes
│       └── schemas.py     # Pydantic schemas
├── models/                 # Trained model files
├── logs/                  # Application logs
├── scripts/               # Utility scripts
│   ├── fetch_sentinel_data.py  # Fetch satellite data
│   └── retrain_model.py       # Model training script
├── tests/                 # Test suite
│   ├── test_api.py        # API tests
│   └── test_model.py      # Model tests
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── Makefile             # Build automation
└── README.md           # This file
```

## 🔧 API Endpoints

### Health Check
- `GET /health` - API health status
- `GET /api/health` - API health check

### Predictions
- `POST /api/v1/predict` - Predict suitable crop
- `GET /api/v1/predict/sample` - Sample prediction for testing

### Model Management
- `GET /api/v1/model/info` - Model information
- `POST /api/v1/model/train` - Train model via API

### Utilities
- `GET /api/v1/crops` - List supported crops

## 📊 Input Parameters

The prediction API accepts the following parameters:

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| N | float | 0-200 | Nitrogen content in soil (kg/hectare) |
| P | float | 0-200 | Phosphorus content in soil (kg/hectare) |
| K | float | 0-300 | Potassium content in soil (kg/hectare) |
| temperature | float | -50 to 60 | Temperature (°C) |
| humidity | float | 0-100 | Humidity (%) |
| ph | float | 0-14 | Soil pH value |
| rainfall | float | ≥0 | Rainfall (mm) |
| ndvi | float (optional) | -1 to 1 | NDVI from satellite data |

## 🌍 Satellite Data Integration

### Fetching Sentinel Data

1. **Setup Google Earth Engine:**
   ```bash
   earthengine authenticate
   ```

2. **Fetch NDVI data:**
   ```bash
   python scripts/fetch_sentinel_data.py --lat 28.6139 --lon 77.2090
   ```

3. **Fetch for predefined regions:**
   ```bash
   python scripts/fetch_sentinel_data.py --region punjab
   ```

## 🧪 Testing

Run the test suite:

```bash
# All tests
make test

# API tests only
make test-api

# Model tests only
make test-model

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 🔧 Development

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Run all checks
make check
```

### Development Server

```bash
# Run with auto-reload and debug logging
make dev
```

## 📦 Production Deployment

### Using Uvicorn

```bash
# Production server with multiple workers
make production
```

### Environment Variables

For production, configure these environment variables:

```bash
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
MONGODB_URI=mongodb://your-mongo-server:27017/crop_recommendation
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## 🤖 Model Information

### Algorithm
- **Base Model**: Random Forest Classifier
- **Features**: Soil nutrients (N, P, K), climate data, optional NDVI
- **Training**: Cross-validated with feature importance analysis

### Performance Metrics
- Training accuracy
- Test accuracy
- Cross-validation scores
- Feature importance rankings

### Supported Crops
The model can predict these crops (varies based on training data):
- Rice
- Wheat
- Corn/Maize
- Cotton
- Sugarcane
- Jute
- Coconut
- Papaya
- Orange
- Apple
- And more...

## 🔍 Troubleshooting

### Common Issues

1. **Model not found error:**
   ```bash
   make train  # Train the model first
   ```

2. **Kaggle API authentication:**
   ```bash
   kaggle config view  # Check credentials
   ```

3. **Google Earth Engine authentication:**
   ```bash
   earthengine authenticate
   ```

4. **Port already in use:**
   ```bash
   # Change port in .env or use different port
   uvicorn src.api.main:app --port 8001
   ```

## 📖 API Documentation

Once the server is running, comprehensive API documentation is available:

- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc
- **OpenAPI spec**: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Format code: `make format`
6. Submit a pull request

## 📞 Support

For technical support or questions:
- **API Documentation**: http://localhost:8000/docs
- **Issues**: Create an issue in the repository
- **Email**: support@cropbackend.com

---

**Built with ❤️ for sustainable agriculture**

*Empowering farmers with AI-driven crop recommendations*