document.addEventListener('DOMContentLoaded', function() {
    // Create and append loading spinner to body
    const spinnerHTML = `
        <div class="spinner-overlay" id="globalSpinner">
            <div class="spinner-container">
                <div class="spinner"></div>
                <div class="spinner-text">Loading...</div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', spinnerHTML);

    // Loading spinner control functions
    window.showSpinner = (message = 'Loading...') => {
        const spinner = document.getElementById('globalSpinner');
        spinner.querySelector('.spinner-text').textContent = message;
        spinner.classList.add('show');
    };

    window.hideSpinner = () => {
        const spinner = document.getElementById('globalSpinner');
        spinner.classList.remove('show');
    };

    // Handle page transitions
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && !link.hasAttribute('data-no-spinner') && 
            link.href && !link.href.startsWith('#') && 
            link.target !== '_blank' && !e.ctrlKey && !e.shiftKey) {
            showSpinner();
        }
    });

    // Add fade-in animation to sections
    const sections = document.querySelectorAll('section');
    const observerOptions = {
        root: null,
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                if (entry.target.classList.contains('skills')) {
                    animateSkills();
                }
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        section.style.opacity = '0';
        observer.observe(section);
    });

    // Navbar scroll behavior
    let lastScroll = 0;
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        if (currentScroll > lastScroll && currentScroll > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScroll = currentScroll;
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

    // Skills animation
    const animateSkills = () => {
        const skills = document.querySelectorAll('.skill-item .progress-bar');
        skills.forEach(skill => {
            const percentage = skill.getAttribute('aria-valuenow');
            skill.style.width = percentage + '%';
        });
    };

    // Form handling and validation
    const forms = document.querySelectorAll('form:not([data-no-spinner])');
    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!form.checkValidity()) {
                e.stopPropagation();
                form.classList.add('was-validated');
                return;
            }

            const submitBtn = form.querySelector('[type="submit"]');
            const formData = new FormData(form);
            
            try {
                form.classList.add('form-loading');
                if (submitBtn) {
                    submitBtn.classList.add('loading');
                    submitBtn.disabled = true;
                }

                if (form.classList.contains('contact-form')) {
                    const response = await fetch(form.action, {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        showAlert('Message sent successfully!', 'success');
                        form.reset();
                    } else {
                        throw new Error('Failed to send message');
                    }
                }
            } catch (error) {
                showAlert('Failed to send message. Please try again.', 'danger');
            } finally {
                form.classList.remove('form-loading');
                if (submitBtn) {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }
            }
        });
    });

    // Project filter
    const filterButtons = document.querySelectorAll('[data-filter]');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');
            
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            projectCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Alert function
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.contact-form');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle page load complete
    window.addEventListener('load', () => {
        hideSpinner();
    });

    // Handle browser back/forward buttons
    window.addEventListener('popstate', () => {
        showSpinner();
    });

    showSpinner('Custom loading message');
    // ... do something ...
    hideSpinner();

    document.addEventListener('submit', (e) => {
        const form = e.target;
        if (!form.hasAttribute('data-no-spinner')) {
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
            showSpinner('Submitting...');
        }
    });
}); 