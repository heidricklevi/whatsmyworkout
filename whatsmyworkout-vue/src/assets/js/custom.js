/**
 * Created by LeviJamesH on 2/3/2017.
 */

// enable tooltips page wide

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});


$(function () {
   $('.side-nav').hover(function () {
       $('.side-nav-list > li > a').css('display', 'inline');
   },
   function () {
       $('.side-nav-list > li > a').css('display', 'none');
   });


});

$(function () {

  // function for mobile side nav and hamburger menu
    $('div.header-toggle i').click(function (e) {
        $('.sidenav').css({"width": "200px", "display": "block"});
        $('#main').css("margin-left", "200px");
        $('.header').css("left", "200px");
        $('.header-toggle .fa.fa-bars').css("display", "none");
    });

    $('.close-button .fa.fa-times').click(function (e) {
        e.preventDefault();
        $('.sidenav').css({"width": "0", "display": "none"});
        $('#main').css("margin-left", "0");
        $('.header').css("left", "0");
        $('.header-toggle .fa.fa-bars').css("display", "block");

    });

});

// main side nav on non mobile

$(function () {
    $('.side-nav-list-main').hover(function () {
        $('.side-nav-list-main').css("width", "200px");
        $('.dashboard-workout-text').append("<span>Dashboard</span>");
        $('.create-workout-text').append("<span>Create Workout</span>");
        $('.calendar-workout-text').append("<span>Schedule</span>");
        $('.share-workout-text').append("<span>Share</span>");
        $('.archive-workout-text').append("<span>Archives</span>");

    }, function () {
        $('.side-nav-list-main').css("width", "60px");
        $('.dashboard-workout-text').contents().last().replaceWith(" ");
        $('.create-workout-text').contents().last().replaceWith(" ");
        $('.archive-workout-text').contents().last().replaceWith(" ");
        $('.calendar-workout-text').contents().last().replaceWith(" ");
        $('.share-workout-text').contents().last().replaceWith(" ");
    });

});




// var csrftoken = $.cookie('csrftoken');
//
// function csrfSafeMethod(method) {
//
//
//
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//
// }
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!csrfSafeMethod(settings.type)) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//             console.log($.cookie());
//         }
//     }
// });
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         console.log(document.cookie);
//         if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
//             function getCookie(name) {
//                 var cookieValue = null;
//                 if (document.cookie && document.cookie != '') {
//                     var cookies = document.cookie.split(';');
//                     for (var i = 0; i < cookies.length; i++) {
//                         var cookie = jQuery.trim(cookies[i]);
//                         // Does this cookie string begin with the name we want?
//                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                             break;
//                         }
//                     }
//                 }
//                 return cookieValue;
//             }
//
//                 // Only send the token to relative URLs i.e. locally.
//             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//
//         }
//     }
// });

 $(document).ready(function()
 {

//     $.ajax({
//     url: 'http://127.0.0.1:8000/get-token/',
//     type: 'GET',
//     dataType: 'json',
//     success: function(data) {
//        $.cookie('csrftoken', data.token); // set the csrftoken cookie
//     }
// });



    // end side nav functions

    $('#workout-form').submit(function (e) {
        e.preventDefault();
        var form = new FormData($('#workout-form').get(0));
        var baseURL = "http://127.0.0.1:8000/";

        $.ajax({
            type: 'POST',
            url: baseURL + "v1/workouts/",
            data: form,
            cache: false,
            processData: false,
            contentType: false,
            success: function () {
                $('#workout-form').before('<div class="alert alert-success alert-dismissable fade show"' +
                    ' role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true"></span></button> Successfully created workout </div>');

                $('.alert').fadeTo(2000, 500).slideUp(500, function () { //auto disappear after 2 seconds
                   $('.alert').slideUp(500);
                });

                $('#workout-form').hide();

            }
        });
        return false;


    });

    $('#workout-form').submit(function (e) {
        var valOfTitle = $('#id_title').val();
        $('.row > .col-sm-8 > h3').text('Add Exercises for workout ' + valOfTitle);
        $('#exercise-form').show('slow');

    });

    // Consume REST api for asynchronous logging into application for user

    $('#login-form').submit(function (e) {
        e.preventDefault();
        var username = $('#id_username').val();
        var password = $('#id_password').val();

        data = {
            username: username,
            password: password
        };

        $.ajax({
            type: 'POST',
            url: '/v1/user/login/',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function () {
                window.location.href = '/';
            }
        });

        return false;

    });

    $('#create-account-form').submit(function (e) {
        e.preventDefault();
        var firstName = $('#id_first_name').val();
        var lastName = $('#id_last_name').val();
        var username = $('#id_username').val();
        var email = $('#id_email').val();
        var password = $('#id_password').val();

        var confirmPassword = $('#id_password2').val();

        data = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            username: username,
            password: password
        };

        if (password !== confirmPassword) {
            var img = $('#pass-img');
            var pass = $('#id_password');
            var confirm = $('#id_password2');

            pass.css({'border-color': 'red', 'border-width': '1px'});
            confirm.css({'border-color': 'red', 'border-width': '1px'});

            img.before('<div class="alert alert-danger" role="alert">Problem submitting. Please make sure your passwords match prior to submitting again.');

            return false;
        }

        $.ajax({
            type: 'POST',
            url: '/v1/users/',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function () {
                window.location.href = '/';
            }
        });

        return false;

    });


    //make REST call to get JSON exercises data based on form selection and store it locally for retrieval

    $('#id_exercises').change(function (e) {
        var exercises = {};
        id = $('#id_exercises').val();

        $.get('/v1/exercises/'+id + '/', function (data, status) {

            if (status) {

                console.log('Retrieved data for exercises '+id);
                exercises = data;
                sessionStorage.id = exercises.id;
                sessionStorage.exercise_link = exercises.exercise_link;
                sessionStorage.exercise_rating = exercises.exercise_rating;
                sessionStorage.start_exercise_image = exercises.start_exercise_image;
                sessionStorage.during_exercise_image = exercises.during_exercise_image;
                sessionStorage.target_muscle = exercises.target_muscle;
                sessionStorage.exercise_name = exercises.exercise_name;
            }

        }).fail(function () {
            sessionStorage.clear();
        });
    });



    $('#exercise-form').submit(function (e) {
        e.preventDefault();
        var workout_name = $('#id_title').val();
        var exerciseName = $('#id_exercise_name').val();
        var sets = $('#id_sets').val();
        var reps = $('#id_reps').val();
        var notes = $('#id_notes').val();
        var user = $('#id_user').val();


        var exercises = {

            id: sessionStorage.id,
            exercise_link: sessionStorage.exercise_link,
            exercise_rating: sessionStorage.exercise_rating,
            start_exercise_image: sessionStorage.start_exercise_image,
            during_exercise_image: sessionStorage.during_exercise_image,
            target_muscle: sessionStorage.target_muscle,
            exercise_name: sessionStorage.exercise_name
        };

        //exercises not loaded and stored in sessionStorage
        if (!exercises.id) {
            exercises.exercise_name = exerciseName;
            exercises.target_muscle = $('#id_target_muscle').val();
        }

        data = {
            exercises: exercises,
            exercise_name: exerciseName,
            sets: sets,
            reps: reps,
            notes: notes,
            workout_name: workout_name,
            user: user
        };

        console.log('Workout name ' + workout_name);

        console.log(data);
        $.ajax({
            type: 'POST',
            url: '/v1/exercise/',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'json',
            success: function () {
                $('#exercise-form').before('<div class="alert alert-success alert-dismissable fade show"' +
                    ' role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true"></span></button> Successfully added exercise</div>');
            }
        });

        return false;

    });


     //preview image when creating a workout

     $('#id_workout_image').change(function (e) {

         var img = document.getElementById('previewimg');
         img.src = URL.createObjectURL(e.target.files[0]);
     });

 });