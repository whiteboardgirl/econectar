// Gallery and Lightbox Handler for Econectar

class GalleryManager {
    constructor() {
        this.currentSlide = 0;
        this.isAnimating = false;
        this.touchStartX = 0;
        this.touchEndX = 0;

        // Configuration
        this.config = {
            animationDuration: 300,
            slideShowDelay: 5000,
            touchThreshold: 50,
            preloadImages: true,
            enableKeyboard: true,
            enableTouch: true,
            gallerySelector: '.gallery',
            lightboxSelector: '.lightbox',
            thumbnailSelector: '.gallery-thumbnail'
        };

        this.init();
    }

    init() {
        this.createLightbox();
        this.initGalleries();
        this.bindEvents();
    }

    createLightbox() {
        // Create lightbox HTML structure
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox hidden';
        lightbox.innerHTML = `
            <div class="lightbox-overlay"></div>
            <div class="lightbox-content">
                <div class="lightbox-header">
                    <span class="lightbox-counter"></span>
                    <button class="lightbox-close" aria-label="Close">×</button>
                </div>
                <div class="lightbox-container">
                    <button class="lightbox-prev" aria-label="Previous">‹</button>
                    <div class="lightbox-image-container">
                        <img class="lightbox-image" src="" alt="">
                        <div class="lightbox-loader"></div>
                    </div>
                    <button class="lightbox-next" aria-label="Next">›</button>
                </div>
                <div class="lightbox-caption"></div>
                <div class="lightbox-thumbnails"></div>
            </div>
        `;

        document.body.appendChild(lightbox);
        this.lightbox = lightbox;
        this.lightboxImage = lightbox.querySelector('.lightbox-image');
        this.lightboxCaption = lightbox.querySelector('.lightbox-caption');
        this.lightboxCounter = lightbox.querySelector('.lightbox-counter');
        this.lightboxThumbnails = lightbox.querySelector('.lightbox-thumbnails');
    }

    initGalleries() {
        // Initialize all galleries on the page
        document.querySelectorAll(this.config.gallerySelector).forEach(gallery => {
            this.setupGallery(gallery);
        });
    }

    setupGallery(gallery) {
        // Setup gallery grid and thumbnails
        const images = gallery.querySelectorAll('img');
        
        images.forEach((img, index) => {
            // Create thumbnail container
            const thumbnail = document.createElement('div');
            thumbnail.className = this.config.thumbnailSelector.substring(1);
            
            // Create thumbnail image
            const thumbImg = document.createElement('img');
            thumbImg.src = img.dataset.thumbnail || img.src;
            thumbImg.alt = img.alt;
            thumbnail.appendChild(thumbImg);

            // Add click event
            thumbnail.addEventListener('click', () => {
                this.openLightbox(gallery, index);
            });

            // Replace original image with thumbnail
            img.parentNode.replaceChild(thumbnail, img);

            // Preload full-size image if enabled
            if (this.config.preloadImages) {
                const preloadImg = new Image();
                preloadImg.src = img.dataset.full || img.src;
            }
        });
    }

    bindEvents() {
        // Bind all event listeners
        this.lightbox.querySelector('.lightbox-close').addEventListener('click', () => this.closeLightbox());
        this.lightbox.querySelector('.lightbox-prev').addEventListener('click', () => this.prevSlide());
        this.lightbox.querySelector('.lightbox-next').addEventListener('click', () => this.nextSlide());
        this.lightbox.querySelector('.lightbox-overlay').addEventListener('click', () => this.closeLightbox());

        // Keyboard navigation
        if (this.config.enableKeyboard) {
            document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        }

        // Touch navigation
        if (this.config.enableTouch) {
            this.lightbox.addEventListener('touchstart', (e) => this.handleTouchStart(e));
            this.lightbox.addEventListener('touchmove', (e) => this.handleTouchMove(e));
            this.lightbox.addEventListener('touchend', () => this.handleTouchEnd());
        }

        // Handle image loading
        this.lightboxImage.addEventListener('load', () => this.handleImageLoad());
        this.lightboxImage.addEventListener('error', () => this.handleImageError());
    }

    openLightbox(gallery, index) {
        this.currentGallery = gallery;
        this.images = Array.from(gallery.querySelectorAll(this.config.thumbnailSelector));
        this.currentSlide = index;

        // Show lightbox
        this.lightbox.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        // Load initial image
        this.loadImage(index);
        this.updateThumbnails();
        this.updateCounter();
    }

    closeLightbox() {
        this.lightbox.classList.add('hidden');
        document.body.style.overflow = '';
        this.stopSlideshow();
    }

    loadImage(index) {
        const image = this.images[index];
        const fullSrc = image.querySelector('img').dataset.full || image.querySelector('img').src;
        const caption = image.querySelector('img').alt;

        // Show loader
        this.lightbox.querySelector('.lightbox-loader').style.display = 'block';
        this.lightboxImage.style.opacity = '0';

        // Load new image
        this.lightboxImage.src = fullSrc;
        this.lightboxCaption.textContent = caption;
    }

    handleImageLoad() {
        // Hide loader and show image
        this.lightbox.querySelector('.lightbox-loader').style.display = 'none';
        this.lightboxImage.style.opacity = '1';
    }

    handleImageError() {
        // Handle image loading error
        this.lightbox.querySelector('.lightbox-loader').style.display = 'none';
        this.lightboxImage.src = '/assets/images/error-image.jpg';
        this.lightboxCaption.textContent = 'Error loading image';
    }

    updateThumbnails() {
        this.lightboxThumbnails.innerHTML = '';
        
        this.images.forEach((image, index) => {
            const thumb = document.createElement('div');
            thumb.className = 'lightbox-thumbnail';
            if (index === this.currentSlide) thumb.classList.add('active');
            
            const thumbImg = document.createElement('img');
            thumbImg.src = image.querySelector('img').src;
            thumbImg.alt = image.querySelector('img').alt;
            
            thumb.appendChild(thumbImg);
            thumb.addEventListener('click', () => this.goToSlide(index));
            this.lightboxThumbnails.appendChild(thumb);
        });
    }

    updateCounter() {
        this.lightboxCounter.textContent = `${this.currentSlide + 1} / ${this.images.length}`;
    }

    prevSlide() {
        if (this.isAnimating) return;
        this.goToSlide(this.currentSlide - 1);
    }

    nextSlide() {
        if (this.isAnimating) return;
        this.goToSlide(this.currentSlide + 1);
    }

    goToSlide(index) {
        if (this.isAnimating) return;

        this.isAnimating = true;
        
        // Handle circular navigation
        if (index < 0) index = this.images.length - 1;
        if (index >= this.images.length) index = 0;

        this.currentSlide = index;
        this.loadImage(index);
        this.updateThumbnails();
        this.updateCounter();

        setTimeout(() => {
            this.isAnimating = false;
        }, this.config.animationDuration);
    }

    handleKeyboard(e) {
        switch (e.key) {
            case 'ArrowLeft':
                this.prevSlide();
                break;
            case 'ArrowRight':
                this.nextSlide();
                break;
            case 'Escape':
                this.closeLightbox();
                break;
        }
    }

    handleTouchStart(e) {
        this.touchStartX = e.touches[0].clientX;
    }

    handleTouchMove(e) {
        this.touchEndX = e.touches[0].clientX;
    }

    handleTouchEnd() {
        const diff = this.touchStartX - this.touchEndX;

        if (Math.abs(diff) > this.config.touchThreshold) {
            if (diff > 0) {
                this.nextSlide();
            } else {
                this.prevSlide();
            }
        }
    }

    startSlideshow() {
        this.slideshowInterval = setInterval(() => {
            this.nextSlide();
        }, this.config.slideShowDelay);
    }

    stopSlideshow() {
        if (this.slideshowInterval) {
            clearInterval(this.slideshowInterval);
            this.slideshowInterval = null;
        }
    }

    // Public API
    static init() {
        return new GalleryManager();
    }
}

// Initialize gallery when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.galleryManager = GalleryManager.init();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GalleryManager;
}
