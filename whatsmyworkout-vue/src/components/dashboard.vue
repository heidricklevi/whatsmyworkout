<template>
    <v-app id="dashboard">
        <v-navigation-drawer
                light
                :mini-variant.sync="mini"
                v-model="drawer"
                clipped
                app
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
                <v-divider></v-divider>
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
        <v-toolbar fixed clipped-left class="indigo darken-4" desnse app>
            <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-items>
                <img src="../assets/img/logo.png" style="width: 100px;">
            </v-toolbar-items>
            <v-container>
                <v-spacer></v-spacer>
                <v-layout row>
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
                </v-layout>
                <v-dialog :computed-auth="computedAuth" v-model="dialog" fullscreen transition="dialog-bottom-transition" :overlay=false>
                    <v-layout row justify-center wrap>
                        <v-flex xs12 md6>
                            <v-card style="width: 100%">
                                <v-toolbar dark class="primary">

                                    <v-btn icon @click.native="dialog = false" dark>
                                        <v-icon>close</v-icon>
                                    </v-btn>
                                    <v-toolbar-title>{{ userAuth.user.username }}'s Profile</v-toolbar-title>
                                    <v-spacer></v-spacer>
                                    <v-toolbar-items>
                                        <v-btn dark flat @click.native="updateProfile">Save</v-btn>
                                    </v-toolbar-items>
                                </v-toolbar>
                                <form id="profile-form" enctype="multipart/form-data" method="post" @submit.prevent="updateProfile">
                                <v-card-media :src="userAuth.user.avatar" style="height: 250px">

                                    <v-btn class="blue-grey white--text" @click.native="onFocus" style="position: absolute; bottom: 0; right: 0">
                                        Change
                                        <v-icon right dark>cloud_upload</v-icon>
                                        <input  id="image" type="file" ref="fileInput" @change="onFileChange">
                                        <span v-model="filename"></span>
                                    </v-btn>
                                </v-card-media>
                                <v-list three-line subheader>
                                    <v-subheader>Profile Settings</v-subheader>
                                    <li class="ma-3">
                                        <v-layout>
                                            <v-flex xs12 sm12 md4 offset-md2>
                                                <v-list-tile-title>Username</v-list-tile-title>
                                            </v-flex>

                                            <v-flex xs12 sm12 md6>
                                                <v-text-field v-model="username"
                                                              name="username"
                                                              :label="userAuth.user.username"
                                                              prepend-icon="perm_identity"
                                                              single-line></v-text-field>
                                            </v-flex>
                                        </v-layout>
                                    </li>
                                    <li class="ma-3">
                                        <v-layout>
                                            <v-flex xs12 sm12 md4 offset-md2>
                                                <v-list-tile-title>Gender</v-list-tile-title>
                                            </v-flex>
                                            <v-flex xs12 sm12 md6>
                                                <v-select v-bind:items="genderOpts"
                                                          v-model="genderSelect"
                                                          :label="userAuth.user.gender"></v-select>
                                            </v-flex>
                                        </v-layout>
                                    </li>
                                    <li class="ma-3">
                                        <v-layout row>
                                            <v-flex xs11 offset-xs1 sm12 md4 offset-md2>
                                                <v-list-tile-title>Weight, Body Fat</v-list-tile-title>
                                            </v-flex>
                                            <v-flex xs3 md2 v-show="weightEdit" id="weight-edit">
                                                    <v-text-field v-model="wt" type="number" ref="wtInput" suffix="lbs."></v-text-field>
                                            </v-flex>
                                            <v-flex xs6 md2 v-show="weightEdit">
                                                     <v-btn  @click.native="saveWt" icon class="blue-grey--text" style="margin-top: -5%; margin-left: -5%">
                                                    <v-icon style="font-size: 16px">check_circle</v-icon></v-btn>
                                                <v-btn  @click.native="editWeight" icon class="red--text" style="margin-top: -5%; margin-left: -5%">
                                                    <v-icon style="font-size: 16px">cancel</v-icon></v-btn>
                                            </v-flex>
                                            <v-flex xs3 md2 class="" v-show="!weightEdit">
                                                <v-chip>
                                                    <div><span>{{ computedAuth.weight }} lbs.</span></div>
                                                </v-chip>
                                                <v-btn icon @click.native="editWeight" class="blue-grey--text" style="margin-top: -20%; margin-left: -23%">
                                                    <v-icon style="font-size: 16px">edit</v-icon></v-btn>
                                            </v-flex>
                                            <v-flex xs3 md1 v-show="bodyFatEdit" id="body-fat-edit">
                                                    <v-text-field v-model="bf" type="number" ref="bfinput" suffix="%"></v-text-field>
                                            </v-flex>
                                            <v-flex xs6 md2 v-show="bodyFatEdit">
                                                     <v-btn  @click.native="saveBF" icon class="blue-grey--text" style="margin-top: -5%; margin-left: -5%">
                                                    <v-icon style="font-size: 16px">check_circle</v-icon></v-btn>
                                                <v-btn  @click.native="editBodyFat" icon class="red--text" style="margin-top: -5%; margin-left: -5%">
                                                    <v-icon style="font-size: 16px">cancel</v-icon></v-btn>
                                            </v-flex>
                                            <v-flex xs3 md2 v-show="!bodyFatEdit">
                                                <v-chip>
                                                    <div v-model="bf"><span>{{ computedAuth.body_fat }} %</span></div>
                                                </v-chip>
                                                <v-btn icon @click.native="editBodyFat" class="blue-grey--text" style="margin-top: -20%; margin-left: -20%">
                                                    <v-icon style="font-size: 16px">edit</v-icon></v-btn>
                                            </v-flex>

                                        </v-layout>
                                    </li>
                                    <li class="ma-3">
                                        <v-layout row>
                                            <v-flex xs11 offset-xs1 offset-md2>
                                                <v-divider></v-divider>
                                                <v-text-field
                                                    label="write something about yourself (e.g. goals in the gym, hobbies etc)"
                                                    v-model="about"
                                                    counter
                                                    max="500"
                                                    multi-line
                                                    single-line
                                                    >
                                                    {{ computedAuth.about }}
                                                </v-text-field>
                                            </v-flex>
                                        </v-layout>
                                    </li>
                                </v-list>
                                    </form>
                            </v-card>

                            <v-snackbar
                            :top="y === 'top'"
                            v-model="snackbar"
                            :success="context === 'success'"
                            :error="context === 'error'">
                                {{ snackbarMessage }}
                                <v-btn flat class="red--text" @click.native="snackbar = false">Close</v-btn>
                            </v-snackbar>
                        </v-flex>
                    </v-layout>
                </v-dialog>
            </v-container>
        </v-toolbar>
        <v-content style="position: absolute; width: 100vw; background-color: #fafafa">
            <v-container fluid style="margin-bottom: 64px">
                
                <router-view :computed-auth="computedAuth"></router-view>
            </v-container>
        </v-content>
        <v-footer class="pa-3" app fixed>
    <v-spacer></v-spacer>
    <div>© {{ new Date().getFullYear() }}</div>
    <p style="position: absolute; left: 50%">v0.2.1 02/05</p>

  </v-footer>
    </v-app>
</template>

<script>

import { baseURLLocal } from '../auth/auth-utils'
import router from '../router/index'
import jwt_decode from 'jwt-decode'
import AccountSettings from '../components/account-settings.vue'
import axios from 'axios'



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
            ]
        }
    },
    props: ['computedAuth'],
    computed: {
        fullName: function (event) {
            return this.userAuth.user.first_name + ' ' + this.userAuth.user.last_name;
        }
    },

    methods: {
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
      updateProfile: function (e) {
          var formData = new FormData();
          var imageElement = document.getElementById('image');
          var self = this;
          var username = this.username || this.computedAuth.username;
          var body_fat = this.bf || this.computedAuth.body_fat;
          var weight = this.wt || this.computedAuth.weight;

          formData.append('username', username);
          formData.append('gender', this.genderSelect);
          formData.append('weight', weight);
          formData.append('body_fat', body_fat);
          formData.append('about', this.about);


          if (imageElement.files.length !== 0){
              formData.append('avatar', imageElement.files[0] );
          }

          axios.put(baseURLLocal + 'v1/users/'+this.userAuth.user.username +'/', formData)
              .then(function (response) {
                  self.snackbarMessage = "Successfully updated your profile";
                  self.context = 'success';
                  self.snackbar = true;

                  self.$store.commit('storeUserData', response.data)
                  console.log("response.data", response.data)

              }).catch(function (error) {
                  if (error.response) {
                  // The request was made and the server responded with a status code
                  // that falls out of the range of 2xx

                      self.snackbarMessage = "There was an error updating your profile: \n"+ 'Status' +'\n'+ error.response.status;
                      self.context = 'error';
                      self.snackbar = true;


                      console.log(error.response.data);
                      console.log(error.response.status);
                      console.log(error.response.headers);
                } else if (error.request) {
                  // The request was made but no response was received
                  // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                  // http.ClientRequest in node.js

                      self.snackbarMessage = "There was an error generating a response from the server: \n"+error.request;
                      self.context = 'error';
                      self.snackbar = true;
                      console.log(error.request);
                } else {
                  // Something happened in setting up the request that triggered an Error

                      self.snackbarMessage = "There was an error in the request: "+error.message;
                      self.context = 'error';
                      self.snackbar = true;
                      console.log('Error', error.message);
                }

                console.log(error.config);
          });
      },
      onFileChange ($event) {
        const files = $event.target.files || $event.dataTransfer.files
        const form = this.getFormData(files);
        console.log(form);
        if (files) {
          if (files.length > 0) {
            this.filename = [...files].map(file => file.name).join(', ')
          } else {
            this.filename = null
          }
        } else {
          this.filename = $event.target.value.split('\\').pop()
        }
        this.$emit('input', this.filename);
        this.$emit('formData', form);
      }

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
</style>