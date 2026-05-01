// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Navigation
function navigateTo(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show target section
    document.getElementById(sectionId).classList.add('active');
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
        }
    });
    
    // Load dashboard data if navigating to dashboard
    if (sectionId === 'dashboard') {
        loadDashboard();
    }
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Setup navigation listeners
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('href').substring(1);
            navigateTo(sectionId);
        });
    });
    
    // Setup form submission
    const form = document.getElementById('loanForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

// Form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        creditShort: parseFloat(formData.get('creditShort')),
        creditLong: parseFloat(formData.get('creditLong')),
        cph: parseFloat(formData.get('cph')),
        ctl: parseFloat(formData.get('ctl')),
        aph: parseFloat(formData.get('aph')),
        atl: parseFloat(formData.get('atl')),
        quarterFluctuation: parseFloat(formData.get('quarterFluctuation')),
        requestedAmount: parseFloat(formData.get('requestedAmount')),
        loanPurpose: formData.get('loanPurpose'),
        employmentStatus: formData.get('employmentStatus'),
        serviceType: 'loan',
        selectedModels: ['xgboost', 'random_forest', 'logistic', 'knn']
    };
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Prediction failed');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get prediction. Please make sure the backend server is running.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// Display results
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const resultCard = document.getElementById('resultCard');
    const assessmentLayout = document.querySelector('.assessment-layout');
    
    // Show two-column layout
    assessmentLayout.classList.remove('centered');
    
    // Determine result type
    const prediction = data.prediction;
    let resultClass = '';
    let icon = '';
    let title = '';
    let message = '';
    let schemes = [];
    
    if (prediction === 'Very_Good') {
        resultClass = 'very-good';
        icon = '✅';
        title = 'Excellent Credit Profile!';
        message = 'Congratulations! You qualify for large loans with favorable interest rates.';
        schemes = [
            { name: 'PM-KISAN Credit Card', amount: '₹3,00,000', rate: '7%' },
            { name: 'Mudra Loan (Tarun)', amount: '₹10,00,000', rate: '8-10%' },
            { name: 'Stand-Up India', amount: '₹1,00,00,000', rate: '9%' }
        ];
    } else if (prediction === 'Normal') {
        resultClass = 'normal';
        icon = '⚠️';
        title = 'Good Credit Profile';
        message = 'You qualify for medium-sized loans. Follow our recommendations to improve your profile.';
        schemes = [
            { name: 'Mudra Loan (Kishor)', amount: '₹5,00,000', rate: '10-12%' },
            { name: 'PM SVANidhi', amount: '₹50,000', rate: '12%' },
            { name: 'SHG Bank Linkage', amount: '₹1,00,000', rate: '11%' }
        ];
    } else {
        resultClass = 'very-bad';
        icon = '📈';
        title = 'Needs Improvement';
        message = 'You qualify for micro-loans. We\'ve prepared a personalized improvement plan for you.';
        schemes = [
            { name: 'Mudra Loan (Shishu)', amount: '₹50,000', rate: '14%' },
            { name: 'SHG Micro-credit', amount: '₹25,000', rate: '15%' },
            { name: 'NRLM Support', amount: '₹30,000', rate: '14%' }
        ];
    }
    
    // Update result card
    resultCard.className = `result-card ${resultClass}`;
    document.getElementById('resultIcon').textContent = icon;
    document.getElementById('resultTitle').textContent = title;
    document.getElementById('resultMessage').textContent = message;
    
    // Update stats
    document.getElementById('classification').textContent = prediction.replace('_', ' ');
    document.getElementById('confidence').textContent = `${data.confidence}%`;
    document.getElementById('loanRange').textContent = data.loan_range;
    document.getElementById('processingTime').textContent = `${data.processing_time_ms}ms`;
    
    // Update details
    const detailsDiv = document.getElementById('resultDetails');
    detailsDiv.innerHTML = `
        <h3 style="margin-bottom: 15px; font-size: 18px;">Recommended Government Schemes</h3>
        ${schemes.map(scheme => `
            <div style="margin-bottom: 15px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="font-weight: 600; margin-bottom: 5px;">${scheme.name}</div>
                <div style="font-size: 14px; opacity: 0.9;">
                    Max Amount: ${scheme.amount} | Interest: ${scheme.rate}
                </div>
            </div>
        `).join('')}
        
        <h3 style="margin: 25px 0 15px; font-size: 18px;">Key Factors</h3>
        <div style="font-size: 14px; opacity: 0.9;">
            <div style="margin-bottom: 8px;">• Credit Score: ${data.factors.creditScore}</div>
            <div style="margin-bottom: 8px;">• Payment History: ${data.factors.creditPaymentHistory}</div>
            <div style="margin-bottom: 8px;">• Average Payment: ${data.factors.avgPaymentHistory}</div>
        </div>
    `;
    
    // Show results
    resultsDiv.style.display = 'block';
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Reset form
function resetForm() {
    const assessmentLayout = document.querySelector('.assessment-layout');
    assessmentLayout.classList.add('centered');
    
    document.getElementById('loanForm').reset();
    document.getElementById('results').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load dashboard
async function loadDashboard() {
    const dashboardContent = document.getElementById('dashboardContent');
    dashboardContent.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading dashboard...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
        if (!response.ok) throw new Error('Failed to load dashboard');
        
        const stats = await response.json();
        
        dashboardContent.innerHTML = `
            <div class="dashboard-card">
                <h3>📊 Total Applications</h3>
                <div style="font-size: 48px; font-weight: 700; color: var(--primary); margin: 20px 0;">
                    ${stats.total_applications}
                </div>
                <p style="color: var(--text-light);">Applications processed</p>
            </div>
            
            <div class="dashboard-card">
                <h3>🎯 Average Confidence</h3>
                <div style="font-size: 48px; font-weight: 700; color: var(--success); margin: 20px 0;">
                    ${stats.average_confidence.toFixed(1)}%
                </div>
                <p style="color: var(--text-light);">Prediction confidence</p>
            </div>
            
            <div class="dashboard-card">
                <h3>📈 Predictions Breakdown</h3>
                ${Object.entries(stats.prediction_breakdown || {}).map(([key, value]) => `
                    <div class="dashboard-stat">
                        <span>${key.replace('_', ' ')}</span>
                        <strong>${value}</strong>
                    </div>
                `).join('')}
            </div>
            
            <div class="dashboard-card">
                <h3>✅ Status Breakdown</h3>
                ${Object.entries(stats.status_breakdown || {}).map(([key, value]) => `
                    <div class="dashboard-stat">
                        <span>${key.charAt(0).toUpperCase() + key.slice(1)}</span>
                        <strong>${value}</strong>
                    </div>
                `).join('')}
            </div>
            
            <div class="dashboard-card" style="grid-column: 1 / -1;">
                <h3>🤖 ML Models Performance</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;">
                    <div style="text-align: center; padding: 20px; background: var(--light); border-radius: 12px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--primary);">94.5%</div>
                        <div style="color: var(--text-light); margin-top: 5px;">XGBoost</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: var(--light); border-radius: 12px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--primary);">92.1%</div>
                        <div style="color: var(--text-light); margin-top: 5px;">Random Forest</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: var(--light); border-radius: 12px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--primary);">87.3%</div>
                        <div style="color: var(--text-light); margin-top: 5px;">Logistic Regression</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: var(--light); border-radius: 12px;">
                        <div style="font-size: 32px; font-weight: 700; color: var(--primary);">85.7%</div>
                        <div style="color: var(--text-light); margin-top: 5px;">KNN</div>
                    </div>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        dashboardContent.innerHTML = `
            <div class="dashboard-card" style="grid-column: 1 / -1; text-align: center; padding: 60px;">
                <p style="color: var(--danger); font-size: 18px; margin-bottom: 10px;">❌ Failed to load dashboard</p>
                <p style="color: var(--text-light);">Please make sure the backend server is running.</p>
                <button class="btn btn-primary" onclick="loadDashboard()" style="margin-top: 20px;">Retry</button>
            </div>
        `;
    }
}

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend API is healthy');
        }
    } catch (error) {
        console.warn('⚠️ Backend API is not responding. Please start the server.');
    }
}

// Initialize
checkAPIHealth();

// Center the assessment form initially
document.addEventListener('DOMContentLoaded', () => {
    const assessmentLayout = document.querySelector('.assessment-layout');
    if (assessmentLayout) {
        assessmentLayout.classList.add('centered');
    }
});
