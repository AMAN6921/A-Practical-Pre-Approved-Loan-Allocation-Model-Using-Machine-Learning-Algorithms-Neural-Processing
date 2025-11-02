// API service for Loan Prediction System
// Handles all communication with the Flask backend

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// API response interceptor for better error handling
const handleApiResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
};

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Helper method to make HTTP requests
  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      return await handleApiResponse(response);
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      
      // Check if it's a network error
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please check if the backend is running.');
      }
      
      throw error;
    }
  }

  // Check if backend is available
  async checkBackendHealth() {
    try {
      await this.healthCheck();
      return true;
    } catch (error) {
      console.warn('Backend health check failed:', error.message);
      return false;
    }
  }

  // Authentication methods
  async register(userData) {
    return this.makeRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials) {
    const response = await this.makeRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    // Store token in localStorage
    if (response.token) {
      localStorage.setItem('authToken', response.token);
    }

    return response;
  }

  logout() {
    localStorage.removeItem('authToken');
  }

  // Loan prediction methods
  async predictLoan(applicationData) {
    return this.makeRequest('/predict', {
      method: 'POST',
      body: JSON.stringify(applicationData),
    });
  }

  // Dashboard methods
  async getDashboardStats() {
    return this.makeRequest('/dashboard/stats');
  }

  async getMonthlyTrends(months = 6) {
    return this.makeRequest(`/dashboard/trends?months=${months}`);
  }

  async getModelPerformance() {
    return this.makeRequest('/dashboard/performance');
  }

  async getFeatureImportance(modelName = null) {
    const query = modelName ? `?model=${modelName}` : '';
    return this.makeRequest(`/dashboard/feature-importance${query}`);
  }

  // User application methods
  async getUserApplications() {
    return this.makeRequest('/applications');
  }

  async getApplicationDetails(applicationId) {
    return this.makeRequest(`/applications/${applicationId}`);
  }

  // Health check
  async healthCheck() {
    return this.makeRequest('/health');
  }

  // Utility methods
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  }

  getAuthToken() {
    return localStorage.getItem('authToken');
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

// Export individual methods for convenience
export const {
  register,
  login,
  logout,
  predictLoan,
  getDashboardStats,
  getMonthlyTrends,
  getModelPerformance,
  getFeatureImportance,
  getUserApplications,
  getApplicationDetails,
  healthCheck,
  isAuthenticated,
} = apiService;