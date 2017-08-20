$(document).ready(function() {

    $('.nav-tabs a:first').tab('show');

    $(".navbar-nav li a[href^='#']").on('click', function(e) {

        // prevent default anchor click behavior
        e.preventDefault();

        // store hash
        var hash = this.hash;

        // animate
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 300, function(){

            // when done, add hash to url
            // (default click behaviour)
            window.location.hash = hash;
        });

    });

    $('.navbar-show').on('click', function(e) {

        e.preventDefault();

        $('#header-mobile').fadeIn('300');
    });

    $('.navbar-hide').on('click', function(e) {

        e.preventDefault();

        $('#header-mobile').fadeOut('300');

    });

    $(".signup #content").vegas({
        slides: [
            { src: "img/slideshow.jpg" },
            { src: "img/slideshow-2.jpg" },
            { src: "img/slideshow-3.jpg" }
        ]
    });
});
