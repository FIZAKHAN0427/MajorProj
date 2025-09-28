import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import mongoService from '../services/mongoService';

/**
 * Professional Farmer Registration component with MongoDB integration
 * Clean design, comprehensive validation, and database storage
 */
const FarmerLogin = () => {
  const navigate = useNavigate();
  
  // Form state management
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    mobile: '',
    location: '',
    farmSize: '',
    soilType: '',
    soilPH: '',
    lastCrop: '',
    irrigationType: '',
    fertilizerUsage: '',
    pesticidesUsed: '',
    farmingExperience: '',
    sensorData: null
  });

  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  // Dropdown options
  const soilTypes = [
    'Alluvial Soil',
    'Black Cotton Soil',
    'Red Soil',
    'Laterite Soil',
    'Desert Soil',
    'Mountain Soil',
    'Clay Loam',
    'Sandy Loam'
  ];

  const irrigationTypes = [
    'Drip Irrigation',
    'Sprinkler Irrigation',
    'Flood Irrigation',
    'Furrow Irrigation',
    'Rain Fed',
    'Tube Well',
    'Canal Irrigation',
    'Tank Irrigation'
  ];

  const cropTypes = [
    'Wheat', 'Rice', 'Maize', 'Cotton', 'Sugarcane', 
    'Mustard', 'Chickpea', 'Soybean', 'Barley', 'Millet'
  ];

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Handle file upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setFormData(prev => ({
      ...prev,
      sensorData: file
    }));
  };

  // Form validation
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.location.trim()) newErrors.location = 'Location is required';
    if (!formData.mobile.trim()) newErrors.mobile = 'Mobile number is required';
    if (!formData.soilType) newErrors.soilType = 'Please select soil type';
    if (!formData.lastCrop) newErrors.lastCrop = 'Please specify last crop';
    if (!formData.irrigationType) newErrors.irrigationType = 'Please select irrigation type';
    if (!formData.farmSize.trim()) newErrors.farmSize = 'Farm size is required';
    
    // Email validation
    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    // Mobile number validation
    if (formData.mobile && !/^[+]?[0-9]{10,13}$/.test(formData.mobile.replace(/\s/g, ''))) {
      newErrors.mobile = 'Please enter a valid mobile number';
    }
    
    // Soil pH validation
    if (formData.soilPH && (formData.soilPH < 0 || formData.soilPH > 14)) {
      newErrors.soilPH = 'pH should be between 0-14';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    setSuccessMessage('');
    
    try {
      // Try to register farmer with MongoDB
      const result = await mongoService.registerFarmer(formData);
      
      if (result.success) {
        setSuccessMessage('Registration successful! Redirecting to dashboard...');
        
        // Store farmer data locally as backup
        localStorage.setItem('farmerData', JSON.stringify(result.data.farmer || formData));
        localStorage.setItem('userType', 'farmer');
        
        // Navigate to farmer dashboard after short delay
        setTimeout(() => {
          navigate('/farmer-dashboard');
        }, 2000);
      } else {
        // Fallback to localStorage if API fails
        console.warn('API registration failed, using localStorage:', result.error);
        
        localStorage.setItem('farmerData', JSON.stringify(formData));
        localStorage.setItem('userType', 'farmer');
        
        setSuccessMessage('Registration completed! Redirecting to dashboard...');
        setTimeout(() => {
          navigate('/farmer-dashboard');
        }, 1500);
      }
    } catch (error) {
      console.error('Registration error:', error);
      
      // Fallback to localStorage
      localStorage.setItem('farmerData', JSON.stringify(formData));
      localStorage.setItem('userType', 'farmer');
      
      setSuccessMessage('Registration completed! Redirecting to dashboard...');
      setTimeout(() => {
        navigate('/farmer-dashboard');
      }, 1500);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-50 to-accent-50 dark:from-secondary-900 dark:to-secondary-800">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-2xl mb-6 shadow-lg">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-secondary-900 dark:text-white mb-2">
            Farmer Registration
          </h1>
          <p className="text-lg text-secondary-600 dark:text-secondary-400">
            Join FasalNeeti and transform your farming with smart technology
          </p>
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="alert-success mb-6 animate-fade-in">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-primary-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span>{successMessage}</span>
            </div>
          </div>
        )}

        {/* Registration Form */}
        <div className="form-container animate-slide-up">
          <div className="relative z-10">
            <form onSubmit={handleSubmit} className="space-y-10">
            
            {/* Personal Information Section */}
            <div className="border-b border-primary-200 dark:border-secondary-700 pb-8">
              <h2 className="text-xl font-semibold text-secondary-900 dark:text-white mb-6 flex items-center">
                <div className="w-6 h-6 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center mr-3">
                  <svg className="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                Personal Information
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    className={`input-field ${errors.name ? 'border-red-500 focus:ring-red-500' : ''}`}
                    placeholder="Enter your full name"
                  />
                  {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className={`input-field ${errors.email ? 'border-red-500 focus:ring-red-500' : ''}`}
                    placeholder="farmer@example.com"
                  />
                  {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Mobile Number *
                  </label>
                  <input
                    type="tel"
                    name="mobile"
                    value={formData.mobile}
                    onChange={handleInputChange}
                    className={`input-field ${errors.mobile ? 'border-red-500 focus:ring-red-500' : ''}`}
                    placeholder="+91 98765 43210"
                  />
                  {errors.mobile && <p className="text-red-500 text-sm mt-1">{errors.mobile}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Location *
                  </label>
                  <input
                    type="text"
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    className={`input-field ${errors.location ? 'border-red-500 focus:ring-red-500' : ''}`}
                    placeholder="State, District, Village"
                  />
                  {errors.location && <p className="text-red-500 text-sm mt-1">{errors.location}</p>}
                </div>
              </div>
            </div>

            {/* Farming Information Section */}
            <div className="border-b border-primary-200 dark:border-secondary-700 pb-8">
              <h2 className="text-xl font-semibold text-secondary-900 dark:text-white mb-6 flex items-center">
                <div className="w-6 h-6 bg-accent-100 dark:bg-accent-900/20 rounded-lg flex items-center justify-center mr-3">
                  <svg className="w-4 h-4 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" />
                  </svg>
                </div>
                Farm Information
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Farm Size *
                  </label>
                  <input
                    type="text"
                    name="farmSize"
                    value={formData.farmSize}
                    onChange={handleInputChange}
                    className={`input-field ${errors.farmSize ? 'border-red-500 focus:ring-red-500' : ''}`}
                    placeholder="e.g., 2 acres, 5 hectares"
                  />
                  {errors.farmSize && <p className="text-red-500 text-sm mt-1">{errors.farmSize}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Soil Type *
                  </label>
                  <select
                    name="soilType"
                    value={formData.soilType}
                    onChange={handleInputChange}
                    className={`input-field ${errors.soilType ? 'border-red-500 focus:ring-red-500' : ''}`}
                  >
                    <option value="">Select soil type</option>
                    {soilTypes.map((type, index) => (
                      <option key={index} value={type}>{type}</option>
                    ))}
                  </select>
                  {errors.soilType && <p className="text-red-500 text-sm mt-1">{errors.soilType}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Soil pH (Optional)
                  </label>
                  <input
                    type="number"
                    name="soilPH"
                    value={formData.soilPH}
                    onChange={handleInputChange}
                    className={`input-field ${errors.soilPH ? 'border-red-500 focus:ring-red-500' : ''}`}
                    placeholder="6.0 - 8.0"
                    min="0"
                    max="14"
                    step="0.1"
                  />
                  {errors.soilPH && <p className="text-red-500 text-sm mt-1">{errors.soilPH}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Last Crop Grown *
                  </label>
                  <select
                    name="lastCrop"
                    value={formData.lastCrop}
                    onChange={handleInputChange}
                    className={`input-field ${errors.lastCrop ? 'border-red-500 focus:ring-red-500' : ''}`}
                  >
                    <option value="">Select crop</option>
                    {cropTypes.map((crop, index) => (
                      <option key={index} value={crop}>{crop}</option>
                    ))}
                  </select>
                  {errors.lastCrop && <p className="text-red-500 text-sm mt-1">{errors.lastCrop}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Irrigation Type *
                  </label>
                  <select
                    name="irrigationType"
                    value={formData.irrigationType}
                    onChange={handleInputChange}
                    className={`input-field ${errors.irrigationType ? 'border-red-500 focus:ring-red-500' : ''}`}
                  >
                    <option value="">Select irrigation type</option>
                    {irrigationTypes.map((type, index) => (
                      <option key={index} value={type}>{type}</option>
                    ))}
                  </select>
                  {errors.irrigationType && <p className="text-red-500 text-sm mt-1">{errors.irrigationType}</p>}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Farming Experience
                  </label>
                  <select
                    name="farmingExperience"
                    value={formData.farmingExperience}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    <option value="">Select experience</option>
                    <option value="Less than 1 year">Less than 1 year</option>
                    <option value="1-5 years">1-5 years</option>
                    <option value="5-10 years">5-10 years</option>
                    <option value="10-20 years">10-20 years</option>
                    <option value="More than 20 years">More than 20 years</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Fertilizer Usage
                  </label>
                  <input
                    type="text"
                    name="fertilizerUsage"
                    value={formData.fertilizerUsage}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="Organic, NPK, DAP, etc."
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-secondary-700 dark:text-secondary-300 mb-2">
                    Pesticide Usage
                  </label>
                  <input
                    type="text"
                    name="pesticidesUsed"
                    value={formData.pesticidesUsed}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="Organic, Chemical, or None"
                  />
                </div>
              </div>
            </div>

            {/* Optional Data Upload Section */}
            <div className="pb-8">
              <h2 className="text-xl font-semibold text-secondary-900 dark:text-white mb-6 flex items-center">
                <div className="w-6 h-6 bg-secondary-100 dark:bg-secondary-700 rounded-lg flex items-center justify-center mr-3">
                  <svg className="w-4 h-4 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                  </svg>
                </div>
                Additional Data (Optional)
              </h2>
              
              <div className="border-2 border-dashed border-primary-300 dark:border-secondary-600 rounded-lg p-8 text-center hover:border-primary-400 dark:hover:border-secondary-500 transition-colors duration-200">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  accept=".csv,.json,.xlsx,.jpg,.png,.pdf"
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center mb-4">
                    <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                    </svg>
                  </div>
                  <span className="text-secondary-700 dark:text-secondary-300 mb-2 font-medium">
                    Upload sensor data or crop images
                  </span>
                  <span className="text-sm text-secondary-500 dark:text-secondary-400">
                    Supported formats: CSV, JSON, Excel, Images, PDF
                  </span>
                </label>
                {formData.sensorData && (
                  <div className="mt-4 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                    <p className="text-primary-700 dark:text-primary-300 flex items-center justify-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      File uploaded: {formData.sensorData.name}
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex justify-center pt-8">
              <button
                type="submit"
                disabled={isLoading}
                className={`btn-primary text-lg px-12 py-4 flex items-center space-x-3 ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isLoading ? (
                  <>
                    <div className="spinner"></div>
                    <span>Creating Account...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <span>Create Account & Continue</span>
                  </>
                )}
              </button>
            </div>
            </form>
          </div>
        </div>

        {/* Support Information */}
        <div className="mt-8 text-center animate-fade-in">
          <div className="text-sm text-secondary-600 dark:text-secondary-400">
            Need help with registration? Contact us at{' '}
            <a 
              href="mailto:support@fasalneeti.com" 
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              support@fasalneeti.com
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FarmerLogin;
