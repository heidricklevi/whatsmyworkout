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
        muscleHistoryGraphLabels: [],
        muscleHistoryGraphData: [],
    },
    mutations: {
      setGraphData (state, payload) {
        state.muscleHistoryGraphData = payload;
        console.log("Graph Data Payload", payload)
      },

      setGraphLabels (state, payload) {
          state.muscleHistoryGraphLabels = payload;
          console.log("Graph Label Payload", payload);
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
            axios.get(baseURLLocal+'v1/max-lifts/?target_muscle='+queryVal+'&max_type=3').then(function (response) {
                for (var i = 0; i < response.data.results.length; i++) {
                    temp[i] = moment(response.data.results[i].created).format("MMM Do YY");
                    tempData[i] = response.data.results[i].weight;
                   // tempData[i] += ' lbs.';
                }

                console.log(temp);
                commit("setGraphData", tempData);
                commit("setGraphLabels", temp);
            }).catch(function (err) {
                
            })
        },

    },
    getters: {

    }
});