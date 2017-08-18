<template >
 <v-app v-if="isAuthenticated">
     <div v-if="computedAuth">
    <dashboard :computed-auth="computedAuth"></dashboard>
     </div>
</v-app>
    <v-app v-else="isAuthenticated" standalone>
        <div>
            <v-toolbar fixed class="transparent theme--dark"  dark>
              <v-toolbar-title><img src="../src/assets/img/logo.png" class="rounded-circle size-for-mobile"></v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                  <a class="btn btn--flat grey--text text--darken-4 title" >Sign up</a>
                  <router-link to="/login/" class="btn btn--flat grey--text text--darken-4 title">Login</router-link>
              </v-toolbar-items>

            </v-toolbar>
            <section v-show="hero" id="hero" class="elevation-12">
                <div class="parallax" style="height: 400px;">
                    <div class="parallax_image-container">
                        <img src="../src/assets/img/gym.jpg" class="parallax__image" style="height: 400px; width: 199px; display: block; opacity: .6">
                    </div>
                    <div class="parallax__content">
                        <div class="layout row align-vert-center align-horiz-center">
                            <div class="flex text-xs-center xs12">
                                <h1 class="text--blue-grey darken-4  display-2">What's My Workout?</h1>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <main>
                <v-container fluid>
                    <router-view></router-view>
              </v-container>
            </main>

        </div>
        <v-footer style="position: absolute; width: 100%; bottom: 0; height: 100px">
                <v-spacer></v-spacer>
                <div>copy Levi Heidrick</div>
        </v-footer>
  </v-app>
</div>
</template>

<script>

import { userAuth, login, authenticationStatus, logout, getUserAccount, getJWTHeader, setUserAuth } from '../src/auth/auth'
import router from '../src/router/index'
import jwt_decode from 'jwt-decode'
import axios from 'axios'
import dashboard from '../src/components/dashboard.vue'

export default {
  name: 'app',
  data () {
    return {
      drawer: true,
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
      isAuthenticated: authenticationStatus(),
      username: '',
      password: '',
      userAuth: userAuth,
      hero: true,
    }
  },
    watch: {
      isAuthenticated: function () {
          router.go('/');
      }
    },
    computed: {
      computedAuth: function () {
          if (!this.userAuth.user) return null;
          return this.userAuth.user;
      }
    },
    methods: {
      logout: function (){
          logout();
          router.go('/')
      }

    },
    components: {
      'dashboard': dashboard
    },
    mounted: function () {
        var self = this;
        if (this.isAuthenticated) {
            var JWT = localStorage.getItem("JWT");
            axios.defaults.headers.common['Authorization'] = getJWTHeader();
            var decoded = jwt_decode(JWT);
            axios.get("http://127.0.0.1:8000/" + "v1/users/" + decoded.username +'/')
                .then(function (response) {
                    userAuth.user = response.data;

                }).catch(function (err) {
                    console.log(err)
            });
            console.log(userAuth);
        }
    }
}
</script>

