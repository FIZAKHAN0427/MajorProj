from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from loguru import logger
import traceback

from .schemas import CropInput, CropPrediction, ModelInfo, ErrorResponse
from ..model import CropModel
from ..utils import validate_input_data, get_crop_info
from ..database import db_manager

router = APIRouter()
model = CropModel()

@router.post("/predict", response_model=CropPrediction)
async def predict_crop(input_data: CropInput):
    """
    Predict the most suitable crop based on soil and environmental conditions
    """
    try:
        logger.info(f"Received prediction request: {input_data.dict()}")
        
        # Validate input data
        validation_errors = validate_input_data(input_data.dict())
        if validation_errors:
            raise HTTPException(status_code=400, detail=f"Validation errors: {', '.join(validation_errors)}")
        
        # Make prediction
        try:
            prediction_result = model.predict(input_data.dict())
        except ValueError as e:
            # Try to load model if not already loaded
            if "Model not trained or loaded" in str(e):
                success = model.load_model()
                if not success:
                    raise HTTPException(
                        status_code=503, 
                        detail="Model not available. Please train the model first using the /train endpoint or scripts/retrain_model.py"
                    )
                prediction_result = model.predict(input_data.dict())
            else:
                raise
        
        # Get additional crop information
        crop_info = get_crop_info(prediction_result['crop'])
        
        # Save prediction to database (optional)
        try:
            db_manager.save_prediction(
                input_data.dict(), 
                prediction_result['crop'], 
                prediction_result['confidence']
            )
        except Exception as db_error:
            logger.warning(f"Failed to save prediction to database: {db_error}")
        
        # Prepare response
        response = CropPrediction(
            crop=prediction_result['crop'],
            confidence=prediction_result['confidence'],
            all_probabilities=prediction_result['all_probabilities'],
            crop_info=crop_info
        )
        
        logger.info(f"Prediction successful: {prediction_result['crop']} (confidence: {prediction_result['confidence']:.3f})")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """
    Get information about the current model
    """
    try:
        # Try to load model if not already loaded
        if model.model is None:
            success = model.load_model()
            if not success:
                raise HTTPException(
                    status_code=404, 
                    detail="Model not found. Please train the model first."
                )
        
        model_info = model.get_model_info()
        if model_info is None:
            raise HTTPException(status_code=404, detail="Model not available")
        
        return ModelInfo(**model_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/model/train")
async def train_model():
    """
    Train the crop recommendation model
    """
    try:
        logger.info("Starting model training via API")
        
        # Train the model
        training_results = model.train()
        
        logger.info("Model training completed successfully")
        return {
            "message": "Model trained successfully",
            "results": training_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Training error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get("/crops")
async def get_supported_crops():
    """
    Get list of crops that the model can predict
    """
    try:
        # Try to load model if not already loaded
        if model.model is None:
            success = model.load_model()
            if not success:
                return {
                    "crops": [],
                    "message": "Model not available. Please train the model first."
                }
        
        model_info = model.get_model_info()
        if model_info is None:
            return {
                "crops": [],
                "message": "Model information not available"
            }
        
        crops_with_info = []
        for crop in model_info['classes']:
            crop_info = get_crop_info(crop)
            crops_with_info.append({
                "name": crop,
                "info": crop_info
            })
        
        return {
            "crops": crops_with_info,
            "total": len(crops_with_info)
        }
        
    except Exception as e:
        logger.error(f"Error getting crops: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/predict/sample")
async def get_sample_prediction():
    """
    Get a sample prediction for testing purposes
    """
    try:
        # Sample input data
        sample_input = CropInput(
            N=90,
            P=42,
            K=43,
            temperature=20.87,
            humidity=82.00,
            ph=6.50,
            rainfall=202.93,
            ndvi=0.65
        )
        
        # Make prediction
        prediction_result = await predict_crop(sample_input)
        
        return {
            "input": sample_input.dict(),
            "prediction": prediction_result.dict(),
            "message": "Sample prediction for testing purposes"
        }
        
    except Exception as e:
        logger.error(f"Sample prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")