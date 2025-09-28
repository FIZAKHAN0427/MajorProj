from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from loguru import logger
from .config import settings

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.database = None
        
    def connect(self):
        """Connect to MongoDB database"""
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.database = self.client[settings.DATABASE_NAME]
            # Test connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_collection(self, collection_name: str):
        """Get a collection from the database"""
        if self.database is None:
            raise RuntimeError("Database not connected")
        return self.database[collection_name]
    
    def save_prediction(self, input_data: dict, prediction: str, confidence: float = None):
        """Save prediction to database"""
        try:
            collection = self.get_collection("predictions")
            document = {
                "input_data": input_data,
                "prediction": prediction,
                "confidence": confidence,
                "timestamp": pd.Timestamp.now()
            }
            result = collection.insert_one(document)
            logger.info(f"Saved prediction with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Failed to save prediction: {e}")
            return None

# Global database instance
db_manager = DatabaseManager()