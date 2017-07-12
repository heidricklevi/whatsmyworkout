/**
 * Created by LeviJamesH on 6/28/2017.
 */

import Vue from 'vue'
import Router from 'vue-router'
import App from '../App.vue'
import CreateWorkout from '../components/create-workout.vue'
import { userAuth, } from '../auth/auth'

Vue.use(Router);
var JWT = localStorage.getItem('JWT');


export default new Router({
  routes: [
    {
      path: '/dashboard/',
      name: 'Hello',
      component: App
    },
    {
      path: '/create-workout/',
      name: 'create-workout',
      component: CreateWorkout
    }
  ]
})