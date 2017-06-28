/**
 * Created by LeviJamesH on 6/28/2017.
 */

import Vue from 'vue'
import Router from 'vue-router'
import App from '../App.vue'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: App
    }
  ]
})