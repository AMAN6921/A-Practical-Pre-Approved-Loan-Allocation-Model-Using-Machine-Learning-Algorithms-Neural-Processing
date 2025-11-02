import { useState } from 'react';
import { motion } from 'framer-motion';
import emailjs from '@emailjs/browser';
import { EMAIL_CONFIG, DEV_MODE } from '../config/email';
import {
  Mail,
  Phone,
  MapPin,
  Send,
  MessageCircle,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  // EmailJS configuration from config file
  const { SERVICE_ID, TEMPLATE_ID, PUBLIC_KEY, TO_EMAIL, SETTINGS } = EMAIL_CONFIG;

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Development mode - just log to console
    if (DEV_MODE) {
      console.log('📧 DEV MODE - Email would be sent:', {
        to: TO_EMAIL,
        from: formData.email,
        subject: formData.subject,
        message: formData.message
      });

      setTimeout(() => {
        setSubmitStatus('success');
        if (SETTINGS.AUTO_CLEAR_FORM) {
          setFormData({ name: '', email: '', subject: '', message: '' });
        }
        setIsSubmitting(false);
        setTimeout(() => setSubmitStatus(null), SETTINGS.STATUS_DISPLAY_TIME);
      }, 1000);
      return;
    }

    try {
      // Check if EmailJS is configured
      if (SERVICE_ID === 'service_your_id' || TEMPLATE_ID === 'template_your_id') {
        throw new Error('EmailJS not configured. Please update src/config/email.js with your EmailJS credentials.');
      }

      // Send email using EmailJS
      const result = await emailjs.send(
        SERVICE_ID,
        TEMPLATE_ID,
        {
          from_name: formData.name,
          from_email: formData.email,
          subject: formData.subject,
          message: formData.message,
          to_email: TO_EMAIL,
          // Additional template variables
          reply_to: formData.email,
          timestamp: new Date().toLocaleString(),
        },
        PUBLIC_KEY
      );

      console.log('✅ Email sent successfully:', result);
      setSubmitStatus('success');

      if (SETTINGS.AUTO_CLEAR_FORM) {
        setFormData({ name: '', email: '', subject: '', message: '' });
      }

    } catch (error) {
      console.error('❌ Email sending failed:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
      // Reset status after configured time
      setTimeout(() => setSubmitStatus(null), SETTINGS.STATUS_DISPLAY_TIME);
    }
  };

  const contactInfo = [
    {
      icon: <Mail className="h-6 w-6" />,
      title: "Email Us",
      details: "aman.devrani6921@gmail.com",
      description: "Send us an email and we'll respond within 24 hours"
    },
    {
      icon: <Phone className="h-6 w-6" />,
      title: "Call Us",
      details: "+91 6398252586",
      description: "Available Monday to Friday, 9 AM to 6 PM EST"
    },
    {
      icon: <MapPin className="h-6 w-6" />,
      title: "Visit Us",
      details: "Graphic Era (Deemed to be University), Dehradun, Uttarakhand.",
      description: "Our headquarters in the heart of the university. :)"
    }
  ];

  const faqs = [
    {
      question: "How accurate are your loan predictions?",
      answer: "Our AI models achieve 94.5% accuracy using advanced machine learning algorithms trained on extensive financial datasets."
    },
    {
      question: "Is my financial data secure?",
      answer: "Yes, we use enterprise-grade security measures. Your data is encrypted and never stored permanently on our servers."
    },
    {
      question: "How long does the prediction process take?",
      answer: "Our AI can process your loan eligibility prediction in under 2 seconds, providing instant results."
    },
    {
      question: "What factors does your AI consider?",
      answer: "We analyze 11 key financial features including credit scores, payment history, debt ratios, and credit length among others."
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
          <MessageCircle className="h-16 w-16 text-primary-600 mx-auto mb-6" />
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Get in Touch
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Have questions about our AI loan prediction service? We're here to help.
            Reach out to our team for support, partnerships, or general inquiries.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-12 mb-16">
          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="card"
          >
            <h2 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
              Send us a Message
            </h2>

            {submitStatus === 'success' && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6 p-4 bg-success-50 border border-success-200 rounded-lg flex items-center"
              >
                <CheckCircle className="h-5 w-5 text-success-600 mr-3" />
                <span className="text-success-700">
                  ✅ Email sent successfully to {TO_EMAIL}! We'll get back to you soon.
                  {DEV_MODE && " (DEV MODE - No real email sent)"}
                </span>
              </motion.div>
            )}

            {submitStatus === 'error' && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center"
              >
                <AlertCircle className="h-5 w-5 text-red-600 mr-3" />
                <span className="text-red-700">❌ Failed to send email. Please try again or contact us directly.</span>
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="Bobby Lashley"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="input-field"
                    placeholder="bobby123@example.com"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Subject *
                </label>
                <select
                  name="subject"
                  value={formData.subject}
                  onChange={handleInputChange}
                  className="input-field"
                  required
                >
                  <option value="">Select a subject</option>
                  <option value="general">General Inquiry</option>
                  <option value="support">Technical Support</option>
                  <option value="partnership">Partnership Opportunity</option>
                  <option value="feedback">Feedback</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Message *
                </label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  rows={6}
                  className="input-field resize-none"
                  placeholder="Tell us how we can help you..."
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isSubmitting ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Sending...
                  </>
                ) : (
                  <>
                    <Send className="h-5 w-5 mr-2" />
                    Send Message
                  </>
                )}
              </button>
            </form>
          </motion.div>

          {/* Contact Information */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="space-y-8"
          >
            <div className="card">
              <h2 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
                Contact Information
              </h2>
              <div className="space-y-6">
                {contactInfo.map((info, index) => (
                  <div key={index} className="flex items-start">
                    <div className="text-primary-600 mr-4 mt-1">
                      {info.icon}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                        {info.title}
                      </h3>
                      <p className="text-primary-600 font-medium mb-1">
                        {info.details}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {info.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card">
              <div className="flex items-center mb-4">
                <Clock className="h-6 w-6 text-primary-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Business Hours
                </h3>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Monday - Friday</span>
                  <span className="text-gray-900 dark:text-white font-medium">9:00 AM - 6:00 PM EST</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Saturday</span>
                  <span className="text-gray-900 dark:text-white font-medium">10:00 AM - 4:00 PM EST</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Sunday</span>
                  <span className="text-gray-900 dark:text-white font-medium">Closed</span>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center mb-4">
                <AlertCircle className="h-6 w-6 text-primary-600 mr-3" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Response Time
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                We typically respond to all inquiries within 24 hours during business days.
                For urgent technical support, please call our support line directly.
              </p>
            </div>
          </motion.div>
        </div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="card"
        >
          <h2 className="text-2xl font-semibold mb-8 text-gray-900 dark:text-white text-center">
            Frequently Asked Questions
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {faqs.map((faq, index) => (
              <div key={index} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {faq.question}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Contact;