/**
 * Created by LeviJamesH on 6/28/2017.
 */

import Vue from 'vue'
import Router from 'vue-router'
import App from '../App.vue'
import CreateWorkout from '../components/create-workout.vue'
import Login from '../components/login.vue'
import Dashboard from '../components/dashboard.vue'
import { userAuth, } from '../auth/auth'
import Vuetify from 'vuetify'
Vue.use(Router);
Vue.use(Vuetify);
var JWT = localStorage.getItem('JWT');


export default new Router({
  base: '/',
  mode: 'hash',
  routes: [
    {
      path: '/dashboard/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/create-workout/',
      name: 'create-workout',
      component: CreateWorkout
    },
    {
      path: '/login/',
      name: 'login',
      component: Login
    }
  ],

})