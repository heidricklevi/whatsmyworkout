'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _vue = require('vue');

var _vue2 = _interopRequireDefault(_vue);

var _vuex = require('vuex');

var _vuex2 = _interopRequireDefault(_vuex);

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

var _authUtils = require('./auth/auth-utils');

var _index = require('./router/index');

var _index2 = _interopRequireDefault(_index);

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _jwtDecode = require('jwt-decode');

var _jwtDecode2 = _interopRequireDefault(_jwtDecode);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_vue2.default.use(_vuex2.default);

//TODO break down into vuex modules

exports.default = new _vuex2.default.Store({
    state: {
        userAuth: {
            isAuthenticated: (0, _authUtils.authenticationStatus)(),
            user: {}
        },
        data: {},
        muscleHistoryGraphLabels: null,
        muscleHistoryGraphData: null,
        recentTargetedMuscleExercises: null,
        targetMuscle: '',
        dialog: false,
        loading: false,
        accountSettingsDialog: false,

        accountSettings: {
            receiveWorkoutNotifications: null,
            receiveWorkoutsFromFriends: null

        },

        userDashboard: {
            friends: [],
            receivedFriendRequests: null,
            sentFriendRequests: null,
            recentWorkouts: [],
            friendsCount: null

        },
        friendProfile: {
            addNewExerciseToggle: false,
            toCopyWorkout: {},
            toCopyExercises: []
        }
    },
    mutations: {
        setRecentWorkouts: function setRecentWorkouts(state, payload) {
            console.log(payload);

            state.userDashboard.recentWorkouts = payload;
        },
        setReceiveWorkoutsFromFriends: function setReceiveWorkoutsFromFriends(state, payload) {
            state.accountSettings.receiveWorkoutsFromFriends = payload;
        },
        setReceiveWorkoutNotifications: function setReceiveWorkoutNotifications(state, payload) {

            state.accountSettings.receiveWorkoutNotifications = payload;
        },
        setNewExerciseToggle: function setNewExerciseToggle(state, payload) {
            state.friendProfile.addNewExerciseToggle = payload;
        },
        setAccountSettingsDialog: function setAccountSettingsDialog(state, payload) {
            state.accountSettingsDialog = payload;
        },
        setLoading: function setLoading(state, payload) {
            state.loading = payload;
        },
        setDialog: function setDialog(state, payload) {
            state.dialog = payload;
        },
        setToCopyExercises: function setToCopyExercises(state, payload) {
            state.friendProfile.toCopyExercises = payload;
        },
        setToCopyWorkout: function setToCopyWorkout(state, payload) {
            state.friendProfile.toCopyWorkout = payload;
        },
        setSentFriendRequests: function setSentFriendRequests(state, payload) {
            state.userDashboard.sentFriendRequests = payload;
        },
        setReceivedFriendRequests: function setReceivedFriendRequests(state, payload) {
            state.userDashboard.receivedFriendRequests = payload;
        },
        setFriendCount: function setFriendCount(state, payload) {
            state.userDashboard.friendsCount = payload;
        },
        setFriends: function setFriends(state, payload) {
            state.userDashboard.friends = payload;
        },
        setTargetedMuscleData: function setTargetedMuscleData(state, payload) {

            if (payload) {
                state.recentTargetedMuscleExercises = payload;
                state.recentTargetedMuscleExercises[0].created = (0, _moment2.default)(payload[0].created).format("MMM Do YY, h:m a");
                state.targetMuscle = payload[0].target_muscle;
            } else {
                state.recentTargetedMuscleExercises = null;
            }
        },
        setGraphData: function setGraphData(state, payload) {

            if (payload) {
                state.muscleHistoryGraphData = payload.reverse();
                console.log("Graph Data Payload", payload);
            } else {
                state.muscleHistoryGraphData = null;
            }
        },
        setGraphLabels: function setGraphLabels(state, payload) {
            if (payload) {
                state.muscleHistoryGraphLabels = payload.reverse();
                console.log("Graph Label Payload", payload);
            } else {
                state.muscleHistoryGraphLabels = null;
            }
        },
        setData: function setData(state, payload) {
            state.data = payload;
        },
        storeUserData: function storeUserData(state, payload) {
            state.userAuth.user = payload;
        },
        setUserAuth: function setUserAuth(state, authPayload) {
            //send jwt on every request
            _axios2.default.defaults.headers.common['Authorization'] = (0, _authUtils.getJWTHeader)();
            state.userAuth.isAuthenticated = true;
            state.userAuth.user = authPayload;
        },
        removeAuth: function removeAuth(state) {
            state.userAuth.isAuthenticated = false;
            state.userAuth.user = null;
            localStorage.removeItem('JWT');

            _index2.default.push({ path: '/' });
        }
    },
    actions: {
        login: function login(_ref, credentials) {
            var commit = _ref.commit;

            _axios2.default.post(_authUtils.baseURLLocal + 'v1/login/', credentials).then(function (response) {
                var JWT = response.data.token;
                localStorage.setItem("JWT", JWT);
                console.log('logging in via store');

                commit('setUserAuth', response.data.user);
            }).catch(function (errors) {
                console.log(errors);
            });
        },
        newUser: function newUser(_ref2, userDataPayload) {
            var commit = _ref2.commit;

            _axios2.default.post(_authUtils.baseURLLocal + 'v1/user/create/', userDataPayload).then(function (response) {
                console.log('success');
                console.log(response);
            }).catch(function (err) {
                console.log(err);
            });
        },
        fetchUserProfile: function fetchUserProfile(_ref3) {
            var commit = _ref3.commit;


            var username = (0, _authUtils.getUsernameFromToken)();
            if (!username || !this.state.userAuth.isAuthenticated) return;

            _axios2.default.defaults.headers.common['Authorization'] = (0, _authUtils.getJWTHeader)();

            _axios2.default.get(_authUtils.baseURLLocal + "v1/users/" + username + '/').then(function (response) {
                console.log("Fetching from store", response);
                commit('storeUserData', response.data);
            }).catch(function (err) {
                console.log(err);
            });
        },
        logout: function logout(_ref4) {
            var commit = _ref4.commit;

            commit('removeAuth');
        },
        fetchGraphData: function fetchGraphData(_ref5, queryVal) {
            var commit = _ref5.commit;

            var temp = [];
            var tempData = [];

            _axios2.default.get(_authUtils.baseURLLocal + 'v1/max-lifts/?target_muscle=' + queryVal.target_muscle + '&max_type=' + '3' + '&exercise_name=' + queryVal.exercise_name).then(function (response) {

                if (response.data.results.length === 0) {

                    console.log("no results");
                    commit("setTargetedMuscleData", null);
                    commit("setGraphData", null);
                    commit("setGraphLabels", null);
                    return;
                }

                for (var i = 0; i < response.data.results.length; i++) {
                    temp[i] = (0, _moment2.default)(response.data.results[i].created).format("MMM Do YY");
                    tempData[i] = response.data.results[i].weight;
                }

                commit("setTargetedMuscleData", response.data.results);
                commit("setGraphData", tempData);
                commit("setGraphLabels", temp);
            }).catch(function (err) {
                console.log("fetchGraphData store.js errors: ", err);
            });
        }
    },
    getters: {}
});
//# sourceMappingURL=store.js.map