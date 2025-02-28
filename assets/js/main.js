// Main JavaScript for Econectar

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all components
    const app = new Econectar();
});

class Econectar {
    constructor() {
        // Initialize properties
        this.isLoading = false;
        this.currentLang = 'pt';
        
        // Initialize components
        this.initNavigation();
        this.initScrollEffects();
        this.initLanguageSwitcher();
        this.initForms();
        this.initAnimations();
        this.initBackToTop();
        this.initLazyLoading();
    }

    // Navigation
    initNavigation() {
        const mobileMenuBtn = document.querySelector('.mobile-menu');
        const nav = document.querySelector('.nav-links');

        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => {
                nav.classList.toggle('active');
                mobileMenuBtn.setAttribute('aria-expanded', 
                    nav.classList.contains('active'));
            });

            // Close menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.nav') && nav.classList.contains('active')) {
                    nav.classList.remove('active');
                    mobileMenuBtn.setAttribute('aria-expanded', 'false');
                }
            });

            // Handle smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => {
                    e.preventDefault();
                    const target = document.querySelector(anchor.getAttribute('href'));
                    if (target) {
                        nav.classList.remove('active');
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });
        }
    }

    // Scroll Effects
    initScrollEffects() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    if (entry.target.classList.contains('counter')) {
                        this.animateCounter(entry.target);
                    }
                }
            });
        }, observerOptions);

        // Observe elements with animation classes
        document.querySelectorAll('.animate-on-scroll, .counter').forEach(el => {
            observer.observe(el);
        });

        // Header scroll effect
        let lastScroll = 0;
        const header = document.querySelector('.header');

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > lastScroll && currentScroll > 100) {
                header.classList.add('header-hidden');
            } else {
                header.classList.remove('header-hidden');
            }
            
            if (currentScroll > 50) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
            
            lastScroll = currentScroll;
        });
    }

    // Counter Animation
    animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const step = target / (duration / 16); // 60fps
        let current = 0;

        const updateCounter = () => {
            current += step;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        };

        updateCounter();
    }

    // Language Switcher
    initLanguageSwitcher() {
        const langButtons = document.querySelectorAll('.lang-btn');
        
        langButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const lang = btn.getAttribute('data-lang');
                this.switchLanguage(lang);
            });
        });
    }

    switchLanguage(lang) {
        document.querySelectorAll(`[class*="text-"]`).forEach(el => {
            el.classList.add('hidden');
        });
        
        document.querySelectorAll(`.text-${lang}`).forEach(el => {
            el.classList.remove('hidden');
        });

        this.currentLang = lang;
        localStorage.setItem('preferred-lang', lang);
    }

    // Form Handling
    initForms() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                if (this.isLoading) return;
                
                try {
                    this.setLoading(true);
                    const formData = new FormData(form);
                    const response = await this.submitForm(form.action, formData);
                    
                    if (response.success) {
                        this.showNotification('success', 'Mensagem enviada com sucesso!');
                        form.reset();
                    } else {
                        throw new Error(response.message);
                    }
                } catch (error) {
                    this.showNotification('error', 'Erro ao enviar mensagem. Tente novamente.');
                    console.error('Form submission error:', error);
                } finally {
                    this.setLoading(false);
                }
            });
        });
    }

    async submitForm(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            body: data
        });
        return await response.json();
    }

    // Loading State
    setLoading(isLoading) {
        this.isLoading = isLoading;
        document.body.classList.toggle('loading', isLoading);
    }

    // Notifications
    showNotification(type, message) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('notification-hidden');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Back to Top Button
    initBackToTop() {
        const backToTop = document.getElementById('backToTop');
        
        if (backToTop) {
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    backToTop.classList.add('visible');
                } else {
                    backToTop.classList.remove('visible');
                }
            });

            backToTop.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }

    // Lazy Loading
    initLazyLoading() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Initialize Animations
    initAnimations() {
        // Stagger animations for grid items
        document.querySelectorAll('.stagger-children').forEach(parent => {
            const children = parent.children;
            Array.from(children).forEach((child, index) => {
                child.style.animationDelay = `${index * 0.1}s`;
            });
        });
    }
}

// Utility Functions
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

const throttle = (func, limit) => {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};
