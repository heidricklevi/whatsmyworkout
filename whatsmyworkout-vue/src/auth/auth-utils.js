/**
 * Created by LeviJamesH on 7/8/2017.
 */

import router from '../router/index'
import axios from 'axios'
import jwt_decoded from 'jwt-decode'


export let baseURLLocal = "http://127.0.0.1:8000/";


export function getJWTHeader() {
    return "JWT " + localStorage.getItem("JWT");
}

export function authenticationStatus() {
    let JWT = localStorage.getItem('JWT');
    let decoded;

    if (!JWT) {
        return false;
    }

    decoded = jwt_decoded(JWT);
    return decoded.exp > Date.now() / 1000;

}

export function getUsernameFromToken() {
    let jwt = localStorage.getItem("JWT");
    let decoded = jwt_decoded(jwt);
    if (!jwt) return false;

    return decoded.username;
}