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
import ManageWorkouts from '../components/manage-workouts.vue'
import ArchiveWorkouts from '../components/archive-workouts.vue'
import WorkoutDetail from '../components/workout-detail.vue'
import WorkoutStats from '../components/workout-stats.vue'
import ProfileStatDetail from '../components/profile-stat-tracking-detail.vue'
import PublicProfile from '../components/user-public-profile.vue'
import ProfileSettings from '../components/profile-settings.vue'
import AccountSettingsDetail from '../components/account-settings-detail.vue'
import PasswordResetConfirm from '../components/password-reset-confirm.vue'
import { getJWTHeader } from '../auth/auth-utils'
import axios from 'axios'
import requireAuth from './guards.js'


Vue.use(Router);

(function() {
     let token = getJWTHeader();
     if (token) {
         axios.defaults.headers.common['Authorization'] = token;
     } else {
       console.log("Delete header");
         delete axios.defaults.headers.common['Authorization'];
         /*if setting null does not remove `Authorization` header then try
           delete axios.defaults.headers.common['Authorization'];
         */
     }
})();




export default new Router({
  base: '/',
  mode: 'history',
  routes: [
      {
        path: '/account/settings/',
        component: AccountSettingsDetail,
          beforeEnter: requireAuth
      },

      {
        path: '/profile-settings/',
        component: ProfileSettings,
          beforeEnter: requireAuth
      },

      {
        path: '/profile/:username',
        component: PublicProfile,
          beforeEnter: requireAuth
      },
      {
        path: '/user/profile-stats/detail/',
        name: 'profile-stat-tracking-detail',
        component: ProfileStatDetail,
          beforeEnter: requireAuth

      },
    {
      path: '/user/dashboard/',
      name: 'user-dashboard',
      component: userDashboard,
      beforeEnter: requireAuth
    },
      {
        path: '/workout/stats/',
        name: 'workout-stats',
        component: WorkoutStats,
          beforeEnter: requireAuth
      },
    {
      path: '/dashboard/',
      name: 'dashboard',
      component: Dashboard,
        beforeEnter: requireAuth
    },
    {
      path: '/manage/workouts/',
      name: 'manage-workouts',
      component: ManageWorkouts,
        beforeEnter: requireAuth

    },
    {
      path: '/create-workout/',
      name: 'create-workout',
      component: CreateWorkout,
      props: { createWorkout: true },
        beforeEnter: requireAuth
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
        beforeEnter: requireAuth

    },
    {
      path: '/archived-workouts/',
      name: 'archive-workouts',
      component: ArchiveWorkouts,
        beforeEnter: requireAuth

    },
    {
      path: '/workout/edit/',
      name: 'workout-detail',
      component: WorkoutDetail,
      props: true,
      beforeEnter: requireAuth

    },
      {
        path: '/password-reset-confirm/',
        name: 'password-reset-confirm',
        component: PasswordResetConfirm
      }
  ],

})