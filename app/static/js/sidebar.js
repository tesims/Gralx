$(document).ready(function() {
    // Smooth scrolling for sidebar links
    $('.sidebar a').on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top - 70
            }, 800);
        }
    });

    // Highlight active section in sidebar
    $(window).scroll(function() {
        var scrollDistance = $(window).scrollTop();
        $('section').each(function(i) {
            if ($(this).position().top <= scrollDistance + 100) {
                $('.sidebar .nav-link.active').removeClass('active');
                $('.sidebar .nav-link').eq(i).addClass('active');
            }
        });
    }).scroll();
});