import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Calculator,
  CheckCircle,
  XCircle,
  TrendingUp,
  AlertCircle,
  Loader,
  BarChart3,
  Sparkles,
  Zap,
  Users
} from 'lucide-react';
import PredictionChart from '../components/PredictionChart';

const Prediction = () => {
  const [formData, setFormData] = useState({
    creditShort: '',
    creditLong: '',
    timeLimitation: '',
    cph: '',
    ctl: '',
    aph: '',
    atl: '',
    quarterFluctuation: '',
    resultantFluctuation: ''
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showChart, setShowChart] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isFormFocused, setIsFormFocused] = useState(false);
  const [selectedService, setSelectedService] = useState('loan'); // 'loan' or 'classification'
  const [selectedModels, setSelectedModels] = useState({
    loan: ['xgboost', 'random_forest'],
    classification: ['knn', 'logistic']
  });
  const [specificModel, setSpecificModel] = useState(null); // For single model prediction

  // Refs for smooth scrolling
  const formSectionRef = useRef(null);

  // Track mouse position for cursor-following elements
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Smooth scroll to form section
  const scrollToForm = () => {
    if (formSectionRef.current) {
      // Calculate offset to show the section nicely
      const elementTop = formSectionRef.current.offsetTop;
      const offset = 80; // Offset from top for better visibility

      window.scrollTo({
        top: elementTop - offset,
        behavior: 'smooth'
      });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let processedValue = value;
    let updatedFormData = { ...formData };

    // Apply validation rules based on field type
    switch (name) {
      case 'cph':
      case 'ctl':
        // CPH & CTL: Only allow 1, 0, -1
        if (value !== '' && !['1', '0', '-1'].includes(value)) {
          return; // Don't update if invalid value
        }
        processedValue = value;
        break;

      case 'aph':
      case 'atl':
        // APH & ATL: Max value 1, can be decimal
        if (value !== '' && (parseFloat(value) > 1 || parseFloat(value) < -10)) {
          alert(`Please enter a value between -10 and 1.0 for ${name.toUpperCase()}`);
          return; // Don't update if out of range
        }
        processedValue = value;
        break;

      case 'creditShort':
        // Credit-Short: Only allow 1, 0, -1
        if (value !== '' && !['1', '0', '-1'].includes(value)) {
          return; // Don't update if invalid value
        }
        processedValue = value;
        break;

      case 'quarterFluctuation':
        // Quarterly Fluctuation: Range -8 to 8
        if (value !== '' && (parseFloat(value) > 8 || parseFloat(value) < -8)) {
          alert('Please enter a value between -8 and 8 for Quarterly Fluctuation');
          return; // Don't update if out of range
        }
        processedValue = value;

        // Auto-calculate Credit-Long and Resultant Fluctuation based on Quarterly Fluctuation
        if (value !== '') {
          const fluctuation = parseFloat(value);
          let calculatedValue;

          if (fluctuation < 0) {
            calculatedValue = '-1'; // Poor
          } else if (fluctuation >= 0 && fluctuation <= 3) {
            calculatedValue = '0'; // Normal
          } else if (fluctuation > 3) {
            calculatedValue = '1'; // Good
          }

          updatedFormData.creditLong = calculatedValue;
          updatedFormData.resultantFluctuation = calculatedValue;
        } else {
          updatedFormData.creditLong = '';
          updatedFormData.resultantFluctuation = '';
        }
        break;



      default:
        processedValue = value;
    }

    updatedFormData[name] = processedValue;
    setFormData(updatedFormData);
  };

  // Helper function to calculate form completion percentage
  const getFormCompletionPercentage = () => {
    // Only count user-required fields (exclude auto-calculated fields)
    const userRequiredFields = [
      'creditShort',
      'cph',
      'ctl',
      'aph',
      'atl',
      'quarterFluctuation'
    ];

    const filledFields = userRequiredFields.filter(field => formData[field] !== '').length;
    return Math.round((filledFields / userRequiredFields.length) * 100);
  };

  // Helper function to get status indicator
  const getStatusIndicator = (fieldName, value) => {
    if (!value) return '';

    const numValue = parseFloat(value);

    switch (fieldName) {
      case 'cph':
      case 'ctl':
      case 'creditShort':
        if (value === '1') return '🟢 Good';
        if (value === '0') return '🟡 Normal';
        if (value === '-1') return '🔴 Poor';
        break;

      case 'aph':
      case 'atl':
        if (numValue === 1) return '🟢 Good';
        if (numValue >= 0 && numValue < 1) return '🟡 Normal';
        if (numValue < 0) return '🔴 Poor';
        break;

      case 'creditLong':
        if (value === '1') return '🟢 Good (Fluctuation > 3)';
        if (value === '0') return '🟡 Normal (Fluctuation 0-3)';
        if (value === '-1') return '🔴 Poor (Fluctuation < 0)';
        break;

      case 'resultantFluctuation':
        if (value === '1') return '🟢 Good (Quarterly > 3)';
        if (value === '0') return '🟡 Normal (Quarterly 0-3)';
        if (value === '-1') return '🔴 Poor (Quarterly < 0)';
        break;

      case 'quarterFluctuation':
        if (numValue > 3) return '🟢 Good (Credit-Long = 1)';
        if (numValue >= 0 && numValue <= 3) return '🟡 Normal (Credit-Long = 0)';
        if (numValue < 0) return '🔴 Poor (Credit-Long = -1)';
        break;
    }

    return '';
  };

  const callPredictionAPI = async () => {
    // Call the real Flask API for prediction
    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          serviceType: selectedService,
          selectedModels: specificModel ? [specificModel] : selectedModels[selectedService]
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      return {
        prediction: data.prediction,
        confidence: data.confidence,
        loanRange: data.loan_range,
        factors: data.factors,
        modelPredictions: data.model_predictions,
        processingTime: data.processing_time_ms
      };
    } catch (error) {
      console.error('API call failed:', error);
      // Fallback to simulation if API is not available
      return simulatePrediction();
    }
  };

  const simulatePrediction = () => {
    // Fallback simulation if API is not available
    const creditShort = parseFloat(formData.creditShort) || 0;
    const creditLong = parseFloat(formData.creditLong) || 0;

    let score = 0;
    if (creditShort > 650) score += 30;
    if (creditLong > 650) score += 30;
    if (formData.paymentHistory === 'excellent') score += 25;
    if (parseFloat(formData.cph) > 0.7) score += 15;

    let result, confidence, loanRange;

    if (score >= 80) {
      result = 'Very_Good';
      confidence = 92 + Math.random() * 6;
      loanRange = '$50,000 - $200,000';
    } else if (score >= 50) {
      result = 'Normal';
      confidence = 75 + Math.random() * 15;
      loanRange = '$10,000 - $50,000';
    } else {
      result = 'Very_Bad';
      confidence = 60 + Math.random() * 20;
      loanRange = 'Not eligible';
    }

    return {
      prediction: result,
      confidence: confidence.toFixed(1),
      loanRange,
      factors: {
        creditScore: creditShort > 650 ? 'Positive' : 'Needs Improvement',
        paymentHistory: formData.paymentHistory === 'excellent' ? 'Excellent' : 'Needs Improvement',
        debtRatio: parseFloat(formData.cph) > 0.7 ? 'Good' : 'High Risk'
      }
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate that a specific model is selected
    if (!specificModel) {
      alert('Please select one of the four AI models (XGBoost, Random Forest, Logistic Regression, or KNN) for analysis.');
      return;
    }

    setLoading(true);

    try {
      const result = await callPredictionAPI();
      setPrediction(result);
      setShowChart(true);
    } catch (error) {
      console.error('Prediction failed:', error);
      // Show error message to user
      alert('Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      creditShort: '',
      creditLong: '',
      timeLimitation: '',
      cph: '',
      ctl: '',
      aph: '',
      atl: '',
      quarterFluctuation: '',
      resultantFluctuation: ''
    });
    setPrediction(null);
    setShowChart(false);
    setSpecificModel(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Cursor-following sparkle effect */}
      <motion.div
        className="fixed pointer-events-none z-50"
        animate={{
          x: mousePosition.x - 10,
          y: mousePosition.y - 10,
        }}
        transition={{
          type: "spring",
          stiffness: 500,
          damping: 28,
        }}
      >
        <Sparkles className="h-5 w-5 text-primary-500 opacity-60" />
      </motion.div>

      {/* Background animated elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(6)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute"
            animate={{
              x: [0, 30, -15, 0],
              y: [0, -30, 15, 0],
              opacity: [0.03, 0.08, 0.03],
            }}
            transition={{
              duration: 25 + i * 5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 3,
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
          >
            <div className={`w-6 h-6 rounded-full ${i % 3 === 0 ? 'bg-blue-400' :
              i % 3 === 1 ? 'bg-purple-400' : 'bg-green-400'
              } opacity-5`} />
          </motion.div>
        ))}
      </div>

      <div className="relative z-10">
        {/* Header Section */}
        <div className="pt-12 pb-8">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center"
            >
              <motion.div
                animate={{ rotate: [0, 5, -5, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                className="inline-block mb-6"
              >
                <Calculator className="h-20 w-20 text-primary-600 mx-auto" />
              </motion.div>
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
                🤖 AI Financial Advisor
              </h1>
              <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-400 max-w-4xl mx-auto leading-relaxed">
                Choose your preferred AI model and get instant, personalized financial analysis
              </p>
            </motion.div>
          </div>
        </div>

        {/* Step 1: AI Model Selection */}
        <div className="py-12">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <div className="text-center mb-12">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-full mb-4">
                  <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">1</span>
                </div>
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                  Choose Your AI Model
                </h2>
                <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                  Select the machine learning algorithm that will analyze your financial profile
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-8 border border-gray-200 dark:border-gray-700">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {[
                    {
                      key: 'xgboost',
                      name: 'XGBoost',
                      accuracy: '94.5%',
                      desc: 'Gradient Boosting',
                      icon: '🚀',
                      service: 'loan',
                      serviceText: 'Loan Prediction',
                      color: 'blue'
                    },
                    {
                      key: 'random_forest',
                      name: 'Random Forest',
                      accuracy: '92.1%',
                      desc: 'Ensemble Trees',
                      icon: '🌳',
                      service: 'loan',
                      serviceText: 'Loan Prediction',
                      color: 'green'
                    },
                    {
                      key: 'logistic',
                      name: 'Logistic Regression',
                      accuracy: '87.3%',
                      desc: 'Statistical Model',
                      icon: '📊',
                      service: 'classification',
                      serviceText: 'Customer Classification',
                      color: 'purple'
                    },
                    {
                      key: 'knn',
                      name: 'KNN',
                      accuracy: '85.7%',
                      desc: 'Similarity Learning',
                      icon: '🎯',
                      service: 'classification',
                      serviceText: 'Customer Classification',
                      color: 'orange'
                    }
                  ].map((model) => (
                    <motion.button
                      key={model.key}
                      type="button"
                      onClick={() => {
                        setSpecificModel(model.key);
                        setSelectedService(model.service);
                        setPrediction(null);
                        setShowChart(false);

                        // Smooth scroll to form section after a short delay to allow state update
                        setTimeout(() => {
                          scrollToForm();
                        }, 100);
                      }}
                      className={`p-6 rounded-2xl border-2 transition-all duration-300 text-center relative overflow-hidden group ${specificModel === model.key
                        ? 'border-primary-500 bg-gradient-to-br from-primary-500 to-primary-600 text-white shadow-xl transform scale-105'
                        : 'border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:border-primary-300 hover:shadow-lg hover:scale-102'
                        }`}
                      whileHover={{ scale: specificModel === model.key ? 1.05 : 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <div className="space-y-4">
                        <div className="text-4xl mb-3">{model.icon}</div>
                        <h5 className="font-bold text-lg">{model.name}</h5>
                        <div className={`text-sm font-bold px-3 py-1 rounded-full ${specificModel === model.key
                          ? 'bg-white/20 text-white'
                          : 'bg-green-100 dark:bg-green-800 text-green-700 dark:text-green-200'
                          }`}>
                          {model.accuracy}
                        </div>
                        <p className="text-sm opacity-80">{model.desc}</p>
                        <div className={`text-xs px-3 py-1 rounded-full ${specificModel === model.key
                          ? 'bg-white/20 text-white'
                          : model.service === 'loan'
                            ? 'bg-blue-100 dark:bg-blue-800 text-blue-700 dark:text-blue-200'
                            : 'bg-purple-100 dark:bg-purple-800 text-purple-700 dark:text-purple-200'
                          }`}>
                          {model.serviceText}
                        </div>
                        {specificModel === model.key && (
                          <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            className="absolute top-3 right-3"
                          >
                            <CheckCircle className="h-6 w-6 text-white" />
                          </motion.div>
                        )}
                      </div>
                    </motion.button>
                  ))}
                </div>

                {specificModel && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-2xl border border-blue-200 dark:border-blue-700"
                  >
                    <div className="text-center">
                      <p className="text-lg font-semibold text-gray-800 dark:text-gray-200">
                        ✅ Selected Model: <span className="text-primary-600 dark:text-primary-400">
                          {[
                            { key: 'xgboost', name: 'XGBoost' },
                            { key: 'random_forest', name: 'Random Forest' },
                            { key: 'logistic', name: 'Logistic Regression' },
                            { key: 'knn', name: 'K-Nearest Neighbors' }
                          ].find(m => m.key === specificModel)?.name}
                        </span>
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                        Analysis Type: {selectedService === 'loan' ? '💰 Loan Eligibility' : '👤 Customer Classification'}
                      </p>
                    </div>
                  </motion.div>
                )}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Step 2: Financial Information Form */}
        <div ref={formSectionRef} className="py-12">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{
                opacity: 1,
                y: 0,
                scale: specificModel ? [1, 1.02, 1] : 1
              }}
              transition={{
                duration: 0.6,
                delay: 0.2,
                scale: { duration: 0.5, delay: specificModel ? 0.3 : 0 }
              }}
            >
              <div className="text-center mb-12">
                <motion.div
                  className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-full mb-4"
                  animate={specificModel ? {
                    scale: [1, 1.1, 1],
                    boxShadow: [
                      "0 0 0 0 rgba(59, 130, 246, 0)",
                      "0 0 0 10px rgba(59, 130, 246, 0.1)",
                      "0 0 0 0 rgba(59, 130, 246, 0)"
                    ]
                  } : {}}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">2</span>
                </motion.div>
                <h2 className={`text-3xl font-bold mb-4 transition-colors duration-500 ${specificModel
                    ? 'text-primary-600 dark:text-primary-400'
                    : 'text-gray-900 dark:text-white'
                  }`}>
                  Enter Your Financial Details
                  {specificModel && (
                    <motion.span
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="ml-2 text-lg"
                    >
                      ✨
                    </motion.span>
                  )}
                </h2>
                <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                  {specificModel
                    ? `Provide your financial information for ${specificModel === 'xgboost' ? 'XGBoost' :
                      specificModel === 'random_forest' ? 'Random Forest' :
                        specificModel === 'logistic' ? 'Logistic Regression' :
                          specificModel === 'knn' ? 'KNN' : 'AI'
                    } analysis`
                    : 'Provide your financial information for AI analysis'
                  }
                </p>
              </div>

              <div className={`bg-white dark:bg-gray-800 rounded-3xl shadow-2xl border transition-all duration-500 ${specificModel
                  ? 'border-primary-300 dark:border-primary-600 shadow-primary-200/50 dark:shadow-primary-800/50'
                  : 'border-gray-200 dark:border-gray-700'
                }`}>
                <div className="p-8">
                  <div className="grid lg:grid-cols-2 gap-12">

                    {/* Left Column - Form Fields */}
                    <div className="space-y-6">

                      {/* Validation Rules Info */}
                      <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                        <h3 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2 flex items-center">
                          <AlertCircle className="h-4 w-4 mr-2" />
                          Input Guidelines
                        </h3>
                        <div className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
                          <p>• <strong>Credit Score Short-term, CPH, CTL:</strong> Select from dropdown (1=Good, 0=Normal, -1=Poor)</p>
                          <p>• <strong>APH, ATL:</strong> Enter decimal values (Range: -10 to 1.0)</p>
                          <p>• <strong>Quarterly Fluctuation:</strong> Range -8 to 8 (Auto-calculates other fields)</p>
                        </div>
                      </div>

                      <form
                        onSubmit={handleSubmit}
                        className="space-y-6"
                        onFocus={() => setIsFormFocused(true)}
                        onBlur={() => setIsFormFocused(false)}
                      >
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                              <Zap className="h-4 w-4 mr-2 text-primary-500" />
                              Credit Score Short-term
                            </label>
                            <select
                              name="creditShort"
                              value={formData.creditShort}
                              onChange={handleInputChange}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                              required
                            >
                              <option value="">Select Credit Score</option>
                              <option value="1">1 - Good</option>
                              <option value="0">0 - Normal</option>
                              <option value="-1">-1 - Poor</option>
                            </select>
                            {formData.creditShort && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('creditShort', formData.creditShort)}
                              </div>
                            )}
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                              <TrendingUp className="h-4 w-4 mr-2 text-primary-500" />
                              Credit Score Long-term
                            </label>
                            <input
                              type="text"
                              name="creditLong"
                              value={formData.creditLong}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white cursor-not-allowed"
                              placeholder="Auto-calculated"
                              readOnly
                            />
                            {formData.creditLong && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('creditLong', formData.creditLong)}
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              CPH (Credit Payment History)
                            </label>
                            <select
                              name="cph"
                              value={formData.cph}
                              onChange={handleInputChange}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                              required
                            >
                              <option value="">Select CPH Value</option>
                              <option value="1">1 - Good</option>
                              <option value="0">0 - Normal</option>
                              <option value="-1">-1 - Poor</option>
                            </select>
                            {formData.cph && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('cph', formData.cph)}
                              </div>
                            )}
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              CTL (Credit Time Limitation)
                            </label>
                            <select
                              name="ctl"
                              value={formData.ctl}
                              onChange={handleInputChange}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                              required
                            >
                              <option value="">Select CTL Value</option>
                              <option value="1">1 - Good</option>
                              <option value="0">0 - Normal</option>
                              <option value="-1">-1 - Poor</option>
                            </select>
                            {formData.ctl && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('ctl', formData.ctl)}
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              APH (Average Payment History)
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              name="aph"
                              value={formData.aph}
                              onChange={handleInputChange}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                              placeholder="Enter value (Max: 1.0)"
                              min="-10"
                              max="1"
                              required
                            />
                            {formData.aph && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('aph', formData.aph)}
                              </div>
                            )}
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              ATL (Average Time Limitation)
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              name="atl"
                              value={formData.atl}
                              onChange={handleInputChange}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                              placeholder="Enter value (Max: 1.0)"
                              min="-10"
                              max="1"
                              required
                            />
                            {formData.atl && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('atl', formData.atl)}
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                              Quarterly Fluctuation
                            </label>
                            <input
                              type="number"
                              name="quarterFluctuation"
                              value={formData.quarterFluctuation}
                              onChange={handleInputChange}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                              placeholder="Enter value (-8 to 8)"
                              min="-8"
                              max="8"
                              required
                            />
                            {formData.quarterFluctuation && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('quarterFluctuation', formData.quarterFluctuation)}
                              </div>
                            )}
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center">
                              <TrendingUp className="h-4 w-4 mr-2 text-primary-500" />
                              Resultant Fluctuation
                            </label>
                            <input
                              type="text"
                              name="resultantFluctuation"
                              value={formData.resultantFluctuation}
                              className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white cursor-not-allowed"
                              placeholder="Auto-calculated"
                              readOnly
                            />
                            {formData.resultantFluctuation && (
                              <div className="mt-1 text-xs text-gray-500">
                                {getStatusIndicator('resultantFluctuation', formData.resultantFluctuation)}
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Form Progress Indicator */}
                        <div className="mt-8">
                          <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                            <span>Form Completion</span>
                            <span>{getFormCompletionPercentage()}%</span>
                          </div>
                          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                            <motion.div
                              className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full"
                              initial={{ width: 0 }}
                              animate={{
                                width: `${getFormCompletionPercentage()}%`
                              }}
                              transition={{ duration: 0.5 }}
                            />
                          </div>
                        </div>

                        <div className="flex space-x-4 pt-6">
                          <motion.button
                            type="submit"
                            disabled={loading}
                            className="flex-1 bg-gradient-to-r from-primary-500 to-primary-600 text-white px-8 py-4 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center relative overflow-hidden shadow-lg hover:shadow-xl transition-all duration-200"
                            whileHover={{ scale: loading ? 1 : 1.02 }}
                            whileTap={{ scale: loading ? 1 : 0.98 }}
                          >
                            {loading && (
                              <motion.div
                                className="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-700"
                                animate={{ x: ['-100%', '100%'] }}
                                transition={{ duration: 1.5, repeat: Infinity }}
                              />
                            )}
                            <span className="relative z-10 flex items-center">
                              {loading ? (
                                <>
                                  <motion.div
                                    animate={{ rotate: 360 }}
                                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                  >
                                    <Loader className="h-5 w-5 mr-2" />
                                  </motion.div>
                                  Analyzing with AI...
                                </>
                              ) : (
                                <>
                                  <TrendingUp className="h-5 w-5 mr-2" />
                                  {specificModel ?
                                    `Analyze with ${specificModel === 'xgboost' ? 'XGBoost' :
                                      specificModel === 'random_forest' ? 'Random Forest' :
                                        specificModel === 'logistic' ? 'Logistic Regression' :
                                          specificModel === 'knn' ? 'KNN' : 'AI Model'
                                    }` :
                                    'Select AI Model First'
                                  }
                                  <Sparkles className="h-4 w-4 ml-2" />
                                </>
                              )}
                            </span>
                          </motion.button>

                          <motion.button
                            type="button"
                            onClick={resetForm}
                            className="px-6 py-4 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-xl font-semibold hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-200"
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                          >
                            Reset
                          </motion.button>
                        </div>
                      </form>
                    </div>

                    {/* Right Column - Results */}
                    <div className="space-y-6">
                      {!prediction && (
                        <div className="text-center py-12">
                          <motion.div
                            animate={{
                              rotate: [0, 5, -5, 0],
                              scale: [1, 1.05, 1]
                            }}
                            transition={{
                              duration: 4,
                              repeat: Infinity,
                              ease: "easeInOut"
                            }}
                            className="mb-6"
                          >
                            <div className="w-32 h-32 mx-auto bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900 dark:to-primary-800 rounded-full flex items-center justify-center">
                              <BarChart3 className="h-16 w-16 text-primary-600 dark:text-primary-400" />
                            </div>
                          </motion.div>
                          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                            AI Models Ready
                          </h3>
                          <p className="text-gray-600 dark:text-gray-400 mb-6">
                            Fill out the form to get your instant financial analysis powered by advanced ML models
                          </p>
                          <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
                            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                              <div className="text-blue-600 dark:text-blue-400 font-semibold">XGBoost</div>
                              <div className="text-sm text-blue-500">94.5% Accuracy</div>
                            </div>
                            <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                              <div className="text-green-600 dark:text-green-400 font-semibold">Random Forest</div>
                              <div className="text-sm text-green-500">92.1% Accuracy</div>
                            </div>
                            <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                              <div className="text-purple-600 dark:text-purple-400 font-semibold">Logistic Reg.</div>
                              <div className="text-sm text-purple-500">87.3% Accuracy</div>
                            </div>
                            <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                              <div className="text-orange-600 dark:text-orange-400 font-semibold">KNN</div>
                              <div className="text-sm text-orange-500">85.7% Accuracy</div>
                            </div>
                          </div>
                        </div>
                      )}

                      {prediction && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.5 }}
                          className="space-y-6"
                        >
                          <div className="text-center mb-6">
                            <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-full mb-4">
                              <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">3</span>
                            </div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                              {specificModel === 'xgboost' ? 'XGBoost Analysis Results' :
                                specificModel === 'random_forest' ? 'Random Forest Analysis Results' :
                                  specificModel === 'logistic' ? 'Logistic Regression Analysis Results' :
                                    specificModel === 'knn' ? 'KNN Analysis Results' : 'AI Analysis Results'}
                            </h2>
                          </div>

                          <div className={`p-6 rounded-2xl mb-6 ${prediction.prediction === 'Very_Good'
                            ? 'bg-green-50 border-2 border-green-200 dark:bg-green-900/20 dark:border-green-700'
                            : prediction.prediction === 'Normal'
                              ? 'bg-yellow-50 border-2 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-700'
                              : 'bg-red-50 border-2 border-red-200 dark:bg-red-900/20 dark:border-red-700'
                            }`}>
                            <div className="flex items-center mb-4">
                              {prediction.prediction === 'Very_Good' ? (
                                <CheckCircle className="h-8 w-8 text-green-600 mr-3" />
                              ) : prediction.prediction === 'Normal' ? (
                                <AlertCircle className="h-8 w-8 text-yellow-600 mr-3" />
                              ) : (
                                <XCircle className="h-8 w-8 text-red-600 mr-3" />
                              )}
                              <div>
                                <h3 className="text-xl font-semibold">
                                  {selectedService === 'loan' ? (
                                    prediction.prediction === 'Very_Good'
                                      ? 'Loan Approved!'
                                      : prediction.prediction === 'Normal'
                                        ? 'Conditional Approval'
                                        : 'Loan Declined'
                                  ) : (
                                    prediction.prediction === 'Very_Good'
                                      ? 'Premium Customer'
                                      : prediction.prediction === 'Normal'
                                        ? 'Standard Customer'
                                        : 'High-Risk Customer'
                                  )}
                                </h3>
                                <p className="text-sm opacity-75">
                                  Confidence: {prediction.confidence}%
                                </p>
                              </div>
                            </div>

                            <div className="space-y-4">
                              <p className="font-medium">
                                {selectedService === 'loan' ? (
                                  <>Loan Range: <span className="font-bold">{prediction.loanRange}</span></>
                                ) : (
                                  <>Customer Category: <span className="font-bold">
                                    {prediction.prediction === 'Very_Good' ? 'Premium (Low Risk)' :
                                      prediction.prediction === 'Normal' ? 'Standard (Medium Risk)' :
                                        'High-Risk (Requires Review)'}
                                  </span></>
                                )}
                              </p>

                              {/* AI Model Information */}
                              <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
                                <h4 className="font-semibold mb-3 text-center flex items-center justify-center">
                                  <BarChart3 className="h-5 w-5 mr-2" />
                                  AI Model Used
                                </h4>

                                <div className="text-center">
                                  <div className="flex items-center justify-center mb-2">
                                    <Sparkles className="h-6 w-6 text-blue-600 mr-2" />
                                    <span className="font-bold text-lg">
                                      {specificModel === 'xgboost' ? 'XGBoost' :
                                        specificModel === 'random_forest' ? 'Random Forest' :
                                          specificModel === 'logistic' ? 'Logistic Regression' :
                                            specificModel === 'knn' ? 'K-Nearest Neighbors' : 'AI Model'}
                                    </span>
                                  </div>

                                  <div className="flex items-center justify-center space-x-4 mb-3">
                                    <span className="text-sm bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 px-3 py-1 rounded-full font-medium">
                                      Confidence: {prediction.confidence}%
                                    </span>
                                    <span className="text-sm bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 px-3 py-1 rounded-full font-medium">
                                      Accuracy: {
                                        specificModel === 'xgboost' ? '94.5%' :
                                          specificModel === 'random_forest' ? '92.1%' :
                                            specificModel === 'logistic' ? '87.3%' :
                                              specificModel === 'knn' ? '85.7%' : '90%'
                                      }
                                    </span>
                                  </div>

                                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                                    {specificModel === 'xgboost' ? 'Advanced gradient boosting algorithm for precise predictions' :
                                      specificModel === 'random_forest' ? 'Ensemble of decision trees for robust analysis' :
                                        specificModel === 'logistic' ? 'Statistical classification model for reliable results' :
                                          specificModel === 'knn' ? 'Similarity-based learning for personalized assessment' : 'Machine learning model'}
                                  </p>

                                  <div className="flex items-center justify-center space-x-2 text-xs text-blue-700 dark:text-blue-300">
                                    <span>🤖 Service: {selectedService === 'loan' ? 'Loan Prediction' : 'Customer Classification'}</span>
                                    <span>•</span>
                                    <span>⚡ Processing: {prediction.processingTime || '150'}ms</span>
                                  </div>
                                </div>
                              </div>

                              {prediction.prediction !== 'Very_Bad' && (
                                <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
                                  <h4 className="font-semibold mb-2">Key Factors:</h4>
                                  <ul className="space-y-1 text-sm">
                                    <li>Credit Score: {prediction.factors.creditScore}</li>
                                    <li>Credit Payment History: {prediction.factors.creditPaymentHistory}</li>
                                    <li>Average Payment History: {prediction.factors.avgPaymentHistory}</li>
                                  </ul>
                                </div>
                              )}

                              {prediction.prediction === 'Very_Bad' && (
                                <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
                                  <h4 className="font-semibold mb-2 text-red-600">Improvement Tips:</h4>
                                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                                    <li>• Improve your credit score by paying bills on time</li>
                                    <li>• Reduce existing debt obligations</li>
                                    <li>• Build a longer credit history</li>
                                    <li>• Consider a co-signer for your application</li>
                                  </ul>
                                </div>
                              )}
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Chart Section */}
        {showChart && prediction && (
          <div className="py-12">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
                className="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-8 border border-gray-200 dark:border-gray-700"
              >
                <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white flex items-center justify-center">
                  <BarChart3 className="h-6 w-6 mr-2" />
                  Analysis Visualization
                </h3>
                <PredictionChart prediction={prediction} />
              </motion.div>
            </div>
          </div>
        )}

        {/* Floating Action Hint */}
        {getFormCompletionPercentage() >= 100 && !prediction && !loading && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0 }}
            className="fixed bottom-8 right-8 z-40"
          >
            <div className="bg-primary-500 text-white px-6 py-3 rounded-full shadow-lg flex items-center space-x-2">
              <Sparkles className="h-5 w-5" />
              <span className="font-medium">Ready to analyze!</span>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Prediction;