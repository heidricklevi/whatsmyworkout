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
import { getJWTHeader } from '../auth/auth-utils'
import axios from 'axios'

Vue.use(Router);

(function() {
     let token = getJWTHeader();
     if (token) {
         axios.defaults.headers.common['Authorization'] = token;
     } else {
         axios.defaults.headers.common['Authorization'] = null;
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
      },

      {
        path: '/profile-settings/',
        component: ProfileSettings,
      },

      {
        path: '/profile/:username',
        component: PublicProfile,
      },
      {
        path: '/user/profile-stats/detail/',
        name: 'profile-stat-tracking-detail',
        component: ProfileStatDetail

      },
    {
      path: '/user/dashboard/',
      name: 'user-dashboard',
      component: userDashboard
    },
      {
        path: '/workout/stats/',
        name: 'workout-stats',
        component: WorkoutStats
      },
    {
      path: '/dashboard/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/manage/workouts/',
      name: 'manage-workouts',
      component: ManageWorkouts

    },
    {
      path: '/create-workout/',
      name: 'create-workout',
      component: CreateWorkout,
      props: { createWorkout: true }
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

    },
    {
      path: '/archived-workouts/',
      name: 'archive-workouts',
      component: ArchiveWorkouts,

    },
    {
      path: '/workout/edit/',
      name: 'workout-detail',
      component: WorkoutDetail,
      props: true,

    }
  ],

})