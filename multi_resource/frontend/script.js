// Risk Distribution Donut Chart with Interactive Hover
const riskCtx = document.getElementById('riskChart').getContext('2d');
const riskChart = new Chart(riskCtx, {
    type: 'doughnut',
    data: {
        labels: ['Low Risk', 'Medium Risk', 'High Risk'],
        datasets: [{
            data: [67, 23, 10],
            backgroundColor: ['#107C10', '#FF8C00', '#D13438'],
            borderWidth: 0,
            hoverOffset: 15,
            hoverBorderWidth: 3,
            hoverBorderColor: '#FFFFFF'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    padding: 15,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    size: 14
                },
                bodyFont: {
                    size: 13
                },
                padding: 12,
                callbacks: {
                    label: function(context) {
                        return context.label + ': ' + context.parsed + '%';
                    }
                }
            }
        },
        animation: {
            animateScale: true,
            animateRotate: true
        }
    }
});

// Cost Trends Line Chart with Interactive Hover
const costCtx = document.getElementById('costChart').getContext('2d');
const costChart = new Chart(costCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [
            {
                label: 'Current Cost',
                data: [1000, 950, 900, 850, 800, 750],
                borderColor: '#D13438',
                backgroundColor: 'rgba(209, 52, 56, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: '#D13438',
                pointHoverRadius: 8,
                pointHoverBackgroundColor: '#D13438',
                pointHoverBorderColor: '#FFFFFF',
                pointHoverBorderWidth: 3
            },
            {
                label: 'Optimized Cost (Savings)',
                data: [1000, 800, 650, 500, 400, 300],
                borderColor: '#107C10',
                backgroundColor: 'rgba(16, 124, 16, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: '#107C10',
                pointHoverRadius: 8,
                pointHoverBackgroundColor: '#107C10',
                pointHoverBorderColor: '#FFFFFF',
                pointHoverBorderWidth: 3
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    padding: 15,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    size: 14
                },
                bodyFont: {
                    size: 13
                },
                padding: 12,
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': $' + context.parsed.y;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return '$' + value;
                    }
                }
            }
        }
    }
});

// Tab Switching Function
function showTab(tabName) {
    // Hide all table contents
    const allTables = document.querySelectorAll('.table-content');
    allTables.forEach(table => {
        table.classList.remove('active');
    });

    // Remove active class from all tabs
    const allTabs = document.querySelectorAll('.tab-btn');
    allTabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected table
    const selectedTable = document.getElementById(tabName + '-table');
    if (selectedTable) {
        selectedTable.classList.add('active');
    }

    // Mark clicked tab as active
    event.target.classList.add('active');
}

/// Theme Toggle Function
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.contains('dark-theme');
    
    if (isDark) {
        // Switch to light theme
        body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        // Switch to dark theme
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme on page load
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
});


// Load saved theme on page load and set active icon
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const lightIcon = document.getElementById('lightThemeIcon');
    const darkIcon = document.getElementById('darkThemeIcon');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        darkIcon.classList.add('active');
    } else {
        lightIcon.classList.add('active');
    }
});

// Toggle dropdown on click
function toggleDropdown(event) {
    event.stopPropagation();
    
    const dropdown = event.currentTarget.closest('.dropdown');
    const menu = dropdown.querySelector('.dropdown-menu');
    
    // Close all other dropdowns first
    document.querySelectorAll('.dropdown-menu').forEach(m => {
        if (m !== menu) {
            m.classList.remove('show');
        }
    });
    
    // Toggle current dropdown
    menu.classList.toggle('show');
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

// Notification Toggle
function toggleNotifications() {
    const panel = document.getElementById('notificationPanel');
    panel.classList.toggle('show');
}

// Close notifications when clicking outside
document.addEventListener('click', function(event) {
    const notificationWrapper = document.querySelector('.notification-wrapper');
    const panel = document.getElementById('notificationPanel');
    
    if (notificationWrapper && !notificationWrapper.contains(event.target)) {
        panel.classList.remove('show');
    }
});

// Account Functions
function refreshDashboard() {
    // Show loading message
    const notification = document.createElement('div');
    notification.style.cssText = 'position:fixed; top:80px; right:20px; background:#0078D4; color:white; padding:15px 25px; border-radius:8px; box-shadow:0 5px 15px rgba(0,0,0,0.3); z-index:10000; font-size:14px;';
    notification.textContent = 'Refreshing dashboard data...';
    document.body.appendChild(notification);
    
    // Simulate refresh (replace with your actual data refresh logic)
    setTimeout(() => {
        // Update last scan time
        document.getElementById('lastScanTime').textContent = 'Just now';
        
        // Remove notification
        notification.textContent = 'Dashboard refreshed successfully!';
        notification.style.background = '#107C10';
        
        setTimeout(() => {
            notification.remove();
        }, 2000);
    }, 1500);
}

function goToProfile() {
    alert('Navigating to profile page...');
    // Replace with actual profile page navigation
    // window.location.href = '/profile';
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear any stored data
        localStorage.clear();
        sessionStorage.clear();
        
        // Redirect to login page or close window
        alert('Logging out...');
        
        // Option 1: Redirect to login page
        // window.location.href = '/login';
        
        // Option 2: Close the current window/tab
        window.close();
        
        // If window.close() doesn't work (browser restriction), redirect to a logout page
        setTimeout(() => {
            window.location.href = 'about:blank';
        }, 500);
    }
}

// Scan Now Function
function scanNow() {
    const scanBtn = event.target;
    const originalText = scanBtn.textContent;
    
    // Disable button and show scanning
    scanBtn.disabled = true;
    scanBtn.textContent = 'Scanning...';
    scanBtn.style.opacity = '0.6';
    
    // Simulate scan (replace with actual scan logic)
    setTimeout(() => {
        document.getElementById('lastScanTime').textContent = 'Just now';
        
        // Re-enable button
        scanBtn.disabled = false;
        scanBtn.textContent = originalText;
        scanBtn.style.opacity = '1';
        
        // Show success notification
        alert('Scan completed successfully!');
    }, 2000);
}
