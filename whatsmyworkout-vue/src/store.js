import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { getJWTHeader, authenticationStatus, getUsernameFromToken } from "./auth/auth-utils";
import router from './router/index';
import jwt_decode from 'jwt-decode'

Vue.use(Vuex);

export let baseURLLocal = "http://127.0.0.1:8000/";


//TODO break down into vuex modules

export default new Vuex.Store({
    state: {
        userAuth: {
            isAuthenticated: authenticationStatus(),
            user: {

            }
        },
        data: {}
    },
    mutations: {
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
        newUser ({commit}, userData) {

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
        }
    },
    getters: {

    }
});