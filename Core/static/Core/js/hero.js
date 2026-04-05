
document.addEventListener('DOMContentLoaded', () => {
        // --- Mobile Menu Logic ---
        const hamburger = document.getElementById('hamburger');
        const mobileCloseNav = document.getElementById('mobileCloseNav');
        const mobileMenu = document.getElementById('mobileMenu');
        const body = document.body;
        const contentWrapper = document.getElementById('contentWrapper'); // NEW: Get the main content wrapper

        function openMenu(){
            mobileMenu.classList.add('active');
            hamburger.style.display = 'none'; // Hide hamburger
            mobileCloseNav.style.display = 'block'; // Show cross in the same spot
            
            mobileMenu.setAttribute('aria-hidden','false');
            hamburger.setAttribute('aria-expanded','true');
            
            body.style.overflow = 'hidden'; // Disable background scrolling
            contentWrapper.classList.add('content-dimmed'); // Dim background content and block interaction
        }
        
    function closeMenu(){
            mobileMenu.classList.remove('active');
            hamburger.style.display = 'block'; // Show hamburger
            mobileCloseNav.style.display = 'none'; // Hide cross
            
            mobileMenu.setAttribute('aria-hidden','true');
            hamburger.setAttribute('aria-expanded','false');
            
            body.style.overflow = ''; // Re-enable background scrolling
            contentWrapper.classList.remove('content-dimmed'); // Restore background content
        }

        // Event listeners for opening and closing the menu
        hamburger && hamburger.addEventListener('click', openMenu);
        mobileCloseNav && mobileCloseNav.addEventListener('click', closeMenu);
        
        // Close menu when clicking the backdrop overlay
        mobileMenu && mobileMenu.addEventListener('click', (e)=>{ 
            // Check if the click was directly on the full menu backdrop, not the sliding panel
            if(e.target === mobileMenu) closeMenu(); 
        });

        // Close menu on ESC key
        document.addEventListener('keydown', (e)=>{ 
            if(e.key === 'Escape' && mobileMenu.classList.contains('active')) closeMenu(); 
        });


        // Initialize button state and handle window resize for desktop view
        const checkMobileVisibility = () => {
             if (window.innerWidth <= 850) {
                if (!mobileMenu.classList.contains('active')) {
                    // Only display hamburger if the menu is closed on mobile
                    hamburger.style.display = 'block';
                    mobileCloseNav.style.display = 'none';
                }
            } else {
                // Ensure buttons are hidden and menu is closed on desktop
                closeMenu(); 
                hamburger.style.display = 'none';
                mobileCloseNav.style.display = 'none';
            }
        };

        window.addEventListener('resize', checkMobileVisibility);
        // Run once on load
        checkMobileVisibility(); 


        // --- Carousel Logic (Simple Manual Scroll) ---
        const carousels = document.querySelectorAll('.carousel');
        
        carousels.forEach(carousel => {
            const track = carousel.querySelector('.carousel-track');
            const leftBtn = carousel.querySelector('.btn-left');
            const rightBtn = carousel.querySelector('.btn-right');

            const scrollAmount = 320; // Scroll roughly one card width + gap
            
            if (leftBtn && rightBtn && track) {
                leftBtn.addEventListener('click', () => {
                    track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
                });

                rightBtn.addEventListener('click', () => {
                    track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
                });
            }
        });


        // --- FAQ Accordion Logic ---
        const accordionList = document.getElementById('faqAccordion');
        const faqSearchInput = document.getElementById('faqSearchInput');

        const toggleAccordion = (item) => {
            const body = item.querySelector('.accordion-body');
            const isActive = item.classList.contains('active');

            // Find currently active item if any, and close it
            document.querySelectorAll('.accordion-item.active').forEach(i => {
                if (i !== item) {
                    i.classList.remove('active');
                    i.querySelector('.accordion-body').style.maxHeight = 0;
                }
            });

            if (!isActive) {
                item.classList.add('active');
                // Use scrollHeight to dynamically set height for smooth transition
                body.style.maxHeight = body.scrollHeight + "px";
            } else {
                item.classList.remove('active');
                body.style.maxHeight = 0;
            }
        };

        const filterFaqs = () => {
            const filterText = faqSearchInput.value.toLowerCase();
            const items = accordionList.querySelectorAll('.accordion-item');

            items.forEach(item => {
                const questionText = item.querySelector('.accordion-question').textContent.toLowerCase();
                const searchTerms = item.getAttribute('data-search-terms').toLowerCase();
                
                if (questionText.includes(filterText) || searchTerms.includes(filterText)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
                
                // Ensure closed when filtering
                item.classList.remove('active');
                item.querySelector('.accordion-body').style.maxHeight = 0;
            });
        };

        // accordionList.querySelectorAll('.accordion-header').forEach(header => {
        //     header.addEventListener('click', () => toggleAccordion(header.closest('.accordion-item')));
        //     header.addEventListener('keydown', (e) => {
        //         if (e.key === 'Enter' || e.key === ' ') {
        //             e.preventDefault();
        //             toggleAccordion(header.closest('.accordion-item'));
        //         }
        //     });
        // });
        
        // faqSearchInput.addEventListener('input', filterFaqs);
        
        // // Initialize the first item's height if it's active by default 
        // const initialActiveItem = accordionList.querySelector('.accordion-item.active');
        // if (initialActiveItem) {
        //     initialActiveItem.querySelector('.accordion-body').style.maxHeight = 
        //         initialActiveItem.querySelector('.accordion-body').scrollHeight + "px";
        // }
    });




// ------------------- logout ------------------------
// 1. Get Elements
const logoutForm = document.getElementById('logout-form'); // Your existing Django form
const openModalBtn = document.getElementById('openLogoutModal'); // The button that OPENS the modal
const logoutModal = document.getElementById('logoutModal');
const confirmBtn = document.getElementById('confirmLogout'); // The "Yes" button
const cancelBtn = document.getElementById('cancelLogout'); // The "No" button


// --- 2. Opening the Modal ---
openModalBtn.addEventListener('click', () => {
    // Open the native HTML <dialog> element
    logoutModal.showModal();
});

// --- 3. Confirmation Logic: Submitting the Django Form ---
confirmBtn.addEventListener('click', () => {
    // Close the modal
    logoutModal.close();
    
    // Programmatically submit your Django form
    logoutForm.submit();
});

// --- 4. Cancellation Logic ---
cancelBtn.addEventListener('click', () => {
    // Just close the modal and do nothing
    logoutModal.close();
});

// Optional: Close the dialog if the user clicks outside of it
logoutModal.addEventListener('click', (event) => {
    if (event.target === logoutModal) {
        logoutModal.close();
    }
});