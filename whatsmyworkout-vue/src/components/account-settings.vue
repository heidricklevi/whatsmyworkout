<template >
    <v-dialog
            :computed-auth="computedAuth"
            v-model="getActivatedSettings"
            fullscreen
            transition="dialog-bottom-transition"
            :overlay=false
            >
                    <v-layout row style="height: 100vh">
                        <v-flex xs12 >
                            <v-card style="height: 100%">

                                <v-toolbar dark class="primary">

                                    <v-btn icon @click.native="closeDialog" dark>
                                        <v-icon>close</v-icon>
                                    </v-btn>
                                    <v-toolbar-title>{{ userAuth.user.username }}'s Settings</v-toolbar-title>
                                    <v-spacer></v-spacer>
                                    <v-btn @click.native="saveSettings" flat >
                                        Save
                                    </v-btn>
                                </v-toolbar>
                                <v-flex ml-4>
                                <v-list three-line subheader>
                                  <v-subheader>User Controls</v-subheader>
                                  <v-list-tile to="/profile-settings/" v-ripple>
                                    <v-list-tile-content >
                                      <v-list-tile-title>Profile Settings</v-list-tile-title>
                                      <v-list-tile-sub-title>Change profile picture, your 'about' section and more. </v-list-tile-sub-title>
                                    </v-list-tile-content>
                                  </v-list-tile>
                                  <v-list-tile to="/account/settings/">
                                    <v-list-tile-content>
                                      <v-list-tile-title>Account Settings</v-list-tile-title>
                                      <v-list-tile-sub-title>Change password, email address, and other account related settings</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                  </v-list-tile>
                                </v-list>
                                <v-divider></v-divider>
                                <v-list three-line subheader>
                                  <v-subheader>Notifications</v-subheader>
                                  <v-list-tile href="javascript:;">
                                    <v-list-tile-action>
                                      <v-checkbox
                                        v-model="getReceiveWorkoutNotifications"
                                      ></v-checkbox>
                                    </v-list-tile-action>
                                    <v-list-tile-content @click="getReceiveWorkoutNotifications = !getReceiveWorkoutNotifications">
                                      <v-list-tile-title>Scheduled Workouts</v-list-tile-title>
                                      <v-list-tile-sub-title>Send me email notifications outlining my workout on the day it is scheduled.</v-list-tile-sub-title>
                                    </v-list-tile-content>
                                  </v-list-tile>
                                  <v-list-tile href="javascript:;">
                                    <v-list-tile-action>
                                      <v-checkbox v-model="getReceiveWorkoutsFromFriends"></v-checkbox>
                                    </v-list-tile-action>
                                    <v-list-tile-content @click="getReceiveWorkoutsFromFriends = !getReceiveWorkoutsFromFriends">
                                      <v-list-tile-title>Workouts From Friends</v-list-tile-title>
                                      <v-list-tile-sub-title>Allow Friends to share workouts with you.
                                          The workout is shared through the app
                                          and comes to you as an email. Your email address is never shared.
                                      </v-list-tile-sub-title>
                                    </v-list-tile-content>
                                  </v-list-tile>
                                  <!--<<v-list-tile href="javascript:;">
                                    <v-list-tile-action>
                                      <v-checkbox v-model="widgets"></v-checkbox>
                                    </v-list-tile-action>
                                    v-list-tile-content @click="widgets = !widgets">
                                      <v-list-tile-title>Friends Scheduled Workouts</v-list-tile-title>
                                      <v-list-tile-sub-title>Automatically receive scheduled </v-list-tile-sub-title>
                                    </v-list-tile-content>
                                  </v-list-tile>-->
                                </v-list>
                                    </v-flex>
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
</template>

<script>
    import PictureInput from 'vue-picture-input'
    import axios from 'axios'
    import { baseURLLocal } from '../auth/auth-utils'


    export default {
        name: 'account-settings',
        props: ['computedAuth'],
        data () {
            return {
                snackbarMessage: 'Status will appear here',
                context: '',
                y: 'top',
                snackbar: false,

                userAuth: this.$store.state.userAuth,
                settingsId: null,


            }
        },
        computed: {
            getActivatedSettings: {
                get: function () {
                    return this.$store.state.accountSettingsDialog;
                },
                
            },

            getReceiveWorkoutsFromFriends: {
                get: function () {
                        return this.$store.state.accountSettings.receiveWorkoutsFromFriends;
                },
                set: function (val) {
                    this.$store.commit('setReceiveWorkoutsFromFriends', val);
                }

            },

            getReceiveWorkoutNotifications: {
                get: function () {
                        return this.$store.state.accountSettings.receiveWorkoutNotifications;
                },
                set: function (val) {
                    this.$store.commit('setReceiveWorkoutNotifications', val)
                }

            },
        },
        methods: {
            saveSettings () {

                let payload = {
                    receive_workout_notifications: this.getReceiveWorkoutNotifications,
                    receive_workouts_from_friends: this.getReceiveWorkoutsFromFriends,
                    user: this.userAuth.user.id,
                    friends_can_subscribe: false,
                };

                axios.put(baseURLLocal+ 'v1/account-settings/'+this.settingsId+'/', payload).then(response => {
                    this.snackbarMessage = "Saved";
                    this.snackbar = true;
                }).catch(err => {

                })


            },
            closeDialog() {
                this.$store.commit('setAccountSettingsDialog', false);
                //this.getActivatedSettings = false;

            },
        },


        mounted() {

            axios.get(baseURLLocal+ 'v1/account-settings/').then(response => {
                this.$store.commit('setReceiveWorkoutNotifications', response.data.results[0].receive_workout_notifications);
                this.$store.commit('setReceiveWorkoutsFromFriends', response.data.results[0].receive_workouts_from_friends);
                console.log(response);
                this.settingsId = response.data.results[0].id;
            }).catch(err => {
                console.log(err)
                this.snackbarMessage = "Error Fetching Account Settings";
                this.snackbar = true;

            })


        },
    }
</script>