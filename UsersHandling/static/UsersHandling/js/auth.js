document.addEventListener('DOMContentLoaded', () => {
    const formSlider = document.getElementById('formSlider');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const loginBtn = document.getElementById('login-btn');
    const signupBtn = document.getElementById('signup-btn');
    const formViewport = document.querySelector('.form-slider-viewport');
    
    // Elements for file upload label update
    const fileInput = document.getElementById('profile-image');
    const fileLabel = document.querySelector('label[for="profile-image"]');

    let currentMode = 'login';
    let loginHeight = 0;
    let signupHeight = 0;

    function calculateFormHeights() {
        // Measure heights
        loginHeight = loginForm.offsetHeight; 
        signupHeight = signupForm.offsetHeight;
        
        // Update viewport to match current mode
        formViewport.style.height = (currentMode === 'login' ? loginHeight : signupHeight) + 'px';
    }
    
    // Update file label when a file is chosen
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                fileLabel.textContent = "Selected: " + e.target.files[0].name;
                fileLabel.style.color = "white";
            } else {
                fileLabel.textContent = "Upload Profile Picture";
                fileLabel.style.color = "rgba(255, 255, 255, 0.6)";
            }
            // Recalculate because changing text might slightly shift height
            calculateFormHeights();
        });
    }

    function switchMode(newMode) {
        if (newMode === currentMode) return;
        
        let transformValue;
        let targetHeight;

        if (newMode === 'signup') {
            transformValue = `-${loginHeight}px`; 
            targetHeight = signupHeight; 
        } else {
            transformValue = '0';
            targetHeight = loginHeight;
        }
        
        formViewport.style.height = `${targetHeight}px`;
        formSlider.style.transform = `translateY(${transformValue})`;

        if (document.activeElement) {
            document.activeElement.blur();
        }

        loginBtn.classList.toggle('active', newMode === 'login');
        signupBtn.classList.toggle('active', newMode === 'signup');
        
        currentMode = newMode;
    }
    
    loginBtn.addEventListener('click', () => switchMode('login'));
    signupBtn.addEventListener('click', () => switchMode('signup'));

    // Wait a tiny bit for browser rendering before first calculation
    setTimeout(calculateFormHeights, 50);

    window.addEventListener('resize', calculateFormHeights);
});