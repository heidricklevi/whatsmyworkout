/**
 * Created by LeviJamesH on 7/8/2017.
 */

import jwt_decoded from 'jwt-decode'


export let baseURLLocal = "/";


export function getJWTHeader() {
    //exact format to set the Authorization header for requests
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