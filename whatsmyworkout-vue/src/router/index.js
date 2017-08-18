/**
 * Created by LeviJamesH on 6/28/2017.
 */

import Vue from 'vue'
import Router from 'vue-router'
import CreateWorkout from '../components/create-workout.vue'
import Login from '../components/login.vue'
import Dashboard from '../components/dashboard.vue'
import AccountSettings from '../components/account-settings.vue'
import userDashboard from '../components/user-dashboard.vue'

Vue.use(Router);

var JWT = localStorage.getItem('JWT');


export default new Router({
  base: '/',
  mode: 'hash',
  routes: [
    {
      path: '/user/dashboard/',
      name: 'user-dashboard',
      component: userDashboard
    },
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
    },
    {
      path: '/account-settings/',
      name: 'account-settings',
      component: AccountSettings,

    }
  ],

})