<template >
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
                              <v-icon>settings</v-icon>
                              <v-list-tile-title style="margin: 24px">Account Settings</v-list-tile-title>
                          </v-list-tile>
                          <v-list-tile>
                              <v-icon>perm_identity</v-icon>
                              <v-list-tile-title style="margin: 24px">Profile Settings</v-list-tile-title>
                          </v-list-tile>
                          <v-list-tile >
                              <v-icon v-on:click="logout">power_settings_new</v-icon>
                              <v-list-tile-title style="margin: 24px">Log Off</v-list-tile-title>
                          </v-list-tile>
                      </v-list>
                  </v-menu>
                </v-btn>
              </v-flex>
          </v-layout>

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
import axios from 'axios'

export default {
    name: 'dashboard',
    data () {
        return {
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
}

</script>