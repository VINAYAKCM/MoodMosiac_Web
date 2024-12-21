class MoodHeatmap {
    constructor(containerId, data, options = {}) {
        this._data = data;
        this._options = {
            cellSize: 15,
            padding: 2,
            monthSpacing: 20,
            navigation: true,
            miniMode: false,  // New option for insights page
            ...options
        };
        
        this._container = document.getElementById(containerId);
        if (!this._container) {
            throw new Error(`Container ${containerId} not found`);
        }
        
        this._currentDate = new Date();
        this._startDate = new Date(this._currentDate.getFullYear(), 0, 1);
        
        // Adjusted mood mapping to match backend values
        this._moodMap = {
            0: 'No entry',
            1: 'Sad',
            2: 'Stressed',
            3: 'Neutral',
            4: 'Happy',
            5: 'Excited'
        };
        
        this.render();
        if (!this._options.miniMode) {
            this.setupNavigation();
        }
    }

    formatDate(date) {
        return date.toISOString().split('T')[0];
    }

    getMonthName(date) {
        return date.toLocaleString('default', { month: 'long' });
    }

    createTooltip(date, value) {
        return `
            <div class="tooltip">
                ${this._moodMap[value] || 'No entry'} on ${date.toLocaleDateString()}
            </div>
        `;
    }

    createMonthGrid(year, month) {
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const monthName = this.getMonthName(firstDay);
        
        let html = `
            <div class="month-container">
                ${!this._options.miniMode ? `<div class="month-header">${monthName}</div>` : ''}
                <div class="days-grid">
        `;

        // Add empty cells for days before the first of the month
        for (let i = 0; i < firstDay.getDay(); i++) {
            html += '<div class="day-cell empty"></div>';
        }

        // Add cells for each day of the month
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const date = new Date(year, month, day);
            const dateKey = this.formatDate(date);
            const value = this._data[dateKey] || 0;
            
            html += `
                <div class="day-cell color-${value}" data-date="${dateKey}">
                    ${this.createTooltip(date, value)}
                </div>
            `;
        }

        html += '</div></div>';
        return html;
    }

    render() {
        let html = '<div class="heatmap-container">';
        
        if (this._options.navigation && !this._options.miniMode) {
            // Add year display section
            html += `
                <div class="year-display">
                    <button class="nav-button prev-button">← Previous</button>
                    <div class="current-year">${this._startDate.getFullYear()}</div>
                    <button class="nav-button next-button">Next →</button>
                </div>
            `;
        }
    
        html += '<div class="months-row">';
        
        
        // For mini mode, only show last 3 months
        const monthsToShow = this._options.miniMode ? 3 : 12;
        const startMonth = this._options.miniMode ? 
            this._currentDate.getMonth() - 2 : 0;
        
        for (let i = 0; i < monthsToShow; i++) {
            const month = (startMonth + i) % 12;
            const year = this._startDate.getFullYear() + Math.floor((startMonth + i) / 12);
            html += this.createMonthGrid(year, month);
        }
        
        html += '</div>';
        
        if (!this._options.miniMode) {
            html += `
                <div class="heatmap-legend">
                    <span>Sad</span>
                    ${[0, 1, 2, 3, 4, 5].map(value => `
                        <div class="legend-color color-${value}"></div>
                    `).join('')}
                    <span>Excited</span>
                </div>
            `;
        }
        
        html += '</div>';
        this._container.innerHTML = html;
    }

    setupNavigation() {
        const prevButton = this._container.querySelector('.prev-button');
        const nextButton = this._container.querySelector('.next-button');
        const yearDisplay = this._container.querySelector('.current-year');
    
        if (prevButton && nextButton) {
            prevButton.addEventListener('click', () => {
                this._startDate.setFullYear(this._startDate.getFullYear() - 1);
                this.render();
                this.setupNavigation(); // Re-setup event listeners after render
            });
    
            nextButton.addEventListener('click', () => {
                this._startDate.setFullYear(this._startDate.getFullYear() + 1);
                this.render();
                this.setupNavigation(); // Re-setup event listeners after render
            });
        }
    }
}