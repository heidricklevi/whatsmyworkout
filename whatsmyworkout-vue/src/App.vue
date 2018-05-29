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
    <v-app v-else="isAuthenticated">
        <v-navigation-drawer
                clipped
                v-model="landingDrawer"
                dark
                fixed
                app
        >
            <v-list dense>
                <v-list-tile href="#home">
                  <v-list-tile-action>
                    <v-icon>home</v-icon>
                  </v-list-tile-action>
                  <v-list-tile-content>
                    <v-list-tile-title>Home</v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-list-tile href="#features">
                  <v-list-tile-action>
                    <v-icon>explore</v-icon>
                  </v-list-tile-action>
                  <v-list-tile-content>
                    <v-list-tile-title>Features</v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-list-tile href="#contact">
                  <v-list-tile-action>
                    <v-icon>record_voice_over</v-icon>
                  </v-list-tile-action>
                  <v-list-tile-content>
                    <v-list-tile-title>Contact</v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-list-tile href="/#about">
                  <v-list-tile-action>
                    <v-icon>info</v-icon>
                  </v-list-tile-action>
                  <v-list-tile-content>
                    <v-list-tile-title>About WMW</v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <v-list-tile class="mt-3" href="#signin">
                      <v-list-tile-action>
                        <v-icon color="grey darken-1">person</v-icon>
                      </v-list-tile-action>
                      <v-list-tile-title class="grey--text text--darken-1">Login</v-list-tile-title>
                    </v-list-tile>
                    <v-list-tile href="#signup">
                      <v-list-tile-action>
                        <v-icon color="grey darken-1">chrome_reader_mode</v-icon>
                      </v-list-tile-action>
                      <v-list-tile-title class="grey--text text--darken-1">Register</v-list-tile-title>
                    </v-list-tile>
              </v-list>

        </v-navigation-drawer>
        <v-toolbar
              clipped-left
              style="border-bottom: 1px solid #78909C; background-image: linear-gradient(-152deg, #6937EA 0%, #377FEA 65%);"
              dark
              app
              fixed
            >
              <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
                <v-toolbar-side-icon @click.stop="landingDrawer = !landingDrawer"></v-toolbar-side-icon>
                <span class="hidden-sm-and-down">What's My Workout?</span>
              </v-toolbar-title>
              <v-spacer></v-spacer>

                <div style="margin-top: 5px; width: 190px!important; height: 140px!important;" class="hidden-sm-and-down">
                  <img
                    src="https://s3.amazonaws.com/wmw-static/static/img/WMW2.png"
                    alt="WMW"
                    style="width: 100%; height: 100%;"
                  >
                </div>
                <div style="margin-top: 5px; margin-right: -30px; width: 260px!important; height: 140px!important;" class="hidden-md-and-up">
                  <img
                    src="https://s3.amazonaws.com/wmw-static/static/img/WMW2.png"
                    alt="WMW"
                    style="width: 100%; height: 100%;"
                  >
                </div>
            </v-toolbar>
        <v-content class="pa-0">
            <v-container fluid class="mt-0 pb-0 px-0">
                <v-layout id="home" row wrap align-center justify-center class="pa-2" style="background-image: linear-gradient(-45deg, #122e57 0%, #4b3190 75%);">
                            <v-container fill-height>
                                <v-layout align-center justify-center row wrap>
                                    <v-flex xs12 class="mt-4 py-4" text-xs-center>
                                        <h4 class="title mt-4 mb-3 white--text" style="color: #FFFFFF !important;">Stop taking your clipboard to the gym!</h4>
                                        <p class="pr-5 text-center white--text" style="padding-right: 0px !important; color: #cccccc !important;">
                                            Easily keep track of your workouts and share them with others, trainer and trainee style.</p>
                                    </v-flex>

                                    <v-flex xs12 text-xs-center>
                                        <img src="../src/assets/img/hero.png" style="width: calc(100% - 300px); min-width: 300px; max-width: 1035px;">
                                    </v-flex>

                                </v-layout>
                            </v-container>
                </v-layout>
                <v-layout id="features" row wrap style="background-image: linear-gradient(-45deg, #FFFFFF 0%, #DDDDDD 75%);" justify-center class="pa-5">

                        <v-flex xs12 md3 class="ma-4" text-xs-center>
                            <v-card class="elevation-8">
                                <v-card-media>
                                    <img src="../src/assets/img/line-chart.svg">
                                </v-card-media>

                                <v-card-text>
                                     <h5 class="title mt-0 mb-3 font-weight-bold grey--text text--darken-4">Workout Stats</h5>
                                    <p class="mb-0 blue-grey--text text--darken-1">Track your stats such as body fat and weight. Plus keep track of the weight you are lifting for each exercise.</p>

                                </v-card-text>
                            </v-card>
                        </v-flex>
                       <v-flex xs12 md3 class="ma-4" text-xs-center>
                            <v-card class="elevation-8 ">
                                <v-flex xs12 d-flex justify-center align-center>
                                    <div style="max-width: 128px; height: 136px; text-align: center" class="my-3">
                                        <img src="../src/assets/img/planner.svg" style="width: 100%;">
                                    </div>
                                </v-flex>
                                <v-card-text>
                                      <h5 class="title mt-0 mb-3 font-weight-bold grey--text text--darken-4">Plan Your Workouts</h5>
                                        <p class="mb-0 blue-grey--text text--darken-1 ">Create and plan your workouts in advance for easy viewing at the gym on any mobile device.</p>

                                </v-card-text>
                            </v-card>
                        </v-flex>
                       <v-flex xs12 md3 class="ma-4" justify-center>
                            <v-card class="elevation-8 text-xs-center">
                                    <v-flex xs12 d-flex justify-center align-center>
                                        <div style="max-width: 128px; height: 136px; " class="my-3">
                                            <img src="../src/assets/img/dumbbell.svg">
                                        </div>
                                    </v-flex>

                                <v-card-text>
                                     <h5 class="title mt-0 mb-3 font-weight-bold grey--text text--darken-4">Strength Training</h5>
                                    <p class="mb-0 blue-grey--text text--darken-1">Keep current on your training plans and sessions with simple exercise and workout creation.</p>

                                </v-card-text>
                            </v-card>
                        </v-flex>
                </v-layout>
                <v-layout id="signin" row wrap style="background-image: linear-gradient(-45deg, #377FEA 0%, #7954db 75%);" justify-center class="pa-5">
                    <v-flex md4 xs12 text-xs-center class="pt-5 mt-4">
                    <h4 class="title pt-3 mb-3 pr-5 text-center" style="padding-right: 0px !important; color: #FFFFFF !important;">
                        Got an account with us?
                    </h4>
                    <p class="pr-5 text-center" style="padding-right: 0px !important; color: #cccccc !important;">Sign in to access your dashboard, workouts, calendar and more.</p>
                    </v-flex>
                    <v-flex xs12 offset-md2 md4 text-xs-center>
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
                    </v-flex>
                </v-layout>
                <v-layout id="signup" row wrap  style="background-image: linear-gradient(-45deg, #7954db 0%, #377FEA 75%);" justify-center class="pa-5">
                    <v-flex md4 xs12 text-xs-center class="pt-5 mt-4">
                    <h4 class="title pt-3 mb-3 pr-5 text-center" style="padding-right: 0px !important; color: #FFFFFF !important;">
                        Need an account?
                    </h4>
                    <p class="pr-5 text-center" style="padding-right: 0px !important; color: #cccccc !important;">Sign up to start creating &amp; tracking your workouts today!</p>
                    </v-flex>
                    <v-flex xs12 offset-md2 md4 text-xs-center>
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
                    </v-flex>
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
                </v-layout>
                <v-layout id="contact" row wrap style="background-image: linear-gradient(-62deg, #AAAAAA 0%, #FFFFFF 50%, #AAAAAA 100%);" class="py-4 px-3">


                            <v-flex md10 offset-md1 text-xs-center class="mt-4">
                                <h4 class="title mt-0 mb-3">Stay In Contact</h4>
                                <p class="mb-5">Follow us on social media to be alerted of updates throughout the development process including new feature drops!</p>
                            </v-flex>
                            <v-flex md8 offset-md2 xs12 class="text-xs-center">
                                <a href="https://www.facebook.com/whatsmyworkout" target="_blank"><img src="../src/assets/img/facebook.png"></a><a href="https://www.twitter.com/whatsmyworkout" target="_blank"><img src="../src/assets/img/twitter.png" style="margin-left: 25px;"></a>
                            </v-flex>


                </v-layout>
                <v-layout id="about" row wrap class="pt-5 pb-5" style="background-image: linear-gradient(-45deg, #122e57 0%, #4b3190 75%);">
                    <v-container><v-flex md10 xs12 offset-md1 class="mt-4" text-xs-center>
                    <h4 class="title mt-0 mb-3 white--text">A Little About Us</h4>
                    </v-flex>
                    <v-flex xs12 md10 offset-md1 offset-xs0>
                        <p style="color: #EEEEEE !important;">What's My Workout began as a senior project for a few Information Technology students at the University of Kansas. We saw a need in the workout industry for being able to collaborate with others in a trainer-trainee format and set out to build a web application that does just that.</p>
                        <p style="color: #EEEEEE !important;">Whether you're a trainer or trainee, you'll find What's My Workout easy to use. The app allows you to view the workout of other members and vice versa. You can also subscribe to other members so they can send you workouts they've created or have others subscribe to you so you can send them workouts that you've created.</p>
                        <p style="color: #EEEEEE !important;">Overtime, additional features and functionality will be added. Be sure to <a href="#signup">create an account</a> and <a href="#contact">follow us on social media</a> to stay up to date on our progress.</p>
                    </v-flex>
                        </v-container>
                </v-layout>

                  <!--<router-view></router-view>-->
            </v-container>
        </v-content>
        <v-footer dark app height="auto" style="position: static!important;">

                    <v-layout row wrap align-center justify-center class="pt-3">
                        <v-flex md4 xs12 text-md-right text-xs-center>
                            <div class="pb-1"><a href="#home" class="title white--text">Home</a></div>
                            <div class="pb-1"><a href="#features" class="title white--text">Features</a></div>
                            <div class="pb-1"><a href="#contact" class="title white--text">Contact</a></div>
                            <div><a href="#about" class="title white--text">About</a></div>
                        </v-flex>
                        <v-flex md4 xs12 text-md-center text-xs-center>
                            <div class="pb-1"><a href="#signup" class="title white--text">Sign Up</a></div>
                            <div><a href="#signin" class="title white--text">Sign In</a></div>
                        </v-flex>
                        <v-flex xs12 md4 text-md-left text-xs-center>
                            <img src="https://s3.amazonaws.com/wmw-static/static/img/WMW2.png"
                                 alt="" class="mb-2"
                                 style="width: 200px; height:150px;
                                 max-height: none;">
                        </v-flex>
                        <v-flex xs12 text-xs-center class="mb-3">
                             <p >&copy; 2018 What's My Workout</p>
                        </v-flex>
                    </v-layout>
            </v-footer>
  </v-app>
</template>

<script>

import { baseURLLocal } from './auth/auth-utils'
import axios from 'axios'
import dashboard from './components/shell-components/dashboard.vue'
import userDashboard from './components/user-dashboard/user-dashboard.vue'

export default {
  name: 'app',
  data () {
    return {

      landingDrawer: false,


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
