document.addEventListener('DOMContentLoaded', () => {
    const moodSelect = document.querySelector('.mood-select');
    const moodOptions = document.querySelectorAll('.mood-option');
    const dateInput = document.getElementById('entry_date');

    // Highlight the selected mood if already set
    if (moodSelect && moodSelect.value) {
        const selectedOption = document.querySelector(`[data-mood="${moodSelect.value}"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
    }

    // Handle mood selection click
    moodOptions.forEach(option => {
        option.addEventListener('click', () => {
            // Remove 'selected' class from all options
            moodOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add 'selected' class to clicked option
            option.classList.add('selected');
            
            // Update hidden input value
            if (moodSelect) {
                moodSelect.value = option.dataset.mood;
            }
        });
    });

    // Handle date change
    if (dateInput) {
        dateInput.addEventListener('change', () => {
            const newDate = dateInput.value;
            window.location.href = `${window.location.pathname}?date=${newDate}`;
        });
    }

    // Initialize mood heatmap if container exists
    const heatmapContainer = document.getElementById('mood-heatmap');
    const miniHeatmapContainer = document.getElementById('mini-mood-heatmap');
    
    function initializeHeatmap(containerId, options = {}) {
        fetch('/api/calendar_data')
            .then(response => response.json())
            .then(data => {
                const formattedData = {};
                for (const [timestamp, value] of Object.entries(data)) {
                    const date = new Date(timestamp * 1000);
                    const dateKey = date.toISOString().split('T')[0];
                    formattedData[dateKey] = value;
                }

                new MoodHeatmap(containerId, formattedData, {
                    width: options.miniMode ? 8 : 12,
                    height: options.miniMode ? 8 : 12,
                    rows: 7,
                    legend: !options.miniMode,
                    ...options
                });
            })
            .catch(error => console.error('Error loading mood data:', error));
    }

    if (heatmapContainer) {
        initializeHeatmap('mood-heatmap');
    }
    
    if (miniHeatmapContainer) {
        initializeHeatmap('mini-mood-heatmap', { miniMode: true, navigation: false });
    }
});