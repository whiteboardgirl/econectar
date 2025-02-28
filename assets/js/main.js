// Language handling
const languageHandler = {
    // Store current language
    currentLang: document.documentElement.lang || 'en',

    // Save language preference
    saveLanguagePreference: function(lang) {
        localStorage.setItem('preferred-language', lang);
    },

    // Get saved language preference
    getLanguagePreference: function() {
        return localStorage.getItem('preferred-language');
    },

    // Detect browser language
    detectBrowserLanguage: function() {
        const lang = navigator.language || navigator.userLanguage;
        return lang.substring(0, 2); // Get first 2 characters (e.g., 'en' from 'en-US')
    }
};

// Navigation handling
const navigationHandler = {
    init: function() {
        // Add active class to current navigation item
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('nav a');
        
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });

        // Add smooth scrolling to anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
};

// Mobile menu handling
const mobileMenuHandler = {
    init: function() {
        const menuButton = document.querySelector('.mobile-menu-button');
        const mobileMenu = document.querySelector('.mobile-menu');

        if (menuButton && mobileMenu) {
            menuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('active');
                menuButton.classList.toggle('active');
            });
        }
    }
};

// Form validation
const formHandler = {
    init: function() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!this.checkValidity()) {
                    e.preventDefault();
                    this.reportValidity();
                }
            });
        });
    }
};

// Image lazy loading
const lazyLoadHandler = {
    init: function() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }
};

// Animation on scroll
const animationHandler = {
    init: function() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        });

        animatedElements.forEach(element => animationObserver.observe(element));
    }
};

// Theme switcher (light/dark mode)
const themeHandler = {
    init: function() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);

        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                
                document.documentElement.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
            });
        }
    }
};

// Initialize all handlers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    navigationHandler.init();
    mobileMenuHandler.init();
    formHandler.init();
    lazyLoadHandler.init();
    animationHandler.init();
    themeHandler.init();

    // Console welcome message
    console.log('Welcome to Econectar! 🐝');
});

// Handle loading state
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Handle scroll events
window.addEventListener('scroll', function() {
    // Add class to header when scrolling
    const header = document.querySelector('header');
    if (header) {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
});
