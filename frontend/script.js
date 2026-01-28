/**
 * Main Application Script
 * Handles search, WebSocket communication, and UI updates
 */

// Configuration
const API_BASE = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws/process';

// Global state
let hologram = null;
let ws = null;
let currentQuery = '';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Initialize hologram visualizer
    hologram = new HologramVisualizer('hologramCanvas');

    // Setup event listeners
    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('submit', handleSearch);

    // Connect WebSocket
    connectWebSocket();
}

// ========================================
// Search Handling
// ========================================

async function handleSearch(event) {
    event.preventDefault();

    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();

    if (!query) return;

    currentQuery = query;

    // Show hologram section
    showHologram();
    hideResults();
    resetEngineNodes();

    // Start hologram animation
    hologram.start('searching');

    // Send search via WebSocket for real-time updates
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ query }));
    } else {
        // Fallback to REST API
        performRESTSearch(query);
    }
}

async function performRESTSearch(query) {
    try {
        updateStatus('Initializing AI search...');

        const response = await fetch(`${API_BASE}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query, max_results: 15 })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Search error:', error);
        updateStatus(`Error: ${error.message}`);
    }
}

// ========================================
// WebSocket Communication
// ========================================

function connectWebSocket() {
    try {
        ws = new WebSocket(WS_URL);

        ws.onopen = () => {
            console.log('WebSocket connected');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket closed, reconnecting...');
            setTimeout(connectWebSocket, 3000);
        };

    } catch (error) {
        console.error('WebSocket connection failed:', error);
    }
}

function handleWebSocketMessage(data) {
    console.log('WebSocket message:', data);

    switch (data.type) {
        case 'status':
            updateStatus(data.message);
            hologram.state = data.stage;
            break;

        case 'breakdown':
            displaySubQueries(data.sub_queries);
            updateStatus(`Generated ${data.sub_queries.length} focused searches`);
            break;

        case 'engine_complete':
            markEngineComplete(data.engine, data.count);
            break;

        case 'complete':
            handleSearchComplete(data);
            break;

        case 'error':
            updateStatus(`Error: ${data.message}`);
            hologram.stop();
            break;
    }
}

// ========================================
// UI Updates
// ========================================

function showHologram() {
    const section = document.getElementById('hologramSection');
    section.classList.remove('hidden');
    hologram.resize();
}

function hideHologram() {
    const section = document.getElementById('hologramSection');
    section.classList.add('hidden');
}

function showResults() {
    const section = document.getElementById('resultsSection');
    section.classList.remove('hidden');
    section.classList.add('fade-in');
}

function hideResults() {
    const section = document.getElementById('resultsSection');
    section.classList.add('hidden');
}

function updateStatus(message) {
    const statusText = document.getElementById('statusText');
    statusText.textContent = message;
}

function displaySubQueries(queries) {
    const container = document.getElementById('subQueries');
    container.innerHTML = '';

    queries.forEach((query, index) => {
        setTimeout(() => {
            const chip = document.createElement('div');
            chip.className = 'sub-query-chip';
            chip.textContent = query;
            container.appendChild(chip);
        }, index * 100);
    });
}

function resetEngineNodes() {
    const nodes = document.querySelectorAll('.engine-node');
    nodes.forEach(node => {
        node.classList.remove('searching', 'complete');
        const status = node.querySelector('.node-status');
        status.textContent = '⟳';
    });
}

function markEngineSearching(engineName) {
    const node = document.querySelector(`.engine-node[data-engine="${engineName}"]`);
    if (node) {
        node.classList.add('searching');
    }
}

function markEngineComplete(engineName, count) {
    const node = document.querySelector(`.engine-node[data-engine="${engineName}"]`);
    if (node) {
        node.classList.remove('searching');
        node.classList.add('complete');
        const status = node.querySelector('.node-status');
        status.textContent = '✓';

        // Update label with count
        const label = node.querySelector('.node-label');
        label.textContent = `${engineName} (${count})`;
    }
}

function handleSearchComplete(data) {
    updateStatus('Processing complete!');

    // Trigger synthesis effect
    hologram.triggerSynthesisEffect();

    // Display results after brief delay
    setTimeout(() => {
        displayResults(data);
        hologram.stop();
    }, 1000);
}

function displayResults(data) {
    showResults();

    // Display summary
    const summaryText = document.getElementById('summaryText');
    summaryText.textContent = data.summary || 'Search completed successfully.';

    // Display stats
    const statsContainer = document.getElementById('summaryStats');
    statsContainer.innerHTML = '';

    if (data.engine_stats) {
        Object.entries(data.engine_stats).forEach(([engine, count]) => {
            const statItem = document.createElement('div');
            statItem.className = 'stat-item';
            statItem.innerHTML = `
                <span class="stat-icon">🔍</span>
                <span>${engine}: ${count} results</span>
            `;
            statsContainer.appendChild(statItem);
        });
    }

    // Display results grid
    const resultsGrid = document.getElementById('resultsGrid');
    resultsGrid.innerHTML = '';

    if (data.results && data.results.length > 0) {
        data.results.forEach((result, index) => {
            setTimeout(() => {
                const card = createResultCard(result);
                resultsGrid.appendChild(card);
            }, index * 50);
        });
    } else {
        resultsGrid.innerHTML = '<p style="text-align: center; color: rgba(255,255,255,0.5);">No results found.</p>';
    }
}

function createResultCard(result) {
    const card = document.createElement('div');
    card.className = 'result-card';

    // Determine source badge color
    const sourceColors = {
        'SearXNG': '--engine-searxng',
        'DuckDuckGo': '--engine-duckduckgo',
        'Qwant': '--engine-qwant',
        'Wikipedia': '--engine-wikipedia',
        'Wikidata': '--engine-wikidata'
    };

    const sourceColor = sourceColors[result.source] || '--accent-cyan';

    card.innerHTML = `
        <div class="result-source" style="background: var(${sourceColor}, rgba(0, 217, 255, 0.2));">
            ${result.source}
        </div>
        <h3 class="result-title">${escapeHtml(result.title)}</h3>
        <p class="result-snippet">${escapeHtml(result.snippet)}</p>
        <a href="${escapeHtml(result.url)}" class="result-url" target="_blank" rel="noopener noreferrer">
            ${truncateUrl(result.url)}
        </a>
        ${result.final_score ? `<span class="result-score">Score: ${(result.final_score * 100).toFixed(0)}%</span>` : ''}
    `;

    // Make card clickable
    card.addEventListener('click', (e) => {
        if (e.target.tagName !== 'A') {
            window.open(result.url, '_blank', 'noopener,noreferrer');
        }
    });

    return card;
}

// ========================================
// Utility Functions
// ========================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncateUrl(url) {
    try {
        const urlObj = new URL(url);
        let display = urlObj.hostname + urlObj.pathname;
        if (display.length > 50) {
            display = display.substring(0, 47) + '...';
        }
        return display;
    } catch {
        return url.substring(0, 50) + '...';
    }
}

// ========================================
// Keyboard Shortcuts
// ========================================

document.addEventListener('keydown', (event) => {
    // Focus search input with Ctrl/Cmd + K
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        document.getElementById('searchInput').focus();
    }

    // Clear search with Escape
    if (event.key === 'Escape') {
        document.getElementById('searchInput').value = '';
        hideHologram();
        hideResults();
        hologram.stop();
    }
});
