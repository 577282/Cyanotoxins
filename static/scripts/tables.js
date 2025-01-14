
document.addEventListener('DOMContentLoaded', () => {
    // Navigation tabs logic
    const navTabs = document.querySelectorAll('.navigation-tabs .tab-link');
    const currentPath = window.location.pathname;

    // Set the active navigation tab based on the current path
    navTabs.forEach(navTab => {
        if (navTab.getAttribute('href') === currentPath) {
            navTab.classList.add('active');
        } else {
            navTab.classList.remove('active');
        }

        // Add click event listener to switch active tab on navigation
        navTab.addEventListener('click', () => {
            // Remove active class from all navigation tabs
            navTabs.forEach(tab => tab.classList.remove('active'));

            // Add active class to clicked navigation tab
            navTab.classList.add('active');
        });
    });

    // Sheet tabs logic
    const sheetTabs = document.querySelectorAll('.sheet-tabs .tab-link');
    const tables = document.querySelectorAll('.table-container');

    // Sheet tab switching logic
    sheetTabs.forEach(sheetTab => {
        sheetTab.addEventListener('click', () => {
            // Remove active class from all sheet tabs and tables
            sheetTabs.forEach(tab => tab.classList.remove('active'));
            tables.forEach(table => table.classList.remove('active'));

            // Add active class to clicked sheet tab and corresponding table
            sheetTab.classList.add('active');
            const tabIndex = sheetTab.getAttribute('data-tab');
            document.getElementById('table-' + tabIndex).classList.add('active');
        });
    });

    // Activate the first sheet tab and table by default
    if (sheetTabs.length > 0) {
        sheetTabs[0].classList.add('active');
        tables[0].classList.add('active');
    }
});



// Initialize DataTables for each table
$(document).ready(function() {
    $('table').each(function() {
        $(this).DataTable({
            search: {
                regex: true, // Enable regex matching globally for searches
                smart: false // Disable smart search (optional, but helps with exact matches)
            }
        });
    });
});


// Click event for toxin types in the first sheet
$(document).on('click', '.clickable-toxin', function() {
    const toxinType = $(this).text().trim();  // Get the clicked toxin type text

    // Switch to the second sheet (if it's not already active)
    $('.tab-link').eq(1).click();  // Assuming Sheet 2 is the second tab (index 1)

    // Use DataTable search to filter by the clicked toxin type in Sheet 2
    const tableSheet2 = $('#table-1 table').DataTable();  // Get DataTable instance for Sheet 2
    tableSheet2.search(toxinType).draw();  // Search and filter rows in Sheet 2

    // Optional: Scroll to Sheet 2
    $('html, body').animate({
        scrollTop: $('#table-1').offset().top
    }, 1000);
});



