document.addEventListener('DOMContentLoaded', () => {
    const breathingCircle = document.querySelector('.breathing-circle');
    const breathingText = document.querySelector('.breathing-text');
    const breathingSteps = document.querySelectorAll('.breathing-step');
    
    let isBreathing = false;
    let currentStep = 0;
    let timer;
    
    const breathingPhases = [
        { text: 'Inhale...', duration: 4000, icon: 'fa-lungs' },
        { text: 'Hold...', duration: 4000, icon: 'fa-pause' },
        { text: 'Exhale...', duration: 4000, icon: 'fa-wind' }
    ];
    
    function startBreathing() {
        if (isBreathing) return;
        isBreathing = true;
        currentStep = 0;
        updateBreathingStep();
    }
    
    function stopBreathing() {
        isBreathing = false;
        clearTimeout(timer);
        breathingText.textContent = 'Click to Start';
        breathingCircle.style.transform = 'scale(1)';
        resetSteps();
    }
    
    function updateBreathingStep() {
        if (!isBreathing) return;
        
        const phase = breathingPhases[currentStep];
        breathingText.textContent = phase.text;
        
        // Update active step
        resetSteps();
        breathingSteps[currentStep].style.background = 'rgba(108, 92, 231, 0.3)';
        breathingSteps[currentStep].style.transform = 'translateY(-5px)';
        
        // Animate circle
        if (currentStep === 0) {
            // Inhale
            breathingCircle.style.transform = 'scale(1.2)';
            breathingCircle.style.transition = 'transform 4s ease-in-out';
        } else if (currentStep === 1) {
            // Hold
            breathingCircle.style.transform = 'scale(1.2)';
        } else {
            // Exhale
            breathingCircle.style.transform = 'scale(1)';
            breathingCircle.style.transition = 'transform 4s ease-in-out';
        }
        
        // Move to next step
        timer = setTimeout(() => {
            currentStep = (currentStep + 1) % breathingPhases.length;
            updateBreathingStep();
        }, phase.duration);
    }
    
    function resetSteps() {
        breathingSteps.forEach(step => {
            step.style.background = 'rgba(255, 255, 255, 0.1)';
            step.style.transform = 'translateY(0)';
        });
    }
    
    // Add click event to start/stop breathing
    breathingCircle.addEventListener('click', () => {
        if (isBreathing) {
            stopBreathing();
        } else {
            startBreathing();
        }
    });
    
    // Add hover effect
    breathingCircle.addEventListener('mouseenter', () => {
        if (!isBreathing) {
            breathingCircle.style.transform = 'scale(1.1)';
        }
    });
    
    breathingCircle.addEventListener('mouseleave', () => {
        if (!isBreathing) {
            breathingCircle.style.transform = 'scale(1)';
        }
    });
    
    // Initialize
    breathingText.textContent = 'Click to Start';

    // Add keyboard shortcuts for emergency contacts
    document.addEventListener('keydown', function(e) {
        switch(e.key) {
            case '1':
                window.location.href = 'tel:911';
                break;
            case '2':
                window.location.href = 'tel:18002738255';
                break;
            case '3':
                window.location.href = 'tel:911';
                break;
        }
    });
}); 
