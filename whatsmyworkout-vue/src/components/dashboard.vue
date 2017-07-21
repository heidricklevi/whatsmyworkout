<template>
    <v-app id="dashboard">
        <v-navigation-drawer persistent light :mini-variant.sync="mini" v-model="drawer" overflow>
            <v-toolbar flat class="transparent">
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
            </v-toolbar>
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
        <v-toolbar fixed class="indigo darken-4" dark>
            <v-toolbar-side-icon @click.native.stop="drawer = !drawer"></v-toolbar-side-icon>
            <v-toolbar-items>
                <img src="../assets/img/logo.png" style="width: 100px;">
            </v-toolbar-items>
            <v-container fluid>
                <v-spacer></v-spacer>
                <v-layout row>
                    <v-flex offset-xs10 offset-md11 style="text-align: center">
                        <v-btn icon style="margin-bottom: 10%">
                            <v-menu left>
                                <v-icon slot="activator" fa class="fa fa-2x">cogs</v-icon>

                                <v-list>

                                    <v-list-tile>
                                        <v-icon class="grey--text text--darken-4">settings</v-icon>
                                        <v-list-tile-title style="margin: 24px">Account Settings</v-list-tile-title>
                                    </v-list-tile>
                                    <v-list-tile @click.native.stop="dialog = true">
                                        <v-icon class="blue-grey--text text--darken-4">perm_identity</v-icon>
                                        <v-list-tile-title style="margin: 24px">Profile Settings</v-list-tile-title>
                                    </v-list-tile>
                                    <v-divider></v-divider>
                                    <v-list-tile>
                                        <v-icon v-on:click="logout" class="red--text text--darken-2">power_settings_new</v-icon>
                                        <v-list-tile-title v-on:click="logout" style="margin: 24px">Log Off</v-list-tile-title>
                                    </v-list-tile>
                                </v-list>
                            </v-menu>
                        </v-btn>
                    </v-flex>
                </v-layout>
                <v-dialog v-model="dialog" fullscreen transition="dialog-bottom-transition" :overlay=false>
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
                                        <v-btn dark flat @click.native="dialog = false">Save</v-btn>
                                    </v-toolbar-items>
                                </v-toolbar>
                                <v-card-media :src="userAuth.user.avatar" style="height: 250px">
                                    <v-btn :loading="loading3" @click.native="loader = 'loading3'" :disabled="loading3" class="blue-grey white--text" style="position: absolute; bottom: 0; right: 0">

                                        Change
                                        <v-icon right dark>cloud_upload</v-icon>
                                    </v-btn>
                                </v-card-media>
                                <v-list three-line subheader>
                                    <v-subheader>Profile Settings</v-subheader>
                                    <v-list-tile>
                                        <v-flex xs12 sm12 md4 offset-md2>
                                            <v-list-tile-title>Username</v-list-tile-title>
                                        </v-flex>

                                        <v-flex xs12 sm12 md6>
                                            <v-text-field name="username" :label="userAuth.user.username" prepend-icon="perm_identity" single-line></v-text-field>
                                        </v-flex>
                                    </v-list-tile>
                                    <v-list-tile>
                                        <v-flex xs12 sm12 md4 offset-md2>
                                            <v-list-tile-title>Gender</v-list-tile-title>
                                        </v-flex>
                                        <v-flex xs12 sm12 md6>
                                            <v-select v-bind:items="genderOpts" v-model="genderSelect" :label="userAuth.user.gender"></v-select>
                                        </v-flex>
                                    </v-list-tile>
                                    <li>
                                        <v-layout row>
                                            <v-flex xs11 offset-xs1 sm12 md4 offset-md2>
                                                <v-list-tile-title>Body Fat <em>(percentage)</em>
                                                </v-list-tile-title>
                                            </v-flex>
                                            <v-flex xs9 offset-xs1 md4>
                                                <v-slider v-bind:max="75" v-model="bf"></v-slider>
                                            </v-flex>
                                            <v-flex xs2 md1>
                                                <input v-model="bf" type="number" :value="userAuth.user.body_fat" style="width: 100%">
                                            </v-flex>
                                        </v-layout>
                                    </li>
                                </v-list>
                            </v-card>
                        </v-flex>
                    </v-layout>
                </v-dialog>
            </v-container>
        </v-toolbar>
        <main>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </main>
    </v-app>
</template>

<script>

import { userAuth, login, authenticationStatus, logout, getUserAccount, getJWTHeader, setUserAuth } from '../auth/auth'
import router from '../router/index'
import jwt_decode from 'jwt-decode'
import AccountSettings from '../components/account-settings.vue'
import axios from 'axios'

export default {
    name: 'dashboard',
    data () {
        return {
            bf: userAuth.user.body_fat,
            genderSelect: null,
            dialog: false,
            drawer: true,
            mini: false,
            right: null,
            userAuth: userAuth,
            items: [
                { title: 'Dashboard', icon: 'dashboard', link: '/'},
                { title: 'Create Workout', icon: 'create', link: '/create-workout/' },
                { title: 'Manage Workouts', icon: 'schedule', link: '/'},
                { title: 'Share Workouts', icon: 'share', link: '/'},
                { title: 'Archive Workouts', icon: 'archive', link: '/'}
            ],
            genderOpts: [
                { text: 'Male' },
                { text: 'Female' },
            ]
        }
    },
    computed: {
        fullName: function (event) {
            return this.userAuth.user.first_name + ' ' + this.userAuth.user.last_name;
        }
    },
    methods: {
      logout: function (){
          logout();
          window.location.href = '/';
      },

    },
    components: {
        'account-settings': AccountSettings
    },
}

</script>

<style>

    .profile-card {
        margin: 0 25% 0 35%;
        width: 200px;
        height: 200px;
    }

     @media only screen and (max-width: 768px) {

        .profile-card {
            margin: 0 25% 0 25%;
            width: 200px;
            height: 200px;
        }

    }
</style>