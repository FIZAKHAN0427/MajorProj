import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * Admin Login Component
 * Simple authentication for admin access
 */
const AdminLogin = () => {
  const navigate = useNavigate();
  
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Clear error when user types
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simple authentication (in real app, this would be server-side)
      if (credentials.username === 'admin' && credentials.password === 'admin123') {
        localStorage.setItem('adminData', JSON.stringify({
          username: credentials.username,
          role: 'admin',
          loginTime: new Date().toISOString()
        }));
        localStorage.setItem('userType', 'admin');
        navigate('/admin-dashboard');
      } else {
        setError('Invalid username or password');
      }
    } catch (error) {
      setError('Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-earth-50 to-crop-50 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-md w-full space-y-8">
        
        {/* Header */}
        <div className="text-center fade-in">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-earth-500 to-crop-500 rounded-full mb-4">
            <span className="text-2xl">👨‍💼</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Admin Login
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            प्रशासक लॉगिन - Access administrative dashboard
          </p>
        </div>

        {/* Login Form */}
        <div className="card p-8 slide-in">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Error Message */}
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <div className="flex items-center">
                  <span className="text-red-500 mr-2">⚠️</span>
                  <span className="text-red-700 dark:text-red-400">{error}</span>
                </div>
              </div>
            )}

            {/* Username Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Username
              </label>
              <input
                type="text"
                name="username"
                value={credentials.username}
                onChange={handleInputChange}
                className="input-field"
                placeholder="Enter admin username"
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={credentials.password}
                onChange={handleInputChange}
                className="input-field"
                placeholder="Enter admin password"
                required
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full btn-primary flex items-center justify-center space-x-3 ${
                isLoading ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Logging in...</span>
                </>
              ) : (
                <>
                  <span>🔐</span>
                  <span>Access Dashboard</span>
                </>
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <h3 className="font-semibold text-blue-800 dark:text-blue-400 mb-2">Demo Credentials:</h3>
            <div className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
              <div><strong>Username:</strong> admin</div>
              <div><strong>Password:</strong> admin123</div>
            </div>
          </div>
        </div>

        {/* Help Section */}
        <div className="text-center fade-in">
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Need help accessing the admin panel?
          </p>
          <div className="flex justify-center space-x-6">
            <a href="mailto:admin@fasalneeti.com" className="text-earth-600 hover:text-earth-700 flex items-center">
              <span className="mr-1">✉️</span>
              admin@fasalneeti.com
            </a>
            <a href="tel:+911800654321" className="text-earth-600 hover:text-earth-700 flex items-center">
              <span className="mr-1">📞</span>
              1800-654-321
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
