import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { getJWTHeader, authenticationStatus, getUsernameFromToken, baseURLLocal } from "./auth/auth-utils";
import router from './router/index'
import moment from 'moment'
import jwt_decode from 'jwt-decode'

Vue.use(Vuex);



//TODO break down into vuex modules

export default new Vuex.Store({
    state: {
        userAuth: {
            isAuthenticated: authenticationStatus(),
            user: {

            }
        },
        data: {},
        muscleHistoryGraphLabels: null,
        muscleHistoryGraphData: null,
        recentTargetedMuscleExercises: null,
        targetMuscle: '',
        dialog: false,
        loading: false,

        userDashboard: {
            friends: [],
            receivedFriendRequests: null,
            sentFriendRequests: null,
        },
        friendProfile: {
            toCopyWorkout: {},
            toCopyExercises: [],
        }
    },
    mutations: {

      setLoading (state, payload) {
        state.loading = payload;
      },
      setDialog (state, payload) {
        state.dialog = payload;
      },

      setToCopyExercises (state, payload) {
        state.friendProfile.toCopyExercises = payload;
      },

      setSentFriendRequests (state, payload) {
        state.userDashboard.sentFriendRequests = payload;
      },

      setReceivedFriendRequests (state, payload) {
        state.userDashboard.receivedFriendRequests = payload;
      },

      setFriends (state, payload) {
        state.userDashboard.friends = payload;
      },
      setTargetedMuscleData (state, payload) {

          if (payload){
              state.recentTargetedMuscleExercises = payload;
              state.recentTargetedMuscleExercises[0].created = moment(payload[0].created).format("MMM Do YY, h:m a");
              state.targetMuscle = payload[0].target_muscle;
            }
          else {
              state.recentTargetedMuscleExercises = null;
          }
      },
      setGraphData (state, payload) {

        if (payload) {
            state.muscleHistoryGraphData = payload.reverse();
            console.log("Graph Data Payload", payload)
          }
        else {
            state.muscleHistoryGraphData = null;
        }
      },

      setGraphLabels (state, payload) {
          if (payload) {
              state.muscleHistoryGraphLabels = payload.reverse();
              console.log("Graph Label Payload", payload);
            }
          else {
            state.muscleHistoryGraphLabels = null;
          }
      },
      setData (state, payload) {
          state.data = payload;
      },
      storeUserData (state, payload) {
          state.userAuth.user = payload;
      },
      setUserAuth (state, authPayload) {
          //send jwt on every request
          axios.defaults.headers.common['Authorization'] = getJWTHeader();
          state.userAuth.isAuthenticated = true;
          state.userAuth.user = authPayload;

      },
      removeAuth (state) {
          state.userAuth.isAuthenticated = false;
          state.userAuth.user = null;
          localStorage.removeItem('JWT');

          router.push({path: '/'});
      }
    },
    actions: {
        login ({commit}, credentials) {
            axios.post(baseURLLocal+'v1/login/', credentials
            ).then(function (response) {
                let JWT = response.data.token;
                localStorage.setItem("JWT", JWT);
                console.log('logging in via store');

                commit('setUserAuth', response.data.user);

            }).catch(function (errors) {
                console.log(errors);
            })


        },
        newUser ({commit}, userDataPayload) {
            axios.post(baseURLLocal+'v1/user/create/', userDataPayload
            ).then(function (response) {
                console.log('success');
                console.log(response);
            }).catch(function (err) {
                console.log(err);
            })
        },

        fetchUserProfile ({commit}) {

            let username = getUsernameFromToken();
            if (!username || !this.state.userAuth.isAuthenticated) return;
            
            axios.defaults.headers.common['Authorization'] = getJWTHeader();

            axios.get(baseURLLocal+"v1/users/" + username +'/')
                .then(function (response) {
                    console.log("Fetching from store", response);
                    commit('storeUserData', response.data);

                }).catch(function (err) {
                    console.log(err)
            });
        },
        logout ({commit}) {
            commit('removeAuth');

        },
        fetchGraphData ({commit}, queryVal) {
            let temp = [];
            let tempData = [];

            axios.get(baseURLLocal+'v1/max-lifts/?target_muscle='+queryVal.target_muscle +'&max_type='+ '3' +'&exercise_name='+queryVal.exercise_name).then(response => {

                if (response.data.results.length === 0) {

                    console.log("no results");
                    commit("setTargetedMuscleData", null);
                    commit("setGraphData", null);
                    commit("setGraphLabels", null);
                    return;
                }

                for (var i = 0; i < response.data.results.length; i++) {
                    temp[i] = moment(response.data.results[i].created).format("MMM Do YY");
                    tempData[i] = response.data.results[i].weight;
                }


                commit("setTargetedMuscleData", response.data.results);
                commit("setGraphData", tempData);
                commit("setGraphLabels", temp);

            }).catch(err =>  {
                console.log("fetchGraphData store.js errors: ", err);
            })
        },

    },
    getters: {

    }
});