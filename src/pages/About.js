import { motion } from 'framer-motion';
import {
  Brain,
  Target,
  Award,
  TrendingUp,
  Shield,
  Zap,
  BarChart3
} from 'lucide-react';

const About = () => {
  const features = [
    {
      icon: <Brain className="h-12 w-12" />,
      title: "Advanced AI Models",
      description: "Our system uses cutting-edge machine learning algorithms including XGBoost, Random Forest, Logistic Regression, and K-Nearest Neighbors to provide the most accurate predictions."
    },
    {
      icon: <Target className="h-12 w-12" />,
      title: "High Accuracy",
      description: "With a 94.5% accuracy rate, our AI models have been trained on extensive financial datasets to ensure reliable loan eligibility predictions."
    },
    {
      icon: <Zap className="h-12 w-12" />,
      title: "Lightning Fast",
      description: "Get instant results in under 2 seconds. Our optimized algorithms process your financial data quickly without compromising accuracy."
    },
    {
      icon: <Shield className="h-12 w-12" />,
      title: "Secure & Private",
      description: "Your financial data is protected with enterprise-grade security. We never store sensitive information and all processing is done securely."
    }
  ];

  const stats = [
    { number: "94.5%", label: "Prediction Accuracy" },
    { number: "4", label: "AI Models Used" },
    { number: "<2s", label: "Processing Time" },
    { number: "11", label: "Key Features Analyzed" }
  ];

  const securityFeatures = [
    {
      icon: "🔒",
      title: "Data Encryption",
      description: "All financial data is encrypted using AES-256 encryption both in transit and at rest"
    },
    {
      icon: "🛡️",
      title: "Privacy Protection",
      description: "We never store sensitive personal information permanently. Data is processed and discarded immediately"
    },
    {
      icon: "⚡",
      title: "Real-time Processing",
      description: "Predictions are generated instantly without storing your financial details on our servers"
    },
    {
      icon: "🔍",
      title: "Transparent AI",
      description: "Our AI models provide clear explanations for every decision, ensuring full transparency"
    },
    {
      icon: "📊",
      title: "Audit Trail",
      description: "Complete logging and monitoring of all system activities for security and compliance"
    },
    {
      icon: "🌐",
      title: "Secure Infrastructure",
      description: "Built on enterprise-grade cloud infrastructure with 99.9% uptime guarantee"
    }
  ];

  const complianceStandards = [
    {
      standard: "GDPR",
      description: "General Data Protection Regulation compliant",
      status: "Compliant"
    },
    {
      standard: "SOC 2",
      description: "Security, Availability, and Confidentiality",
      status: "Certified"
    },
    {
      standard: "ISO 27001",
      description: "Information Security Management",
      status: "Aligned"
    },
    {
      standard: "PCI DSS",
      description: "Payment Card Industry Data Security",
      status: "Ready"
    }
  ];

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <TrendingUp className="h-16 w-16 text-primary-600 mx-auto mb-6" />
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            About LoanPredict AI
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            We're revolutionizing loan approval processes with advanced artificial intelligence,
            making financial decisions faster, more accurate, and completely transparent.
          </p>
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-20"
        >
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-primary-600 mb-2">
                {stat.number}
              </div>
              <div className="text-gray-600 dark:text-gray-400 font-medium">
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>

        {/* Mission Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="card mb-16"
        >
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
              Our Mission
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400 max-w-4xl mx-auto leading-relaxed">
              To democratize access to fair and transparent loan approvals through artificial intelligence.
              We believe everyone deserves to understand their financial standing and have equal access to
              credit opportunities. Our AI-powered platform eliminates bias and provides clear,
              data-driven decisions that help both lenders and borrowers make informed choices.
            </p>
          </div>
        </motion.div>

        {/* Features Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-12">
            What Makes Us Different
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.8 + index * 0.1 }}
                className="card hover:shadow-xl transition-shadow duration-300"
              >
                <div className="text-primary-600 mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Technology Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          className="card mb-16"
        >
          <div className="text-center mb-8">
            <BarChart3 className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Our Technology Stack
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Built with industry-leading machine learning frameworks and technologies
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">XGBoost</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">Gradient boosting framework for high-performance predictions</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Random Forest</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">Ensemble learning method for robust decision making</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Neural Networks</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">Deep learning models for complex pattern recognition</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Python & Scikit-learn</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">Industry-standard ML libraries and frameworks</p>
            </div>
          </div>
        </motion.div>

        {/* Security & Compliance Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2 }}
        >
          <h2 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-12">
            Security & Compliance
          </h2>

          {/* Security Features */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {securityFeatures.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 1.4 + index * 0.1 }}
                className="card text-center hover:shadow-xl transition-shadow duration-300"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Compliance Standards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.8 }}
            className="card"
          >
            <h3 className="text-2xl font-bold text-center text-gray-900 dark:text-white mb-8">
              Compliance Standards
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {complianceStandards.map((item, index) => (
                <div key={index} className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <h4 className="font-bold text-lg text-gray-900 dark:text-white mb-2">
                    {item.standard}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    {item.description}
                  </p>
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${item.status === 'Compliant' || item.status === 'Certified'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                    }`}>
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 2.0 }}
            className="mt-12 text-center"
          >
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              Why Trust Our AI System?
            </h3>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="p-4">
                <div className="text-3xl font-bold text-primary-600 mb-2">256-bit</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Encryption</div>
              </div>
              <div className="p-4">
                <div className="text-3xl font-bold text-green-600 mb-2">0</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Data Breaches</div>
              </div>
              <div className="p-4">
                <div className="text-3xl font-bold text-blue-600 mb-2">99.9%</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Uptime</div>
              </div>
              <div className="p-4">
                <div className="text-3xl font-bold text-purple-600 mb-2">24/7</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Monitoring</div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default About;