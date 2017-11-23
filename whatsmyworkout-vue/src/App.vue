<template >
 <div v-if="isAuthenticated">
     <div v-if="computedAuth">
    <dashboard :computed-auth="computedAuth">
    </dashboard>
     </div>
</div>
    <v-app v-else="isAuthenticated" standalone>
    <header id="header" style="position: relative">
             <v-alert info v-model="alert">
            NOTE: This site and app is still under heavy active development and very early along the development process.
            This means that several features and aesthetics are not yet implemented. Please keep this in mind when using the app and site.
            All feedback and suggestions are much appreciated.
        </v-alert>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <nav class="navbar navbar-toggleable-md navbar-dark bg-faded p-0">
                    <button @click="hide = false" id="show" class="navbar-toggler navbar-show navbar-toggler-right" type="button">
                        <v-icon>menu</v-icon>
                    </button>
                    <a class="navbar-brand" href="#">
                        <div class="text-center logo-heading hidden-sm-and-down">Whats My Workout?
                        </div>
                        <img id="header-logo" src="../src/assets/img/logo.png" alt="" class="img-fluid mr-5">
                    </a>

                    <div class="collapse navbar-collapse align-items-center">
                        <ul class="navbar-nav mr-auto ">
                            <li class="nav-item active mr-3">
                                <a class="nav-link white--text title" href="#header">Home <span class="sr-only">(current)</span></a>
                            </li>
                            <li class="nav-item mr-3">
                                <a class="nav-link white--text title" href="#features">Features</a>
                            </li>
                            <li class="nav-item mr-3">
                                <a class="nav-link white--text title" href="#signup">Contact</a>
                            </li>
                            <li class="nav-item mr-3">
                                <a class="nav-link white--text title" href="#feedback">Feedback</a>
                            </li>
                        </ul>
                        <span class="navbar-text">
                            <a href="#signup" class="font-weight-bold">Sign Up!</a>
                        </span>
                        <span class="navbar-text">
                            <a href="#login" class="font-weight-bold">Sign In</a>
                        </span>
                    </div>
                </nav>
            </div>
        </div>
    </div>
</header>

<div id="header-mobile" v-show="hide">
    <div class="container h-100">
        <div class="row h-100">
            <div class="col-md-12 h-100">
                <div class="d-flex">
                    <div>
                        <div class="top-overflow" style="overflow-x: hidden; overflow-y: hidden">
                            <div class="top">
                                <ul class="navbar-nav ml-1">
                                    <li class="nav-item">
                                        <a @click="hide = true" class="nav-link" href="#header">Home <span class="sr-only">(current)</span></a>
                                    </li>
                                    <li class="nav-item">
                                        <a @click="hide = true" class="nav-link" href="#features">Features</a>
                                    </li>
                                    <li class="nav-item">
                                        <a @click="hide = true" class="nav-link" href="#signup">Contact</a>
                                    </li>
                                    <li class="nav-item">
                                        <a @click="hide = true" class="nav-link" href="#feedback">Feedback</a>
                                    </li>
                                </ul>
                                <div>
                        <span class="navbar-text">
                            <a @click="hide = true" href="#signup" class="font-weight-bold">Free Sign Up Now!</a>
                        </span>
                        <span class="navbar-text">
                            <a @click="hide = true" href="#login" class="font-weight-bold">Sign In</a>
                        </span>
                                </div>
                            </div>
                        </div>

                        <div class="bottom ">
                             <v-divider ></v-divider>
                            <img src="../src/assets/img/logo.png" alt="" class="img-fluid mb-2">
                            <p class="mb-0 mt-3">Copyright Whats My Workout 2017</p>
                            <div style="font-size: x-small;" class="grey--text">Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
                            is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>
                        </div>
                        </div>
                    </div>
                    <div class="ml-auto">
                        <button @click="hide = true" id="hide" class="navbar-toggler navbar-hide navbar-toggler-right" type="button">
                            <v-icon>close</v-icon>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<section class="hero hero-1">
    <div class="white--text text-center title hidden-md-and-up">What's My Workout?</div>
    <div style="text-align: center" class="hidden-md-and-up"><img id="mockup" style="height: 60%; width: 60%;"  src="../src/assets/img/Untitled.png" alt="" class="mockup hidden-md-and-up"></div>
    <div class="container">

        <div class="row">
            <div class="col-lg-6">
                <h5 class="title pt-4 mb-4">Easily Create your workouts!</h5>
                <p class="lead">
                    Dedicated simple creation of your workouts including the ability to assign the date you will complete the workout.
                    Then see that workout front and center in your dashboard.
                </p>
                <a href="#signup" style="padding-left: 5%" class="btn text-md-center blue--text font-weight-bold text-uppercase">Checkout Whats My Workout Now!</a>
            </div>
            <div class="col-lg-6 text-right d-lg-block">
                <img id="mockup" style="top: -90px;" src="../src/assets/img/Untitled.png" alt="" class="mockup hidden-sm-and-down">
            </div>
        </div>
    </div>
</section>

<section id="features" class="features features-1 pt-5 mt-5 pb-5 mb-4">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-3 preamble">
                <h4 class="title mt-0 mb-3">Some of <span style="font-style: italic">Whats My Workout</span> features</h4>
                <p class="lead mb-5">
                    Stop taking your clipboard to the gym. Easily keep track of your workouts and share them with others, trainer and trainee style.
                </p>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="single-feature text-center p-5 rounded">
                    <img src="../src/assets/img/planner.svg" alt="" class="img-fluid mb-4 pb-2 rounded-circle">
                    <h5 class="title mt-0 mb-3 font-weight-bold">Plan Your workouts</h5>
                    <p class="mb-0">Create and plan your workouts in advance for easy viewing at the gym.</p>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="single-feature text-center p-5 rounded">
                    <img src="../src/assets/img/line-chart.svg" alt="" class="img-fluid mb-4 pb-2">
                    <h5 class="title mt-0 mb-3 font-weight-bold">Workout Stats</h5>
                    <p class="mb-0">Track your stats such as body fat and weight. Plus keep track of the weight you are lifting for each exercise.</p>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="single-feature text-center p-5 rounded">
                    <img src="../src/assets/img/dumbbell.svg" alt="" class="img-fluid mb-4 pb-2 rounded-circle">
                    <h5 class="title mt-0 mb-3 font-weight-bold">Strength Training</h5>
                    <p class="mb-0">Keep current on your training plans and sessions with simple exercise and workout creation.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="login" class="tour">
    <div class="part with-bg pt-5 pb-5">
        <div class="container">
            <div class="row d-flex align-items-center">
                <div class="col-md-6 preamble">
                    <h4 class="title pt-3 mb-3 pr-5 text-center">
                        Got an account with us?
                    </h4>
                    <p class="lead pr-5 text-center">Sign in to access your dashboard, workouts, calendar and more.</p>
                </div>
                <div class="col-md-6 text-center">
                        <v-card >
                            <v-card-text>
                                    <v-layout row wrap>
                                        <v-flex xs12 md12>
                                            <v-subheader display-4>Provide your credentials to login</v-subheader>
                                        </v-flex>
                                    </v-layout>
                                    <form v-on:submit.prevent="userLogin" method="post">
                                        <v-layout row>
                                            <v-flex xs12 sm12 md8>
                                                <v-text-field v-model="username"
                                                              label="username"
                                                              prepend-icon="account_circle"
                                                ></v-text-field>
                                            </v-flex>
                                        </v-layout>
                                          <v-layout row>
                                            <v-flex xs12 sm12 md8>
                                                <v-text-field v-model="password" label="password"
                                                                prepend-icon="visibility_off" type="password"></v-text-field>
                                            </v-flex>
                                        </v-layout>
                                        <v-layout row>
                                            <v-flex xs12 md8>
                                                <input class="btn primary" type="submit" value="Login">
                                            </v-flex>
                                        </v-layout>
                                    </form>
                            </v-card-text>
                        </v-card>
                </div>

            </div>
        </div>
    </div>
</section>

<section id="signup" class="features-tabs pt-5 pb-3">
  <div class="container">

      <div class="row">
          <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-4 preamble">
              <h4 class="title mt-0 mb-3">Sign up to start creating & tracking your workouts today!</h4>
          </div>
          <div class="col-md-6 offset-md-3">
              <!-- Tab panes -->
              <div class="tab-content">
         <v-card >
                <v-alert error v-model="signUpErrorAlert" transition="scale-transition">{{ signUpAlertMessage }}</v-alert>
                        <v-card-text>
                                <v-layout row wrap>
                                    <v-flex xs12 md12>
                                        <v-subheader display-4>Fill out the information below to create an account!</v-subheader>
                                    </v-flex>
                                </v-layout>
                                <form v-on:submit.prevent="userSignUp" method="post">
                                    <v-layout row>
                                        <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="fullName"
                                                          label="First & Last name"
                                                          prepend-icon="account_circle"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                        <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="email"
                                                          label="email address"
                                                          prepend-icon="email"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                        <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="username"
                                                          label="username"
                                                          prepend-icon="account_circle"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                    </v-layout>
                                      <v-layout row>
                                        <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="password" label="password"
                                                            prepend-icon="visibility_off" type="password">
                                                            required
                                            </v-text-field>
                                        </v-flex>
                                          <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="confirmPass"
                                                          label="Repeat password"
                                                          prepend-icon="visibility_off"
                                                          type="password"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                    </v-layout>
                                    <v-layout row>
                                        <v-flex xs12 md8>
                                            <input class="btn primary" type="submit" value="Sign Up">
                                        </v-flex>
                                    </v-layout>
                                </form>
                        </v-card-text>
                    </v-card>
              </div>
          </div>
      </div>
  </div>
</section>

<section id="feedback" class="services services-1 pt-5 pb-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-4 preamble">
                <h4 class="title mt-0 mb-3">Let us know what you think.</h4>
                <p class="lead mb-5">Keep in mind this software has yet to hit beta stages and there is much to be done. Nonetheless, we want to know how we can improve the experience for anyone wishing to use it.
                We believe in consumer driven development. Share your thoughts and ideas. Let us know what works and what doesn't. We appreciate all constructive feedback.</p>
            </div>
            <div class="col-md-10 offset-md-1 text-center">
                <form @click.submit.prevent="onFeedbackSubmit" method="post">
                    <v-text-field multi-line dark required label="Write your feedback here"></v-text-field>
                    <v-btn type="submit" success>Send Feedback<v-icon right>send</v-icon></v-btn>
                </form>
            </div>
        </div>
    </div>
</section>

<section id="newsletter" class="newsletter pt-5 pb-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-4 preamble">
                <h4 class="title mt-0 mb-3">Stay Informed</h4>
                <p class="lead mb-5">Subscribe to our newsletter to be alerted of updates throughout the development process including new feature drops!</p>
            </div>
            <div class="col-lg-6 offset-lg-3 col-md-8 offset-md-2 col-sm-12 offset-sm-0">
                <form action="#" class="mb-4">
                    <div class="pb-1">
                        <input type="email" class="form-control" placeholder="Enter your email" required>
                        <button class="font-weight-bold text-uppercase" type="submit">Subscribe</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>

<footer id="footer" class="pt-5 pb-5 mb-0 mb-lg-4">
    <div class="container">
        <div class="row d-flex align-items-end">
            <div class="col-lg-6">
                <img src="../src/assets/img/logo.png" alt="" class="img-fluid mb-2">
                <p class="mb-0 mt-3">Copyright Whats My Workout 2017</p>
            </div>
            <div class="col-lg-6">
                <ul class="list-unstyled flex-wrap p-0 mb-4 justify-content-end d-none d-lg-flex">
                    <li class=""><a href="#feedback" class="font-weight-bold">Feedback</a></li>
                    <li class="ml-5"><a href="#" class="font-weight-bold">About</a></li>
                    <li class="ml-5"><a href="#" class="font-weight-bold">Contact</a></li>
                </ul>
                <div class="d-flex justify-content-center justify-content-lg-end w-100 align-items-center mt-4 mt-lg-0">
                        <div style="font-size: x-small;" class="grey--text">Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
                            is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>
                        </div>
                </div>
            </div>
        </div>
    </div>
</footer>
  </v-app>
</div>
</template>

<script>

import { baseURLLocal } from './auth/auth-utils'
import router from '../src/router/index'
import jwt_decode from 'jwt-decode'
import axios from 'axios'
import dashboard from '../src/components/dashboard.vue'
import userDashboard from '../src/components/user-dashboard.vue'


export default {
  name: 'app',
  data () {
    return {
      drawer: true,
      alert: true,
      signUpErrorAlert: false,
      signUpAlertMessage: ' ',
       hide: true,
      items: [
          { title: 'Home', icon: 'dashboard' },
          { title: 'About', icon: 'question_answer' }
          ],
       cItems: [
           { src: "http://lorempixel.com/400/200/"},
           { src: "http://lorempixel.com/400/200/"},
           { src: "http://lorempixel.com/400/200/"},
           { src: "http://lorempixel.com/400/200/"}
       ],
      mini: false,
      right: null,
      username: '',
      password: '',
      fullName: '',
      email: '',
      confirmPass: '',
      userAuth: this.$store.state.userAuth,
      hero: true,
      snackbar: true,
      mode: ' ',
      y: 'top',
      snackbarText: 'gafsgfsagsgfsdgffdg',
      context: ' '
    }
  },
    watch: {
    },
    computed: {
      computedAuth: function () {
          if (!this.userAuth.user) return null;
          return this.userAuth.user;
      },
      isAuthenticated: function () {
          return this.$store.state.userAuth.isAuthenticated;
      },
    },
    methods: {
       userLogin: function () {
          let credentials = { username: this.username, password: this.password };
          this.$store.dispatch('login', credentials).then(() => {
              this.$router.push('/user/dashboard')
          });
      },
      onFeedbackSubmit: function () {

        //stub until implemented
        console.log("feedback submitted");
      },
      userSignUp: function () {
        var self = this;
        var firstName = this.fullName.split(' ')[0];
        var lastName = this.fullName.split(' ')[1];


        var endURL = "v1/user/create/";


        let payload = {

            email: this.email,
            username: this.username,
            first_name: firstName,
            last_name: lastName,
            password: this.password,
            profile: {
                avatar: null,
                gender: 'None',
                body_fat: 0,
                weight: 0,
                about: 'Default About',
            }
        };
        axios.post(baseURLLocal+endURL, payload
            ).then(function (response) {
                console.log("Success")
                self.signUpErrorAlert = true;
                self.signUpAlertMessage = "You have successfully created your account.";
                self.context = 'success';

            }).catch(function (errors) {

                self.signUpErrorAlert = true;
                self.signUpAlertMessage = "Sign ups have been limited during the early development stages." +
                    " Please submit a request for an account via the feedback area.";


                console.log(errors);
        })
      },

    },
    components: {
        'dashboard': dashboard,
        'user-dashboard': userDashboard,
    },
    mounted: function () {
        this.$store.dispatch('fetchUserProfile').then(() => {
              this.$router.push('/user/dashboard')
          });
    }
}
</script>
<style>
#header nav .navbar-brand img#header-logo {
    max-height: inherit;
}

    .logo-heading {
        letter-spacing: 2px;
        font-size: large;
        text-transform: uppercase;
        font-weight: 600;
    }

    @media only screen and (max-width: 768px) {
    /* For mobile phones: */
        .logo-heading {
            position: absolute;
            bottom: -65px;
            text-align: center;
            letter-spacing: 0.5px;
            font-size: large;
            color: white;
            text-transform: uppercase;
            font-weight: 600;
    }

        a.navbar-brand img#header-logo {
            max-height: 75px;
            max-width: none;
            position: absolute;
            left: -25px;
            height: 54px;
            width: 54px;

        }

        a.navbar-brand {
            margin-top: 10%;
            float: left;
        }


}
</style>
