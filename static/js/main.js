// Main JavaScript for CodeVerseHub

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Countdown timer for contests
    const countdownElements = document.querySelectorAll('.countdown-timer');
    countdownElements.forEach(function(element) {
        const endTime = new Date(element.dataset.endTime).getTime();
        updateCountdown(element, endTime);
        
        setInterval(function() {
            updateCountdown(element, endTime);
        }, 1000);
    });

    // Code editor enhancements
    const codeEditors = document.querySelectorAll('.code-editor');
    codeEditors.forEach(function(editor) {
        // Add line numbers (simplified)
        editor.addEventListener('input', function() {
            const lines = this.value.split('\n').length;
            // Could add more sophisticated line numbering here
        });
        
        // Tab support
        editor.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;
                
                this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
                this.selectionStart = this.selectionEnd = start + 1;
            }
        });
    });

    // Problem filtering
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('select, input');
        filterInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // Contest registration confirmation
    const contestRegisterBtns = document.querySelectorAll('.contest-register-btn');
    contestRegisterBtns.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to register for this contest?')) {
                e.preventDefault();
            }
        });
    });

    // Submission form validation
    const submissionForm = document.getElementById('submission-form');
    if (submissionForm) {
        submissionForm.addEventListener('submit', function(e) {
            const codeField = document.getElementById('id_code');
            if (codeField && codeField.value.trim() === '') {
                e.preventDefault();
                alert('Please enter your code before submitting.');
                codeField.focus();
            }
        });
    }

    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performSearch(searchInput.value);
            }, 300);
        });
    }

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                navigator.clipboard.writeText(targetElement.textContent).then(function() {
                    const originalText = btn.textContent;
                    btn.textContent = 'Copied!';
                    btn.classList.add('btn-success');
                    
                    setTimeout(function() {
                        btn.textContent = originalText;
                        btn.classList.remove('btn-success');
                    }, 2000);
                });
            }
        });
    });
});

// Countdown timer function
function updateCountdown(element, endTime) {
    const now = new Date().getTime();
    const distance = endTime - now;

    if (distance < 0) {
        element.innerHTML = "Contest has ended";
        return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    element.innerHTML = `
        <div class="countdown-item">
            <span class="countdown-number">${days}</span>
            <span class="countdown-label">Days</span>
        </div>
        <div class="countdown-item">
            <span class="countdown-number">${hours}</span>
            <span class="countdown-label">Hours</span>
        </div>
        <div class="countdown-item">
            <span class="countdown-number">${minutes}</span>
            <span class="countdown-label">Minutes</span>
        </div>
        <div class="countdown-item">
            <span class="countdown-number">${seconds}</span>
            <span class="countdown-label">Seconds</span>
        </div>
    `;
}

// Search function
function performSearch(query) {
    if (query.length < 2) return;
    
    // This would typically make an AJAX request to the server
    // For now, we'll just filter visible elements
    const searchableElements = document.querySelectorAll('.searchable');
    searchableElements.forEach(function(element) {
        const text = element.textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    });
}

// Chart.js configuration for dashboard
function createDashboardChart(elementId, data, options = {}) {
    const ctx = document.getElementById(elementId);
    if (!ctx) return;

    const defaultOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: options.title || 'Chart'
            }
        }
    };

    const config = {
        type: options.type || 'line',
        data: data,
        options: { ...defaultOptions, ...options }
    };

    return new Chart(ctx, config);
}

// Utility functions
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

function formatMemory(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

// AJAX utility
function makeAjaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Ajax request failed:', error);
        throw error;
    });
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Footer Functions

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show/hide back to top button based on scroll position
window.addEventListener('scroll', function() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.visibility = 'visible';
        } else {
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.visibility = 'hidden';
        }
    }
});

// Newsletter subscription
function subscribeNewsletter() {
    const emailInput = document.querySelector('.newsletter-form input[type="email"]');
    const email = emailInput.value.trim();
    
    if (!email) {
        showNotification('Please enter your email address', 'warning');
        return;
    }
    
    if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    // Simulate newsletter subscription
    showNotification('Thank you for subscribing! You\'ll receive updates soon.', 'success');
    emailInput.value = '';
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Initialize newsletter subscription on button click
document.addEventListener('DOMContentLoaded', function() {
    const subscribeBtn = document.querySelector('.newsletter-form .btn');
    if (subscribeBtn) {
        subscribeBtn.addEventListener('click', subscribeNewsletter);
    }
    
    // Handle enter key in newsletter input
    const newsletterInput = document.querySelector('.newsletter-form input[type="email"]');
    if (newsletterInput) {
        newsletterInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                subscribeNewsletter();
            }
        });
    }
    
    // Initialize back to top button visibility
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        backToTopBtn.style.opacity = '0';
        backToTopBtn.style.visibility = 'hidden';
        backToTopBtn.style.transition = 'all 0.3s ease';
    }
});

// Footer animations on scroll
function initFooterAnimations() {
    const footer = document.querySelector('.footer');
    if (!footer) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Animate footer elements when they come into view
                const animateElements = footer.querySelectorAll('.footer-links li, .stat-item, .social-link');
                animateElements.forEach((el, index) => {
                    setTimeout(() => {
                        el.style.opacity = '1';
                        el.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            }
        });
    }, {
        threshold: 0.1
    });
    
    observer.observe(footer);
    
    // Set initial state for animation
    const animateElements = footer.querySelectorAll('.footer-links li, .stat-item, .social-link');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease';
    });
}

// Initialize footer animations when DOM is loaded
document.addEventListener('DOMContentLoaded', initFooterAnimations);