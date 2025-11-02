// Email Configuration for Contact Form
// Update these values after setting up EmailJS

export const EMAIL_CONFIG = {
  // Get these from your EmailJS dashboard
  SERVICE_ID: 'service_3dpdxut',     // Replace with your EmailJS Service ID
  TEMPLATE_ID: 'aman.devrani6921@gmail.com',   // Replace with your EmailJS Template ID  
  PUBLIC_KEY: '7KpMznXGgl3ORtwU-',     // Replace with your EmailJS Public Key
  
  // Your email address (where messages will be sent)
  TO_EMAIL: 'aman.devrani6921@gmail.com',
  
  // Email settings
  SETTINGS: {
    // Show detailed success/error messages
    SHOW_DETAILED_MESSAGES: true,
    
    // Auto-clear form after successful submission
    AUTO_CLEAR_FORM: true,
    
    // How long to show status messages (milliseconds)
    STATUS_DISPLAY_TIME: 5000,
  }
};

// Quick setup instructions
export const SETUP_INSTRUCTIONS = {
  step1: "Go to https://www.emailjs.com/ and create account",
  step2: "Add Gmail service and connect your account", 
  step3: "Create email template with variables: {{from_name}}, {{from_email}}, {{subject}}, {{message}}",
  step4: "Copy Service ID, Template ID, and Public Key",
  step5: "Update the values above in this file",
  step6: "Test the contact form!"
};

// For development/testing - set to true to use console.log instead of real emails
export const DEV_MODE = false;