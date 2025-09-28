from pydantic import BaseModel, Field
from typing import Optional

class CropInput(BaseModel):
    """Input schema for crop prediction"""
    N: float = Field(..., description="Nitrogen content in soil", ge=0, le=200)
    P: float = Field(..., description="Phosphorus content in soil", ge=0, le=200)
    K: float = Field(..., description="Potassium content in soil", ge=0, le=300)
    temperature: float = Field(..., description="Temperature in Celsius", ge=-50, le=60)
    humidity: float = Field(..., description="Humidity percentage", ge=0, le=100)
    ph: float = Field(..., description="pH value of soil", ge=0, le=14)
    rainfall: float = Field(..., description="Rainfall in mm", ge=0)
    ndvi: Optional[float] = Field(None, description="NDVI value from satellite data", ge=-1, le=1)

    class Config:
        schema_extra = {
            "example": {
                "N": 90,
                "P": 42,
                "K": 43,
                "temperature": 20.87,
                "humidity": 82.00,
                "ph": 6.50,
                "rainfall": 202.93,
                "ndvi": 0.65
            }
        }

class CropPrediction(BaseModel):
    """Output schema for crop prediction"""
    crop: str = Field(..., description="Recommended crop")
    confidence: float = Field(..., description="Prediction confidence", ge=0, le=1)
    all_probabilities: dict = Field(..., description="Probabilities for all crops")
    crop_info: Optional[dict] = Field(None, description="Additional crop information")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="API status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: str = Field(..., description="Error timestamp")

class ModelInfo(BaseModel):
    """Model information schema"""
    model_type: str
    n_features: int
    feature_columns: list
    n_classes: int
    classes: list
    last_trained: Optional[str] = None

class PredictionHistory(BaseModel):
    """Prediction history schema"""
    id: str
    input_data: CropInput
    prediction: str
    confidence: float
    timestamp: str