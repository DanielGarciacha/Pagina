document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const contentItems = document.querySelectorAll('.content-item');

    menuItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            
            const contentId = this.getAttribute('data-content');

            contentItems.forEach(content => {
                if (content.id === contentId) {
                    content.classList.add('active');
                } else {
                    content.classList.remove('active');
                }
            });
        });
    });

    // Show the first section by default
    document.getElementById('section1').classList.add('active');
});
