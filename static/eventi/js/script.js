document.addEventListener('DOMContentLoaded', function () {
    const galleryItems = Array.from(document.querySelectorAll('.js-gallery-item'));
    const lightbox = document.getElementById('eventLightbox');
    const lightboxImage = document.getElementById('lightboxImage');
    const closeBtn = document.getElementById('lightboxClose');
    const prevBtn = document.getElementById('lightboxPrev');
    const nextBtn = document.getElementById('lightboxNext');

    if (!galleryItems.length || !lightbox || !lightboxImage) return;

    const images = galleryItems.map(item => ({
        url: item.dataset.imageUrl,
        alt: item.dataset.imageAlt || ''
    }));

    let currentIndex = 0;

    function updateLightbox(index) {
        currentIndex = index;
        lightboxImage.src = images[currentIndex].url;
        lightboxImage.alt = images[currentIndex].alt;
    }

    function openLightbox(index) {
        updateLightbox(index);
        lightbox.classList.add('is-open');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
    }

    function closeLightbox() {
        lightbox.classList.remove('is-open');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lightbox-open');
        lightboxImage.src = '';
        lightboxImage.alt = '';
    }

    function showNext() {
        const nextIndex = (currentIndex + 1) % images.length;
        updateLightbox(nextIndex);
    }

    function showPrev() {
        const prevIndex = (currentIndex - 1 + images.length) % images.length;
        updateLightbox(prevIndex);
    }

    galleryItems.forEach((item, index) => {
        item.addEventListener('click', function () {
            openLightbox(index);
        });
    });

    closeBtn.addEventListener('click', closeLightbox);
    nextBtn.addEventListener('click', showNext);
    prevBtn.addEventListener('click', showPrev);

    lightbox.addEventListener('click', function (e) {
        if (e.target.classList.contains('event-lightbox-backdrop')) {
            closeLightbox();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (!lightbox.classList.contains('is-open')) return;

        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowRight') showNext();
        if (e.key === 'ArrowLeft') showPrev();
    });
});