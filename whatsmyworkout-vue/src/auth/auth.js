/**
 * Created by LeviJamesH on 7/8/2017.
 */

import router from '../router/index'
import axios from 'axios'
import jwt_decoded from 'jwt-decode'

let baseURL = "http://127.0.0.1:8000/";

export var userAuth = {
    isAuthenticated: authenticationStatus(),
    user: {
        firstName: '',
        lastName: '',
        username: '',
        id: 0,
        email: '',
        avatar: '',

    }
};

export function login(username, pass) {

    let credentials = {
        username: username,
        password: pass,
    };

    axios.post(baseURL + 'v1/login/', credentials
    ).then(function (response) {

        var JWT = response.data.token;
        localStorage.setItem("JWT", JWT);
        axios.defaults.headers.common['Authorization'] = getJWTHeader();

        userAuth.isAuthenticated = true;
        setUserAuth(response.data);

        router.go(-2);
    }).catch(function (errors) {

        console.log(errors);
    })
}

export function getJWTHeader() {
    return "JWT " + localStorage.getItem("JWT");
}

export function getUserAccount(username) {

     axios.get(baseURL + "v1/users/" + username)
         .then(function (response) {
             return response;
         }).catch(function (err) {
             return err;
     })
}

export function setUserAuth(data) {

    
    userAuth.user.username = data.user.username;
    userAuth.user.email = data.user.email;
    userAuth.user.firstName = data.user.first_name;
    userAuth.user.lastName = data.user.last_name;
    userAuth.user.avatar = data.user.avatar;
    userAuth.user.id = data.user.id;

    return userAuth;
}


export function logout() {
    localStorage.removeItem("JWT");
    authenticationStatus();
}

export function authenticationStatus() {
    var JWT = localStorage.getItem('JWT');
    var decoded = {};

    if (!JWT) { return false; }

    decoded = jwt_decoded(JWT);
    return decoded.exp > Date.now() / 1000;

}



