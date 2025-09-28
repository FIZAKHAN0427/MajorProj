# FasalNeeti - Smart Farming Solutions

## Project Overview
FasalNeeti ("Crop Wisdom") is a comprehensive smart farming platform that combines a React frontend with an AI-powered backend for crop recommendations and agricultural insights.

**Slogan:** "Apni Mitti, Apna Data, Apna Bhavishya" (Our Soil, Our Data, Our Future)

## Current Architecture
- **Frontend**: React.js application with Tailwind CSS
- **Backend**: Crop recommendation system (in development)
- **Data Sources**: Kaggle datasets + Sentinel satellite data
- **Database**: MongoDB for farmer data and analytics

## Frontend Features
- Farmer and Admin dashboards
- Crop yield predictions with interactive charts
- Stress detection alerts and analytics  
- Weather integration and forecasts
- Fertilizer recommendations
- Hindi-English bilingual interface
- Light/dark theme support

## Recent Changes
- **2024-09-28**: Successfully configured React app for Replit environment
  - Updated package.json to use HOST=0.0.0.0 PORT=5000 
  - Added DANGEROUSLY_DISABLE_HOST_CHECK=true for Replit proxy compatibility
  - Fixed compilation errors in FarmerDashboard.js and mockData.js
  - Set up Frontend Server workflow on port 5000
  - Configured deployment for autoscale with build and serve setup

## Technical Setup
- **Development Server**: Configured for 0.0.0.0:5000 with host check disabled
- **Deployment**: Autoscale deployment with npm build and serve
- **Workflow**: Single frontend workflow for development server

## Project Status
- ✅ Frontend setup complete and functional
- 🔄 Backend integration in progress
- 📊 Using mock data currently, backend will provide real API endpoints

## User Preferences
- Maintains existing Indian farming theme and Hindi-English interface
- Focuses on farmer-friendly design with large buttons and clear navigation
- Uses earth-tone color palette with crop and soil inspired themes