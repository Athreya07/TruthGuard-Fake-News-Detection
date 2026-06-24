document.addEventListener("DOMContentLoaded", () => {
    // 1. Smooth scroll to detector section from Hero CTA
    const ctaBtn = document.getElementById("cta-btn");
    const detectorSection = document.getElementById("detector-section");

    if (ctaBtn && detectorSection) {
        ctaBtn.addEventListener("click", (e) => {
            e.preventDefault();
            detectorSection.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    }

    // 2. Character and Word Counter
    const newsInput = document.getElementById("news-input");
    const charCountEl = document.getElementById("char-count");
    const wordCountEl = document.getElementById("word-count");

    if (newsInput) {
        const updateCounters = () => {
            const text = newsInput.value;
            const chars = text.length;
            
            // Count words (splitting by whitespace, filtering out empty strings)
            const words = text.trim() === "" ? 0 : text.trim().split(/\s+/).length;
            
            if (charCountEl) charCountEl.textContent = chars;
            if (wordCountEl) wordCountEl.textContent = words;
        };

        // Run initially in case Flask re-rendered the text
        updateCounters();
        
        // Listen for user typing
        newsInput.addEventListener("input", updateCounters);
    }

    // 3. Form Loading Animations & Submission Handling
    const analysisForm = document.getElementById("analysis-form");
    const loadingScreen = document.getElementById("loading-screen");
    const submitBtn = document.getElementById("submit-btn");
    const loadingMessage = document.getElementById("loading-message");

    if (analysisForm && loadingScreen && submitBtn) {
        const loadingPhases = [
            "Initializing pipeline...",
            "Cleaning text and removing noise...",
            "Extracting TF-IDF features (N-grams)...",
            "Running Logistic Regression classifier...",
            "Calculating class probabilities...",
            "Generating analytical report..."
        ];

        analysisForm.addEventListener("submit", (e) => {
            // Only show loader if form validation passes (HTML5 required field)
            if (newsInput && newsInput.value.trim().length >= 20) {
                // Show loading screen and disable form elements
                loadingScreen.classList.remove("hidden");
                submitBtn.disabled = true;
                newsInput.readOnly = true;

                // Cycle through AI classification steps to show recruiter premium work
                let phaseIndex = 0;
                if (loadingMessage) {
                    loadingMessage.textContent = loadingPhases[0];
                }

                const interval = setInterval(() => {
                    phaseIndex++;
                    if (phaseIndex < loadingPhases.length) {
                        if (loadingMessage) {
                            loadingMessage.textContent = loadingPhases[phaseIndex];
                        }
                    } else {
                        clearInterval(interval);
                    }
                }, 400); // cycle quickly to keep it responsive but noticeable
            }
        });
    }

    // 4. Auto-Scroll to Results / Error Section on Page Load
    const resultsSection = document.getElementById("results-section");
    const errorSection = document.getElementById("error-section");

    if (resultsSection) {
        // Delay slightly for smooth styling animations to kick in
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 150);
    } else if (errorSection) {
        setTimeout(() => {
            errorSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 150);
    }
});
