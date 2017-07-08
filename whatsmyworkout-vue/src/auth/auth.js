/**
 * Created by LeviJamesH on 7/8/2017.
 */

import Router from 'vue-router'
import axios from 'axios'

var baseURL = "http://127.0.0.1:8000/";
axios.defaults.headers.common['Authorization'] = getJWT();


var userAuth = {};

export function login(username, pass) {

    var credentials = {
        username: username,
        password: pass,
    };

    axios.post(baseURL + 'v1/login/', credentials
    ).then(function (response) {

        var JWT = response.data.token;
        var expiryDate = new Date();
        var newDate = expiryDate.getDate() + 7;

        expiryDate.setDate(newDate);
        localStorage.setItem("JWT", JWT);
        localStorage.setItem("Expiry", expiryDate);



        console.log(response);

    }).catch(function (errors) {

        console.log(errors);
    })
}

function getJWT() {
    return "JWT " + localStorage.getItem("JWT");
}

function getUserAccount(username) {

    return axios.get(baseURL + "v1/users/" + username);
}

