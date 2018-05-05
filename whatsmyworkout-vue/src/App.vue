<template >
 <div v-if="isAuthenticated">
     <div v-if="computedAuth">
    <dashboard :computed-auth="computedAuth">
    </dashboard>
     </div>
</div>
    <v-app v-else-if="$route.path != '/' && !isAuthenticated">
        <router-view></router-view>
    </v-app>
    <v-app v-else="isAuthenticated" standalone>
    <header id="header" style="position: relative; border-bottom: 1px solid #78909C; background-image: linear-gradient(-152deg, #6937EA 0%, #377FEA 65%);" >
    <div class="container ">
        <div class="row ">
            <div class="col-md-12">
                <nav class="navbar navbar-toggleable-md navbar-dark bg-faded p-0">
                    <button @click="hide = false" id="show" class="navbar-toggler navbar-show navbar-toggler-right" type="button">
                        <v-icon>menu</v-icon>
                    </button>
                    <a class="navbar-brand" href="#header" style="margin-top: 0px !important; margin-right: 10%"><img
                            id="header-logo" src="https://s3.amazonaws.com/wmw-static/static/img/WMW2.png" alt="" class="img-fluid mr-5"
                            style="position: absolute; top: -45px; height: 150px; width: 200px; left: -90px; max-width: inherit"></a>
                    
                    <div class="collapse navbar-collapse align-items-center">
                        <ul class="navbar-nav mr-auto ">
                            <li class="nav-item active mr-3">
                                <a class="nav-link blue-grey--text text--darken-4 title" href="#header" style="color: #FFFFFF !important;">Home <span class="sr-only">(current)</span></a>
                            </li>
                            <li class="nav-item mr-3">
                                <a class="nav-link blue-grey--text text--darken-4 title" href="#features" style="color: #FFFFFF !important;">Features</a>
                            </li>
                            <li class="nav-item mr-3">
                                <a class="nav-link blue-grey--text text--darken-4 title" href="#contact" style="color: #FFFFFF !important;">Contact</a>
                            </li>
                            <li class="nav-item mr-3">
                                <a class="nav-link blue-grey--text text--darken-4 title" href="#about" style="color: #FFFFFF !important;">About</a>
                            </li>
                        </ul>
                        <span class="navbar-text">
                            <a href="#signup" class="font-weight-bold">Sign Up</a>
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
                                        <a @click="hide = true" class="nav-link" href="#contact">Contact</a>
                                    </li>
                                    <li class="nav-item">
                                        <a @click="hide = true" class="nav-link" href="#about">About</a>
                                    </li>
                                </ul>
                                <div>
                        <span class="navbar-text">
                            <a @click="hide = true" href="#signup" class="font-weight-bold">Sign Up</a>
                        </span>
                        <span class="navbar-text">
                            <a @click="hide = true" href="#login" class="font-weight-bold">Sign In</a>
                        </span>
                                </div>
                            </div>
                        </div>

                        <div class="bottom ">
                             <v-divider ></v-divider>
                            <img src="https://s3.amazonaws.com/wmw-static/static/img/WMW2.png" alt="" class="img-fluid mb-2" style="width: 86px; height: 54px; max-height: none;">
                            <p class="mb-0 mt-3">&copy; 2017 What's My Workout</p>
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

<!--<section class="hero hero-1">
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
                <a href="#signup" style="padding-left: 5%" class="btn text-md-center blue--text font-weight-bold text-uppercase">Checkout What's My Workout Now!</a>
            </div>
            <div class="col-lg-6 text-right d-lg-block">
                <img id="mockup" style="top: -90px;" src="../src/assets/img/Untitled.png" alt="" class="mockup hidden-sm-and-down">
            </div>
        </div>
    </div>
</section>-->

<section class="features features-1 pt-5 mt-5 pb-5 mb-4" style="background-image: linear-gradient(-45deg, #122e57 0%, #4b3190 75%); margin: 0px !important; padding: 72px 0px 72px 0px !important;">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-3 preamble">
                <h4 class="title mt-0 mb-3" style="color: #FFFFFF !important;">Stop taking your clipboard to the gym!</h4>
                <p class="lead pr-5 text-center" style="padding-right: 0px !important; color: #cccccc !important;">Easily keep track of your workouts and share them with others, trainer and trainee style.</p>
            </div>
            <div class="col-lg-12 mb-12 text-center"><img src="../src/assets/img/hero.png" style="width: calc(100% - 300px); min-width: 300px; max-width: 1035px;"></div>
        </div>
    </div>
</section>

<section id="features" class="features features-1 pt-5 mt-5 pb-5 mb-4" style="background-image: linear-gradient(-45deg, #FFFFFF 0%, #DDDDDD 75%); margin: 0px !important; padding: 72px 0px 72px 0px !important;">
    <div class="container">
        <div class="row">
            <div class="col-lg-4 mb-4 ">
                <div class="single-feature text-center p-5 rounded " style="background-color: #FFFFFF !important;">
                    <img src="../src/assets/img/planner.svg" alt="" class="img-fluid mb-4 pb-2 rounded-circle">
                    <h5 class="title mt-0 mb-3 font-weight-bold grey--text text--darken-4">Plan Your Workouts</h5>
                    <p class="mb-0 blue-grey--text text--darken-1 ">Create and plan your workouts in advance for easy viewing at the gym on any mobile device.</p>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="single-feature text-center p-5 rounded" style="background-color: #FFFFFF !important;">
                    <img src="../src/assets/img/line-chart.svg" alt="" class="img-fluid mb-4 pb-2">
                    <h5 class="title mt-0 mb-3 font-weight-bold grey--text text--darken-4">Workout Stats</h5>
                    <p class="mb-0 blue-grey--text text--darken-1">Track your stats such as body fat and weight. Plus keep track of the weight you are lifting for each exercise.</p>
                </div>
            </div>
            <div class="col-lg-4 mb-4">
                <div class="single-feature text-center p-5 rounded " style="background-color: #FFFFFF !important;">
                    <img src="../src/assets/img/dumbbell.svg" alt="" class="img-fluid mb-4 pb-2 rounded-circle">
                    <h5 class="title mt-0 mb-3 font-weight-bold grey--text text--darken-4">Strength Training</h5>
                    <p class="mb-0 blue-grey--text text--darken-1">Keep current on your training plans and sessions with simple exercise and workout creation.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<section id="login" class="tour" style="background-image: linear-gradient(-45deg, #377FEA 0%, #7954db 75%);">
    <div class="part pt-5 pb-5">
        <div class="container">
            <div class="row d-flex align-items-center">
                <div class="col-md-6 preamble">
                    <h4 class="title pt-3 mb-3 pr-5 text-center" style="padding-right: 0px !important; color: #FFFFFF !important;">
                        Got an account with us?
                    </h4>
                    <p class="lead pr-5 text-center" style="padding-right: 0px !important; color: #cccccc !important;">Sign in to access your dashboard, workouts, calendar and more.</p>
                </div>
                <div class="col-md-6 text-center">
                        <v-card >
                            <v-card-text>
                                    <v-layout row wrap >
                                        <v-flex xs12 class="text-xs-center">
                                            <h6 class="grey--text text--darken-3">Provide your credentials to login</h6>
                                        </v-flex>
                                    </v-layout>
                                    <form v-on:submit.prevent="userLogin" method="post">
                                        <v-layout row wrap justify-center>

                                            <v-flex xs12 md7 text-xs-center>
                                                <v-text-field v-model="loginUsername"
                                                              label="Username"
                                                              prepend-icon="account_circle"
                                                              required
                                                ></v-text-field>
                                            </v-flex>
                                            <v-flex xs12 md7 text-xs-center>
                                                <v-text-field v-model="loginPassword"
                                                                label="Password"
                                                                prepend-icon="vpn_key"
                                                                type="password"
                                                                required
                                                ></v-text-field>
                                            </v-flex>
                                              <v-flex xs12 md7 text-xs-center>
                                                  <v-btn small outline color="secondary" @click.prevent.stop="passwordResetDialog = !passwordResetDialog">
                                                      Forgot Password
                                                  </v-btn>
                                          </v-flex>
                                            <v-flex xs12>
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
    <v-layout row justify-center v-if="passwordResetDialog">
    <v-dialog v-model="passwordResetDialog" max-width="500">
       <v-flex xs12 >
            <v-card class="elevation-12">
              <v-toolbar dark class="blue lighten-1">
                <v-toolbar-title>Password Reset</v-toolbar-title>
                <v-spacer></v-spacer>

              </v-toolbar>
              <v-card-text>
                <v-flex xs12>
                    <p class="subheading grey--text text--darken-2">{{ resetText }}</p>
                </v-flex>
                <v-form v-model="passwordFormValid">
                  <v-text-field v-model="forgotPasswordEmail" required prepend-icon="person" name="login" label="Email" type="text"></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn flat color="warning" @click.prevent.stop="closePasswordResetDialog">Close</v-btn>
                <v-btn color="primary" :disabled="forgotPasswordDisabled" @click="submitPasswordResetRequest">Submit</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
    </v-dialog>
  </v-layout>
</section>

<section id="signup" style="background-image: linear-gradient(-45deg, #7954db 0%, #377FEA 75%);">
    <div class="part pt-5 pb-5">
        <div class="container">
            <div class="row d-flex align-items-center">
                <div class="col-md-6 preamble">
                    <h4 class="title pt-3 mb-3 pr-5 text-center" style="padding-right: 0px !important; color: #FFFFFF !important;">
                        Need an account?
                    </h4>
                    <p class="lead pr-5 text-center" style="padding-right: 0px !important; color: #cccccc !important;">Sign up to start creating &amp; tracking your workouts today!</p>
                </div>
                <div class="col-md-6 text-center">
                    <v-card >
                      <v-alert error v-model="signUpErrorAlert" transition="scale-transition">{{ signUpAlertMessage }}</v-alert>
                        <v-card-text>
                                <v-layout row wrap>
                                    <v-flex xs12 md12>
                                        <v-subheader display-4>Fill out the information below to create an account!</v-subheader>
                                    </v-flex>
                                </v-layout>
                                <form v-on:submit.prevent="userSignUp" method="post">
                                    <v-layout row wrap>
                                        <v-flex xs11 md5>
                                            <v-text-field v-model="fullName"
                                                          label="First & Last Name"
                                                          prepend-icon="person"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                        <v-flex xs11 md6>
                                            <v-text-field v-model="email"
                                                          label="Email"
                                                          prepend-icon="email"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                    </v-layout>
                                    <v-layout row>
                                        <v-flex xs11>
                                            <v-text-field v-model="username"
                                                          label="Username"
                                                          prepend-icon="account_circle"
                                                          required
                                            ></v-text-field>
                                        </v-flex>
                                    </v-layout>
                                      <v-layout row wrap>
                                        <v-flex xs11 md5>
                                            <v-text-field v-model="password"
                                                            label="Password"
                                                            prepend-icon="vpn_key"
                                                            type="password"
                                                            required
                                            ></v-text-field>
                                        </v-flex>
                                          <v-flex xs11 md6>
                                            <v-text-field v-model="confirmPass"
                                                          label="Confirm Password"
                                                          prepend-icon="vpn_key"
                                                          type="password"
                                                          required
                                            ></v-text-field>
                                        </v-flex>

                                    </v-layout>
                                    <v-layout row>
                                        <v-flex xs12>
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

<!-- <section id="feedback" class="services services-1 pt-5 pb-5">
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
</section>-->

<!--<section id="newsletter" class="newsletter pt-5 pb-5">
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
</section>-->

<section id="contact" class="features pt-5 pb-5" style="background-image: linear-gradient(-62deg, #AAAAAA 0%, #FFFFFF 50%, #AAAAAA 100%);">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-4 preamble">
                <h4 class="title mt-0 mb-3">Stay In Contact</h4>
                <p class="lead mb-5">Follow us on social media to be alerted of updates throughout the development process including new feature drops!</p>
            </div>
            <div class="col-lg-6 offset-lg-3 col-md-8 offset-md-2 col-sm-12 offset-sm-0" style="text-align: center;">
                <a href="https://www.facebook.com/whatsmyworkout" target="_blank"><img src="../src/assets/img/facebook.png"></a><a href="https://www.twitter.com/whatsmyworkout" target="_blank"><img src="../src/assets/img/twitter.png" style="margin-left: 25px;"></a>
            </div>
        </div>
    </div>
</section>

<section id="about" class="newsletter pt-5 pb-5" style="background-image: linear-gradient(-45deg, #122e57 0%, #4b3190 75%);">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 text-center mt-4 preamble">
                <h4 class="title mt-0 mb-3">A Little About Us</h4>
            </div>
            <div class="col-lg-8 offset-lg-2 col-md-10 offset-md-1 col-sm-12 offset-sm-0">
                <p style="color: #EEEEEE !important;">What's My Workout began as a senior project for a few Information Technology students at the University of Kansas. We saw a need in the workout industry for being able to collaborate with others in a trainer-trainee format and set out to build a web application that does just that.</p>
                <p style="color: #EEEEEE !important;">Whether you're a trainer or trainee, you'll find What's My Workout easy to use. The app allows you to view the workout of other members and vice versa. You can also subscribe to other members so they can send you workouts they've created or have others subscribe to you so you can send them workouts that you've created.</p>
                <p style="color: #EEEEEE !important;">Overtime, additional features and functionality will be added. Be sure to <a href="#signup">create an account</a> and <a href="#contact">follow us on social media</a> to stay up to date on our progress.</p>
            </div>
        </div>
    </div>
</section>

<footer id="footer" class="pt-5 pb-5 mb-0 mb-lg-4">
    <div class="container">
        <div class="row d-flex">
            <div class="col-lg-6 text-xs-center">
                <img src="https://s3.amazonaws.com/wmw-static/static/img/WMW2.png"
                     alt="" class="img-fluid mb-2"
                     style="width: 200px; height:150px;
                     max-height: none;">
                <p class="mb-0 mt-3" >&copy; 2018 What's My Workout</p>
            </div>
            <div class="col-lg-3 d-none d-lg-block">
                <div class="row"><a href="#header" class="font-weight-bold">Home</a></div>
                <div class="row"><a href="#features" class="font-weight-bold">Features</a></div>
                <div class="row"><a href="#contact" class="font-weight-bold">Contact</a></div>
                <div class="row"><a href="#about" class="font-weight-bold">About</a></div>
            </div>
            <div class="col-lg-3 d-none d-lg-block">
                <div class="row"><a href="#signup" class="font-weight-bold">Sign Up</a></div>
                <div class="row"><a href="#login" class="font-weight-bold">Sign In</a></div>
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
      passwordResetDialog: false,
      forgotPasswordDisabled: false,
      forgotPasswordEmail: null,
      passwordFormValid: false,
      resetText: 'Please provide the email address that was used when you setup your account.',


      drawer: true,
      alert: true,
      signUpErrorAlert: false,
      signUpAlertMessage: ' ',
       hide: true,
      items: [
          { title: 'Home', icon: 'dashboard' },
          { title: 'About', icon: 'question_answer' }
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
      $router () {
          console.log(this.$route);

      }
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
      closePasswordResetDialog () {
          this.passwordResetDialog = false;
          this.resetText = 'Please provide the email address that was used when you setup your account.';
      },
      submitPasswordResetRequest () {
        this.forgotPasswordDisabled = true;
        let payload = { email: this.forgotPasswordEmail};
        delete axios.defaults.headers.common['Authorization'];

        axios.post(baseURLLocal+'v1/forgot-password-reset/', payload).then(response => {
            this.forgotPasswordDisabled = false;
            console.log(response);
            this.resetText = response.data.status;
        }).catch(err => {
            this.forgotPasswordDisabled = false;
            console.log(err);
        })
      },
       userLogin: function () {
          let credentials = { username: this.loginUsername, password: this.loginPassword };
          /*this.$store.dispatch('login', credentials).then((r) => {
              console.log('Login', r);
              this.$router.push('/user/dashboard')
          });*/

           axios.post(baseURLLocal+'v1/login/', credentials
            ).then(response => {
                let JWT = response.data.token;
                localStorage.setItem("JWT", JWT);
                this.$store.commit('setUserAuth', response.data.user);
                this.$router.push('/user/dashboard')
            }).catch(err => {
                console.log(err);

            })
      },

      onFeedbackSubmit: function () {

        //stub until implemented
        console.log("feedback submitted");
      },
      userSignUp: function () {
        delete axios.defaults.headers.common['Authorization'];
        let self = this;
        let firstName = this.fullName.split(' ')[0];
        let lastName = this.fullName.split(' ')[1];

        let payload = {

            email: this.email,
            username: this.username,
            first_name: firstName,
            last_name: lastName,
            password: this.password,
            profile: {
                avatar: null,
                gender: 'None',
                about: 'Default About',
            }
        };

        this.$store.dispatch('newUser', payload).then(() => {

            self.signUpErrorAlert = true;
            self.signUpAlertMessage = "You have successfully created your account.";
            self.context = 'success';
        }).catch(() => {

            self.signUpErrorAlert = true;
            self.signUpAlertMessage = "Sign ups have been limited during the early development stages." +
                    " Please submit a request for an account via the feedback area.";
            console.log(errors);
        });
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


    },

    created () {
      this.$router.push(this.$route.path);
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
