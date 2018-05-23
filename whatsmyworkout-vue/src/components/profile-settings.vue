<template >

                    <v-layout row wrap>

                                        <v-flex xs12 md11 offset-md1 >
                                            <h6 class="headline text-xs-center  grey--text text--lighten-1 text-md-left">Profile Settings</h6>
                                        </v-flex>

                        <v-flex md4 offset-md1 xs12>
                            <v-flex xs12 md8 text-xs-center class="elevation-5 mt-3">
                                <v-avatar size="300" ><img :src="getProfileAvatar">



                                </v-avatar>
                                <v-btn block class="blue-grey white--text text-xs-center" @click.native="onFocus">
                                        Change
                                        <v-icon right dark>cloud_upload</v-icon>
                                        <input  id="image" type="file" ref="fileInput" accept="image/*" @change="onFileChange">
                                        <span v-model="filename"></span>
                                </v-btn>
                                    <v-btn

                                          block
                                          v-if="avatarChange"
                                           @click="revertAvatarSelection"

                                           color="orange"
                                           class="white--text">
                                        <v-icon left>undo</v-icon>
                                        Revert
                                    </v-btn>
                                </v-flex>

                        </v-flex>
                        <v-flex xs12 md5>

                            <v-card color="grey lighten-4" class="mb-4 mt-4">
                                <v-card-text>

                                <v-flex xs12 d-flex>
                                        <v-flex xs4 text-xs-center style="border-right: 1px solid lightslategrey">
                                            <v-icon>person</v-icon>
                                            <h6 class="primary--text text--darken-1" >{{ fullName }}</h6>
                                        </v-flex>
                                        <v-flex xs4 text-xs-center style="border-right: 1px solid lightslategrey">
                                            <p class="grey--text text--darken-1 mb-1 caption"><em>Username</em></p>
                                            <h6 class="primary--text text--darken-3">{{ userAuth.user.username }}</h6>
                                        </v-flex>
                                    <v-flex xs4 text-xs-center >
                                            <p class="grey--text text--darken-1 mb-1 caption"><em>Member Since</em></p>
                                            <h6 class="primary--text text--darken-3">{{ userAuth.user.date_joined | moment }}</h6>
                                        </v-flex>
                                    </v-flex>

                                </v-card-text>

                            </v-card>

                            <div>
                                <!--<v-toolbar dark class="primary">

                                    <v-btn icon @click.native="closeDialog" dark>
                                        <v-icon>close</v-icon>
                                    </v-btn>
                                    <v-toolbar-title>{{ userAuth.user.username }}'s Profile</v-toolbar-title>
                                    <v-spacer></v-spacer>
                                    <v-toolbar-items>
                                        <v-btn dark flat @click.native="updateProfile">Save</v-btn>
                                    </v-toolbar-items>
                                </v-toolbar>-->
                                <v-form ref="profileForm" v-model="valid" id="profile-form" enctype="multipart/form-data" method="post" @submit.prevent="updateProfile">

                                    <v-layout row wrap class="ml-1" justify-center align-center>
                                        <!--<v-flex xs12 md6 text-md-left>
                                            <v-text-field
                                                v-model="username"
                                                label="Username"
                                                box
                                                light
                                                color="primary darken-3"
                                                hint="Unique & Alphanumeric. For example, JSmith1234"
                                                ></v-text-field>
                                        </v-flex>
                                        <v-flex class="hide-sm-and-down" md6></v-flex>-->

                                        <v-flex xs12 text-xs-left class="mb-0 pb-0">
                                            <h6 class="caption grey--text text--darken-3 mb-0 pb-0">Body Metrics</h6>
                                        </v-flex>
                                        <v-flex xs5 md2>
                                            <v-text-field
                                                v-model="feet"
                                                label="Feet"
                                                :value="heightInFeet"
                                                suffix="ft."
                                                type="number"
                                                :rules="[rules.required, rules.validHeightInFeet]"
                                                box
                                                light
                                                color="primary darken-3"
                                                ></v-text-field>
                                        </v-flex>
                                        <v-flex xs5 offset-xs2 md2 offset-md1>
                                            <v-text-field
                                                v-model="inches"
                                                :value="remainingHeightInInches"
                                                label="Inches"
                                                suffix="in."
                                                type="number"
                                                :rules="[rules.required, rules.validHeightInInches]"
                                                box
                                                light
                                                color="primary darken-3"
                                                ></v-text-field>
                                        </v-flex>
                                        <v-flex xs5 md2 offset-md2>
                                            <v-text-field
                                                v-model="bodyFat"
                                                label="Body Fat"
                                                suffix="%"
                                                v-mask="['##.#', '#.#']"
                                                return-masked-value
                                                box
                                                light
                                                color="primary darken-3"

                                                ></v-text-field>
                                        </v-flex>
                                        <v-flex xs5 offset-xs2 md2 offset-md1>
                                            <v-text-field
                                                v-model="weight"
                                                label="Weight"
                                                suffix="lbs."
                                                v-mask="['###.#', '##.#']"
                                                return-masked-value
                                                :rules="[rules.required]"
                                                box
                                                light
                                                color="primary darken-3"
                                                ></v-text-field>
                                        </v-flex>
                                        <v-flex xs5 md5>
                                            <v-select
                                                v-model="gender"
                                                label="Gender"
                                                :items="genderOpts"
                                                solo
                                                light
                                                color="primary darken-3"
                                                ></v-select>
                                        </v-flex>
                                        <v-flex xs5 offset-xs2 md5 offset-md2>
                                            <v-text-field
                                                disabled
                                                v-model="bmi"
                                                label="BMI"
                                                box
                                                light
                                                hint="BMI is automatically calculated based on profile data."
                                                persistent-hint
                                                color="primary darken-3"
                                                ></v-text-field>
                                        </v-flex>
                                        <v-flex xs12>
                                            <v-text-field
                                                    v-model="about"
                                                    multi-line
                                                    hint="Describe your goals, hobbies etc. "
                                                    light
                                                    ref="about"
                                                    color="primary darken-3"
                                                    counter="160"
                                                    :rules="[() => about.length <= 160 || 'Must be less than 160 characters.']"
                                                >
                                                <div slot="label">
                                                    About
                                                </div>
                                            </v-text-field>
                                        </v-flex>
                                    </v-layout>


                                </v-form>
                            </div>

                            <v-snackbar
                            :top="y === 'top'"
                            v-model="snackbar"
                            :color="context">
                                {{ snackbarMessage }}
                                <v-btn flat class="red--text" @click.native="snackbar = false">Close</v-btn>
                            </v-snackbar>
                        </v-flex>
                        <v-flex xs12 md10 offset-md1 text-xs-right>
                            <v-divider></v-divider>
                            <v-btn
                                    :disabled="disabledSave"
                               @click.prevent.stop="updateProfile()"
                               color="accent">
                                Save Changes
                               <v-icon right>save</v-icon>
                            </v-btn>
                        </v-flex>
                    </v-layout>

</template>

<script>
    import {mask} from 'vue-the-mask'
    import PictureInput from 'vue-picture-input'
    import axios from 'axios'
    import { baseURLLocal } from '../auth/auth-utils'
    import moment from 'moment'


    export default {
        name: 'profile-settings',
        props: ['computedAuth'],
        directives: { mask },

        data () {
            return {



                valid: false,

                loading: false,

                snackbarMessage: 'Status will appear here',
                context: '',
                y: 'top',
                snackbar: false,

                disabledSave: false,


                filename: '',
                username: this.$store.state.userAuth.user.username,
                gender: this.$store.state.userAuth.user.gender,
                about: this.$store.state.userAuth.user.about,

                genderOpts: [ 'Female', 'Male', 'Other'],

                currentBodyStats: null,

                feet: '',
                inches: '',
                heightInInches: '',

                bodyFat: '',
                weight: '',
                bmi: '',


                rules: {

                    required: (val) => !!val || 'Cannot be blank.',
                    validHeightInFeet: (val) => (val > 1 && val < 8) || 'Enter a valid number between 2-7',
                    validHeightInInches: (val) => (val >= 0 && val <= 11) || 'Enter a valid number between 0-11',
                },
                formHasErrors: false,


                wt: this.computedAuth.weight,
                bf: this.computedAuth.body_fat,
                genderSelect: null,
                bodyFatEdit: false,
                weightEdit: false,
                dialog: false,
                userAuth: this.$store.state.userAuth,


                newAvatar: this.$store.state.userAuth.user.avatar,
                avatarChange: false,


            }
        },
        filters: {

            moment (date) {
                return moment(date).format("MMM Do YY");
            },

            heightDisplay: function (hInches) {

                return Math.floor(hInches / 12).toString() + '\'' + ' '+ (hInches%12).toString()+'\'\'';
            }


        },

        watch: {
            valid() {
                this.disabledSave = !this.valid;
            }
        },

        computed: {

            heightInFeet () {
                return this.feet = Math.floor(this.heightInInches / 12).toString();
            },

            remainingHeightInInches () {

                return this.inches = (this.heightInInches%12).toString();
            },

            fullName () {

                return this.userAuth.user.first_name + ' ' + this.userAuth.user.last_name;
            },

            getProfileAvatar: {
                get: function () {
                    return this.newAvatar;
                },
                set: function (newImage) {
                    this.newAvatar = newImage;
                }
            },
            getActivatedSettings: {
                get: function () {
                    return this.$store.state.accountSettingsDialog;
                },

            }
        },
        methods: {

            saveBodyStats (payload) {


                      console.log('saveBodyStats', payload);
                      console.log('currentBodyStats', this.currentBodyStats);

                  if (this.currentBodyStats.height === payload.height &&
                          this.currentBodyStats.weight === payload.weight &&
                          this.currentBodyStats.body_fat === payload.body_fat) {

                        console.log('no changes - body stats');
                      return;
                  }

                  axios.post(baseURLLocal+ 'v1/body-stats/', payload).then(response => {

                      console.log(response);
                      this.heightInInches = response.data.height;
                      this.bmi = response.data.bmi;
                      this.currentBodyStats = response.data

                    }).catch(err => {


                        console.log(err);

                    })
            },

            revertAvatarSelection () {

                this.getProfileAvatar = this.userAuth.user.avatar;
                this.avatarChange = false;
            },
            closeDialog() {
                this.$store.commit('setAccountSettingsDialog', false);
                //this.getActivatedSettings = false;

            },

            saveProfile: function (e) {
                var formData = new FormData();
                var imageElement = document.getElementById('image');
                var self = this;


                formData.append('username', this.username);
                formData.append('gender', this.gender);
                formData.append('about', this.about);


                if (imageElement.files.length !== 0) {
                    formData.append('avatar', imageElement.files[0]);
                }

                this.disabledSave = true;

                axios.put(baseURLLocal + 'v1/users/' + this.userAuth.user.username + '/', formData)
                    .then(function (response) {
                        self.disabledSave = false;
                        self.snackbarMessage = "Successfully updated your profile";
                        self.context = 'success';
                        self.snackbar = true;

                        self.$store.commit('storeUserData', response.data)
                        self.avatarChange = false;
                        console.log("response.data", response.data)

                    }).catch(function (error) {
                        self.disabledSave = false;
                    if (error.response) {
                        // The request was made and the server responded with a status code
                        // that falls out of the range of 2xx

                        self.snackbarMessage = "There was an error updating your profile: \n" + 'Status' + '\n' + error.response.status;
                        self.context = 'error';
                        self.snackbar = true;


                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);
                    } else if (error.request) {
                        // The request was made but no response was received
                        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                        // http.ClientRequest in node.js

                        self.snackbarMessage = "There was an error generating a response from the server: \n" + error.request;
                        self.context = 'error';
                        self.snackbar = true;
                        console.log(error.request);
                    } else {
                        // Something happened in setting up the request that triggered an Error

                        self.snackbarMessage = "There was an error in the request: " + error.message;
                        self.context = 'error';
                        self.snackbar = true;
                        console.log('Error', error.message);
                    }

                    console.log(error.config);
                });
            },

            updateProfile() {
                this.disabledSave = true;


                let height = ((parseInt(this.feet) * 12) + parseInt(this.inches));

                let payload = {
                      height: height,
                      weight: this.weight,
                      body_fat: this.bodyFat,
                      bmi: null,
                  };

                payload.profile = this.userAuth.user.profile_id;
                console.log("payload - body stats", payload);


                axios.all([this.saveBodyStats(payload), this.saveProfile()]).then(axios.spread(function (acct, perms) {
                        this.disabledSave = false;
                        this.snackbarMessage = "Data updated successfully.";
                        this.context = 'success';
                        this.snackbar = true;




                })).catch(error => {
                        this.snackbarMessage = "There was an error updating your profile: \n" + 'Status' + '\n' + error.response.status;
                        this.context = 'error';
                        this.snackbar = true;


                        console.log(error.response.data);
                        console.log(error.response.status);
                        console.log(error.response.headers);
                        console.log(error)

                })
            },

            onFocus() {
                this.$refs.fileInput.click();
            },
            onChange() {

            },
            onFileChange($event) {
                const files = $event.target.files || $event.dataTransfer.files;
                console.log(files);



                if (files) {

                     this.getProfileAvatar = URL.createObjectURL(files[0]);
                     this.avatarChange = true;
                }



            },
        },
        mounted() {
            this.$store.commit('setAccountSettingsDialog', false);

            this.loading = true;

            axios.get(baseURLLocal+'v1/body-stats/').then(response => {
                this.loading = false;
                this.currentBodyStats = response.data.results[0]; //get most recent stats
                this.currentBodyStats.created = moment(response.data.results[0].created).format("MMM Do YY, h:m a");

                this.heightInInches = response.data.results[0].height;
                this.bodyFat = response.data.results[0].body_fat;
                this.weight = response.data.results[0].weight;
                this.bmi = response.data.results[0].bmi;
            }).catch(err =>  {
                this.loading = false;
                console.log(err)
            })
        },

      components: {
            PictureInput
      }
    }
</script>