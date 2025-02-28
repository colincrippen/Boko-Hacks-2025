function initializeApp() {
    console.log('News app initialization started');
    setupEventListeners();
    fetchNews('business');
    setupSettingsDialog();
}

function cleanupApp() {
    console.log('News app cleanup');
    const newsContainer = document.getElementById('news-root');
    if (newsContainer) {
        const newsList = newsContainer.querySelector('.news-list');
        if (newsList) {
            newsList.innerHTML = '<div class="loading">Loading news feed...</div>';
        }
    }
}

function setupEventListeners() {
    const newsContainer = document.getElementById('news-root');
    
    newsContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('filter-btn')) {
            const category = e.target.getAttribute('data-category');
            if (category) {
                document.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                e.target.classList.add('active');
                fetchNews(category);
            }
        }
    });

    const searchBtn = document.getElementById('search-button');
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const searchTerm = document.getElementById('search-news').value.trim();
            if (searchTerm) {
                alert("Search functionality is not implemented in this version.");
            } else {
                alert("Please enter a search term.");
            }
        });
    }
}

function setupSettingsDialog() {
    const settingsDialogHTML = `
        <div id="settings-dialog" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                                    background: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.3);
                                    z-index: 1000; display: none; width: 300px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0;">News Settings</h3>
                <button id="close-settings" style="background: none; border: none; font-size: 1.5rem; cursor: pointer;">×</button>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px;">Articles Per Page</label>
                <select id="articles-count" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    <option value="5">5 articles</option>
                    <option value="10" selected>10 articles</option>
                    <option value="15">15 articles</option>
                </select>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px;">Default Category</label>
                <select id="default-category" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    <option value="business" selected>Business</option>
                    <option value="technology">Technology</option>
                    <option value="world">World</option>
                </select>
            </div>
            <div style="text-align: right; margin-top: 20px;">
                <button id="save-settings" style="background-color: #501214; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer;">Save Settings</button>
            </div>
            <!-- Hidden developer section - only shows in dev tools -->
            <div style="display: none;" id="dev-options">
                <hr style="margin: 15px 0;">
                <h4>Developer Options</h4>
                <div style="margin-bottom: 10px;">
                    <label style="display: block; margin-bottom: 5px;">API Filters (JSON)</label>
                    <textarea id="filter-json" style="width: 100%; height: 60px; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" placeholder='{"count": 10}'></textarea>
                </div>
                <button id="apply-filters" style="background-color: #333; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Apply</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', settingsDialogHTML);

    const settingsButton = document.getElementById('settings-button');
    if (settingsButton) {
        settingsButton.addEventListener('click', function() {
            document.getElementById('settings-dialog').style.display = 'block';
        });
    }

    const closeSettingsButton = document.getElementById('close-settings');
    if (closeSettingsButton) {
        closeSettingsButton.addEventListener('click', function() {
            document.getElementById('settings-dialog').style.display = 'none';
        });
    }

    const saveSettingsButton = document.getElementById('save-settings');
    if (saveSettingsButton) {
        saveSettingsButton.addEventListener('click', function() {
            const currentSettings = {
                articlesCount: parseInt(document.getElementById('articles-count').value),
                defaultCategory: document.getElementById('default-category').value,
                filters: {}
            };

            const devOptions = document.getElementById('dev-options');
            if (window.getComputedStyle(devOptions).display !== 'none') {
                try {
                    const filterJSON = document.getElementById('filter-json').value;
                    if (filterJSON.trim()) {
                        currentSettings.filters = JSON.parse(filterJSON);
                    }
                } catch (e) {
                    console.error('Invalid JSON filters:', e);
                    alert('Invalid JSON format for filters');
                    return;
                }
            }

            document.getElementById('settings-dialog').style.display = 'none';

            const activeCategory = document.querySelector('.filter-btn.active').getAttribute('data-category');
            fetchNews(activeCategory, currentSettings.filters); // Pass filters along with category
        });
    }

    const applyFiltersButton = document.getElementById('apply-filters');
    if (applyFiltersButton) {
        applyFiltersButton.addEventListener('click', function() {
            try {
                const filterJSON = document.getElementById('filter-json').value;
                if (filterJSON.trim()) {
                    const currentSettings = { filters: JSON.parse(filterJSON) };
                    const activeCategory = document.querySelector('.filter-btn.active').getAttribute('data-category');
                    fetchNews(activeCategory, currentSettings.filters); // Pass filters along with category
                }
            } catch (e) {
                console.error('Invalid JSON filters:', e);
                alert('Invalid JSON format for filters');
            }
        });
    }
}

function fetchNews(category, filters = {}) {
    const newsContainer = document.getElementById('news-root');
    const newsList = newsContainer.querySelector('.news-list');
    
    // Show loading state
    newsList.innerHTML = '<div class="loading">Loading news feed...</div>';
    
    // Build the base API URL
    let apiUrl = `/apps/news/fetch?category=${category}`;
    
    // Append filters to the URL as query parameters
    if (filters && Object.keys(filters).length > 0) {
        const filterParam = JSON.stringify(filters);
        apiUrl += `&filter=${encodeURIComponent(filterParam)}`;
    }

    console.log(`Fetching news from: ${apiUrl}`);
    
    // Fetch news from the server
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            renderNews(data);
            updateDebugInfo(data);
        })
        .catch(error => {
            console.error('Error fetching news:', error);
            newsList.innerHTML = `
                <div class="error-message">
                    Failed to load news. Please try again later.
                    <br><small>${error.message}</small>
                </div>
            `;
            updateDebugInfo({ error: error.message });
        });
}

function renderNews(data) {
    const newsContainer = document.getElementById('news-root');
    const newsList = newsContainer.querySelector('.news-list');
    
    if (!data || !data.success || !data.data || data.data.length === 0) {
        newsList.innerHTML = '<div class="error-message">No news articles found.</div>';
        return;
    }
    
    const newsItems = data.data; 
    
    let html = '';
    
    // Add each news item
    newsItems.forEach(item => {
        const date = new Date(item.date || new Date()).toLocaleDateString();
        const hasImage = item.imageUrl && item.imageUrl !== 'null';
        
        html += `
            <div class="news-item">
                <div class="news-title">${item.title}</div>
                ${hasImage ? `<div class="news-image"><img src="${item.imageUrl}" alt="${item.title}"></div>` : ''}
                <div class="news-content">${item.content}</div>
                <div class="news-meta">
                    <span>${date}</span>
                    <a href="${item.readMoreUrl}" target="_blank" class="read-more">Read more</a>
                </div>
            </div>
        `;
    });
    
    newsList.innerHTML = html;
    
    // Update timestamp
    const updateTime = document.getElementById('update-time');
    if (updateTime) {
        updateTime.textContent = new Date().toLocaleTimeString();
    }
}

function updateDebugInfo(data) {
    const debugOutput = document.getElementById('debug-output');
    if (debugOutput) {
        debugOutput.style.display = 'block';
        
        // Format the data for display
        let debugText = '';
        if (data.error) {
            debugText = `Error: ${data.error}`;
        } else {
            // Show a truncated version of the response
            const simplifiedData = {...data};
            if (simplifiedData.data && simplifiedData.data.length > 2) {
                simplifiedData.data = [
                    simplifiedData.data[0],
                    simplifiedData.data[1],
                    "... (truncated for display)"
                ];
            }
            debugText = 'API Response:\n' + JSON.stringify(simplifiedData, null, 2);
        }
        
        debugOutput.textContent = debugText;
    }
}

function fetchSourceDetails() {
    const sourceId = document.getElementById('source-id').value.trim();
    const sourceDetails = document.getElementById('source-details');
    
    sourceDetails.innerHTML = '<div class="loading">Loading source details...</div>';
    sourceDetails.style.display = 'block';
    
    fetch(`/apps/news/admin/fetch_source?id=${sourceId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                sourceDetails.innerHTML = `<pre>${JSON.stringify(data.source, null, 2)}</pre>`;
            } else {
                sourceDetails.innerHTML = `<div class="error-message">${data.error || 'Source not found'}</div>`;
            }
        })
        .catch(error => {
            sourceDetails.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
        });
}

function importNewsData() {
    const importData = document.getElementById('import-data').value.trim();
    if (!importData) {
        alert('Please enter base64 encoded data');
        return;
    }
    
    const formData = new FormData();
    formData.append('data', importData);
    
    fetch('/apps/news/import', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Import successful! ${data.count} items imported.`);
        } else {
            alert(`Import failed: ${data.error}`);
        }
    })
    .catch(error => {
        alert(`Error: ${error.message}`);
    });
}

function generateExamplePicklePayload() {
    const payload = "KGRwMApTJ2V4YW1wbGUnCnAxClMndGVzdCBwYXlsb2FkJwpwMgpzLg==";
    
    navigator.clipboard.writeText(payload)
        .then(() => {
            alert("Example payload copied to clipboard! Use it in the Import field.");
        })
        .catch(err => {
            console.error('Could not copy text: ', err);
            alert("Example payload: " + payload);
        });
}

// Make functions available globally
window.initializeApp = initializeApp;
window.cleanupApp = cleanupApp;
window.fetchNews = fetchNews;
window.generateExamplePicklePayload = generateExamplePicklePayload;

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('news-root')) {
        initializeApp();
    }
});

console.log('News.js loaded');