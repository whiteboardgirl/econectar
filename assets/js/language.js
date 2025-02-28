// Language Handler for Econectar

class LanguageManager {
    constructor() {
        // Available languages
        this.languages = {
            pt: 'Português',
            en: 'English',
            es: 'Español'
        };

        // Default language
        this.defaultLang = 'pt';
        
        // Current language
        this.currentLang = this.getInitialLanguage();
        
        // Initialize
        this.init();
    }

    init() {
        // Set up language switcher
        this.setupLanguageSwitcher();
        
        // Initial language load
        this.loadLanguage(this.currentLang);
        
        // Update meta tags
        this.updateMetaTags();
        
        // Setup URL handling
        this.handleURLParameters();
    }

    getInitialLanguage() {
        // Check priority:
        // 1. Saved preference
        // 2. URL parameter
        // 3. Browser language
        // 4. Default language

        const savedLang = localStorage.getItem('econectar-language');
        const urlLang = new URLSearchParams(window.location.search).get('lang');
        const browserLang = navigator.language.split('-')[0];

        return savedLang || 
               urlLang || 
               (this.isValidLanguage(browserLang) ? browserLang : this.defaultLang);
    }

    isValidLanguage(lang) {
        return Object.keys(this.languages).includes(lang);
    }

    setupLanguageSwitcher() {
        // Create language switcher if it doesn't exist
        if (!document.querySelector('.language-switcher')) {
            this.createLanguageSwitcher();
        }

        // Add event listeners to language buttons
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const newLang = btn.getAttribute('data-lang');
                this.switchLanguage(newLang);
            });
        });
    }

    createLanguageSwitcher() {
        const switcher = document.createElement('div');
        switcher.className = 'language-switcher';

        Object.keys(this.languages).forEach(lang => {
            const btn = document.createElement('button');
            btn.className = `lang-btn ${lang === this.currentLang ? 'active' : ''}`;
            btn.setAttribute('data-lang', lang);
            btn.innerHTML = `
                <span class="lang-code">${lang.toUpperCase()}</span>
                <span class="lang-name">${this.languages[lang]}</span>
            `;
            switcher.appendChild(btn);
        });

        // Insert switcher into the navigation
        const nav = document.querySelector('.nav-links');
        if (nav) {
            nav.appendChild(switcher);
        }
    }

    async switchLanguage(newLang) {
        if (!this.isValidLanguage(newLang) || newLang === this.currentLang) {
            return;
        }

        try {
            // Show loading state
            this.toggleLoading(true);

            // Load new language
            await this.loadLanguage(newLang);

            // Update UI
            this.updateLanguageUI(newLang);

            // Save preference
            localStorage.setItem('econectar-language', newLang);

            // Update URL if needed
            this.updateURL(newLang);

            // Update meta tags
            this.updateMetaTags();

        } catch (error) {
            console.error('Error switching language:', error);
            this.showNotification('error', 'Error changing language. Please try again.');
        } finally {
            this.toggleLoading(false);
        }
    }

    async loadLanguage(lang) {
        try {
            // Hide all language texts
            document.querySelectorAll('[class*="text-"]').forEach(el => {
                el.classList.add('hidden');
            });

            // Show selected language texts
            document.querySelectorAll(`.text-${lang}`).forEach(el => {
                el.classList.remove('hidden');
            });

            // Update current language
            this.currentLang = lang;

            // Dispatch event for other components
            window.dispatchEvent(new CustomEvent('languageChanged', { 
                detail: { language: lang } 
            }));

        } catch (error) {
            throw new Error(`Failed to load language: ${lang}`);
        }
    }

    updateLanguageUI(newLang) {
        // Update language buttons
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === newLang);
        });

        // Update HTML lang attribute
        document.documentElement.setAttribute('lang', newLang);

        // Update direction for RTL languages if needed
        const isRTL = ['ar', 'he'].includes(newLang);
        document.documentElement.setAttribute('dir', isRTL ? 'rtl' : 'ltr');
    }

    updateURL(lang) {
        if (window.history.pushState) {
            const newURL = new URL(window.location.href);
            newURL.searchParams.set('lang', lang);
            window.history.pushState({ path: newURL.href }, '', newURL.href);
        }
    }

    updateMetaTags() {
        // Update meta tags based on current language
        const metaTags = {
            title: document.querySelector('title'),
            description: document.querySelector('meta[name="description"]'),
            ogTitle: document.querySelector('meta[property="og:title"]'),
            ogDescription: document.querySelector('meta[property="og:description"]'),
            twitterTitle: document.querySelector('meta[name="twitter:title"]'),
            twitterDescription: document.querySelector('meta[name="twitter:description"]')
        };

        // Update each meta tag if it exists
        Object.entries(metaTags).forEach(([key, element]) => {
            if (element) {
                const content = element.querySelector(`.text-${this.currentLang}`);
                if (content) {
                    if (key === 'title') {
                        element.textContent = content.textContent;
                    } else {
                        element.setAttribute('content', content.textContent);
                    }
                }
            }
        });
    }

    handleURLParameters() {
        // Handle language parameter in URL
        window.addEventListener('popstate', () => {
            const urlLang = new URLSearchParams(window.location.search).get('lang');
            if (urlLang && this.isValidLanguage(urlLang) && urlLang !== this.currentLang) {
                this.switchLanguage(urlLang);
            }
        });
    }

    toggleLoading(show) {
        document.body.classList.toggle('loading', show);
    }

    showNotification(type, message) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Utility method to get translated text
    getTranslation(key) {
        const element = document.querySelector(`[data-translate="${key}"] .text-${this.currentLang}`);
        return element ? element.textContent : key;
    }
}

// Initialize language manager
document.addEventListener('DOMContentLoaded', () => {
    window.languageManager = new LanguageManager();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageManager;
}
