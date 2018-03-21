<template>
    <v-app id="dashboard">
        <v-navigation-drawer

                :mini-variant.sync="mini"
                v-model="drawer"
                clipped
                app
                light

        >

                <v-list class="pa-0">
                    <v-list-tile avatar tag="div">
                        <v-list-tile-avatar>
                            <img :src="userAuth.user.avatar" />
                        </v-list-tile-avatar>
                        <v-list-tile-content>
                            <v-list-tile-title>{{ fullName }}</v-list-tile-title>
                        </v-list-tile-content>
                        <v-list-tile-action>
                            <v-btn icon @click.native.stop="mini = !mini">
                                <v-icon>chevron_left</v-icon>
                            </v-btn>
                        </v-list-tile-action>
                    </v-list-tile>
                </v-list>

            <v-list class="pt-0" dense>
                <v-divider class="divider-color"></v-divider>
                <v-list-tile v-for="item in items" :key="item.title" :to="item.link">
                    <v-list-tile-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar fixed clipped-left color="secondary" dark desnse app>
            <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-items>
                <img src="../assets/img/logo.png" style="width: 100px;">
            </v-toolbar-items>
            <v-container>
                <v-spacer></v-spacer>
                <v-layout justify-end>
                <v-speed-dial

                              v-model="fab"
                              top
                              right
                              direction="bottom"
                              transition="slide-y-reverse"
                              :style="fabDisplay"
                            >
                              <v-btn
                                slot="activator"
                                color="accent"
                                dark
                                fab
                                hover
                                v-model="fab"
                              >
                                <v-icon large style="top: unset!important;">account_circle</v-icon>
                                <v-icon style="top: unset!important;">close</v-icon>
                              </v-btn>
                              <v-btn
                                to="/create-workout/"
                                fab
                                dark
                                small
                                color="green"
                              >
                                <v-icon>add</v-icon>
                              </v-btn>
                              <v-btn
                                @click="activateSettings"
                                fab
                                dark
                                small
                                color="indigo"
                              >
                                <v-icon>settings</v-icon>
                              </v-btn>
                              <v-btn
                                fab
                                dark
                                small
                                color="red"
                                @click="logout"
                              >
                                <v-icon>power_settings_new</v-icon>
                              </v-btn>
                            </v-speed-dial>

                    </v-layout>
                <!--<v-layout row>
                    <v-flex offset-xs10 offset-md11 style="text-align: center">
                        <v-btn icon style="margin-bottom: 10%; position: absolute; top: -5px;"></v-btn>
                            <v-menu left>
                                <v-icon slot="activator" class="white--text" large>settings</v-icon>

                                <v-list>

                                    <v-list-tile @click="">
                                        <v-icon class="grey--text text--darken-4">settings</v-icon>
                                        <v-list-tile-title style="margin: 24px">Account Settings</v-list-tile-title>
                                    </v-list-tile>
                                    <v-list-tile @click="" @click.native.stop="dialog = true">
                                        <v-icon class="blue-grey--text text--darken-4">perm_identity</v-icon>
                                        <v-list-tile-title style="margin: 24px">Profile Settings</v-list-tile-title>
                                    </v-list-tile>
                                    <v-divider></v-divider>
                                    <v-list-tile @click="">
                                        <v-icon v-on:click="logout" class="red--text text--darken-2">power_settings_new</v-icon>
                                        <v-list-tile-title v-on:click="logout" style="margin: 24px">Log Off</v-list-tile-title>
                                    </v-list-tile>
                                </v-list>
                            </v-menu>

                    </v-flex>
                </v-layout>!-->
                <account-settings :computed-auth="computedAuth"></account-settings>
            </v-container>
        </v-toolbar>
        <v-content style="position: absolute; width: 100vw; background-color: #fafafa">
            <v-container fluid style="margin-bottom: 64px">
                
                <router-view :computed-auth="computedAuth"></router-view>
            </v-container>
        </v-content>
        <v-footer class="pa-3" app fixed>
            <p ><small>Last Build: </small>{{ "03/21/2018" | moment }}</p>
    <v-spacer></v-spacer>
    <div>© {{ new Date().getFullYear() }}</div>
            <p style="position: absolute; left: 50%">v0.4.7 </p>



  </v-footer>
    </v-app>
</template>

<script>

import { baseURLLocal } from '../auth/auth-utils'
import router from '../router/index'
import jwt_decode from 'jwt-decode'
import AccountSettings from '../components/account-settings.vue'
import axios from 'axios'
import moment from 'moment'



export default {
    name: 'dashboard',
    data () {
        return {
            snackbarMessage: 'Status will appear here',
            context: '',
            y: 'top',
            snackbar: false,
            userAuth: this.$store.state.userAuth,
            filename: '',
            username: this.$store.state.userAuth.user.username,
            about: this.computedAuth.about,
            wt: this.computedAuth.weight,
            bf: this.computedAuth.body_fat,
            genderSelect: null,
            bodyFatEdit: false,
            weightEdit: false,
            dialog: false,
            drawer: false,
            mini: false,
            right: null,

            items: [
                { title: 'Dashboard', icon: 'dashboard', link: '/user/dashboard/'},
                { title: 'Create Workout', icon: 'create', link: '/create-workout/' },
                { title: 'Manage Workouts', icon: 'schedule', link: '/manage/workouts/'},
                { title: 'Workout Stats', icon: 'trending_up', link: '/workout/stats/'},
                { title: 'Archived Workouts', icon: 'archive', link: '/archived-workouts/'}
            ],
            genderOpts: [
                { text: 'Female' },
                { text: 'Male' },
            ],
            fab: false,
            hover: true,

        }
    },
    props: ['computedAuth'],
    computed: {
        fullName: function (event) {
            return this.userAuth.user.first_name + ' ' + this.userAuth.user.last_name;
        },
        fabDisplay () {

            if (this.$vuetify.breakpoint.mdAndUp) {
                return ''; //don't make any modifications
            }
            else {
                return 'right: -50px; top: unset;';
            }

        },
    },
    filters: {
        moment: function (date) {
            return moment(date).format("MMM Do YY");
        }
    },

    methods: {
      activateSettings () {
          this.$store.commit('setAccountSettingsDialog', true)
      },

      saveBF: function (event) {
          this.bodyFatEdit = false;
          console.log(this.bf);
          this.bf = this.$refs.bfinput.value;
          this.computedAuth.body_fat = this.$refs.bfinput.value;
      },
      saveWt: function (event) {
          this.weightEdit = false;
          this.wt = this.$refs.wtInput.value;
          this.computedAuth.weight = this.$refs.wtInput.value;
      },
      logout: function (){
          this.$store.dispatch('logout');
      },
      getFormData (files) {
          const forms = []
          for (const file of files) {
              const form = new FormData()
              form.append('data', file, file.name)
              forms.push(form)
          }
          return forms
      },
      editBodyFat: function () {
          this.bodyFatEdit = !this.bodyFatEdit;

      },
      editWeight: function () {
          this.weightEdit = !this.weightEdit;

      },
      onFocus: function () {
          this.$refs.fileInput.click();
      },


    },
    components: {
        'account-settings': AccountSettings
    },
}

</script>

<style>

    #body-fat-edit > span > div > div > input {
        width: 25%;
        padding: 2px;
        font-size: 12px;
    }

    input[type=file] {
    position: absolute;
    left: -99999px;
  }

    .profile-card {
        margin: 0 25% 0 35%;
        width: 200px;
        height: 200px;
    }



     @media only screen and (max-width: 960px) {

        .profile-card {
            margin: 0 25% 0 25%;
            width: 200px;
            height: 200px;
        }

        .container.fluid {

            max-width: 100%;
            margin: 15% 0 0 0 ;
        }

    }


    .dark-primary-color    { background: #455A64; }
    .default-primary-color { background: #607D8B; }
    .light-primary-color   { background: #CFD8DC; }
    .text-primary-color    { color: #FFFFFF; }
    .accent-color          { background: #00BCD4; }
    .primary-text-color    { color: #212121; }
    .secondary-text-color  { color: #757575; }
    .divider-color         { border-color: #BDBDBD; }

</style>