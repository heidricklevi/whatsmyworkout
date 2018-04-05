'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _vue = require('vue');

var _vue2 = _interopRequireDefault(_vue);

var _vueRouter = require('vue-router');

var _vueRouter2 = _interopRequireDefault(_vueRouter);

var _createWorkout = require('../components/create-workout.vue');

var _createWorkout2 = _interopRequireDefault(_createWorkout);

var _login = require('../components/login.vue');

var _login2 = _interopRequireDefault(_login);

var _dashboard = require('../components/dashboard.vue');

var _dashboard2 = _interopRequireDefault(_dashboard);

var _accountSettings = require('../components/account-settings.vue');

var _accountSettings2 = _interopRequireDefault(_accountSettings);

var _userDashboard = require('../components/user-dashboard.vue');

var _userDashboard2 = _interopRequireDefault(_userDashboard);

var _manageWorkouts = require('../components/manage-workouts.vue');

var _manageWorkouts2 = _interopRequireDefault(_manageWorkouts);

var _archiveWorkouts = require('../components/archive-workouts.vue');

var _archiveWorkouts2 = _interopRequireDefault(_archiveWorkouts);

var _workoutDetail = require('../components/workout-detail.vue');

var _workoutDetail2 = _interopRequireDefault(_workoutDetail);

var _workoutStats = require('../components/workout-stats.vue');

var _workoutStats2 = _interopRequireDefault(_workoutStats);

var _profileStatTrackingDetail = require('../components/profile-stat-tracking-detail.vue');

var _profileStatTrackingDetail2 = _interopRequireDefault(_profileStatTrackingDetail);

var _userPublicProfile = require('../components/user-public-profile.vue');

var _userPublicProfile2 = _interopRequireDefault(_userPublicProfile);

var _profileSettings = require('../components/profile-settings.vue');

var _profileSettings2 = _interopRequireDefault(_profileSettings);

var _accountSettingsDetail = require('../components/account-settings-detail.vue');

var _accountSettingsDetail2 = _interopRequireDefault(_accountSettingsDetail);

var _authUtils = require('../auth/auth-utils');

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_vue2.default.use(_vueRouter2.default); /**
                                         * Created by LeviJamesH on 6/28/2017.
                                         */

(function () {
  var token = (0, _authUtils.getJWTHeader)();
  if (token) {
    _axios2.default.defaults.headers.common['Authorization'] = token;
  } else {
    _axios2.default.defaults.headers.common['Authorization'] = null;
    /*if setting null does not remove `Authorization` header then try
      delete axios.defaults.headers.common['Authorization'];
    */
  }
})();

exports.default = new _vueRouter2.default({
  base: '/',
  mode: 'history',
  routes: [{
    path: '/account/settings/',
    component: _accountSettingsDetail2.default
  }, {
    path: '/profile-settings/',
    component: _profileSettings2.default
  }, {
    path: '/profile/:username',
    component: _userPublicProfile2.default
  }, {
    path: '/user/profile-stats/detail/',
    name: 'profile-stat-tracking-detail',
    component: _profileStatTrackingDetail2.default

  }, {
    path: '/user/dashboard/',
    name: 'user-dashboard',
    component: _userDashboard2.default
  }, {
    path: '/workout/stats/',
    name: 'workout-stats',
    component: _workoutStats2.default
  }, {
    path: '/dashboard/',
    name: 'dashboard',
    component: _dashboard2.default
  }, {
    path: '/manage/workouts/',
    name: 'manage-workouts',
    component: _manageWorkouts2.default

  }, {
    path: '/create-workout/',
    name: 'create-workout',
    component: _createWorkout2.default,
    props: { createWorkout: true }
  }, {
    path: '/login/',
    name: 'login',
    component: _login2.default
  }, {
    path: '/account-settings/',
    name: 'account-settings',
    component: _accountSettings2.default

  }, {
    path: '/archived-workouts/',
    name: 'archive-workouts',
    component: _archiveWorkouts2.default

  }, {
    path: '/workout/edit/',
    name: 'workout-detail',
    component: _workoutDetail2.default,
    props: true

  }]

});
//# sourceMappingURL=index.js.map