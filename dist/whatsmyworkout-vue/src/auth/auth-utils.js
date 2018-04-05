"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.baseURLLocal = undefined;
exports.getJWTHeader = getJWTHeader;
exports.authenticationStatus = authenticationStatus;
exports.getUsernameFromToken = getUsernameFromToken;

var _jwtDecode = require("jwt-decode");

var _jwtDecode2 = _interopRequireDefault(_jwtDecode);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var baseURLLocal = exports.baseURLLocal = "/"; /**
                                                * Created by LeviJamesH on 7/8/2017.
                                                */

function getJWTHeader() {
    //exact format to set the Authorization header for requests
    return "JWT " + localStorage.getItem("JWT");
}

function authenticationStatus() {
    var JWT = localStorage.getItem('JWT');
    var decoded = void 0;

    if (!JWT) {
        return false;
    }

    decoded = (0, _jwtDecode2.default)(JWT);
    return decoded.exp > Date.now() / 1000;
}

function getUsernameFromToken() {
    var jwt = localStorage.getItem("JWT");
    var decoded = (0, _jwtDecode2.default)(jwt);
    if (!jwt) return false;

    return decoded.username;
}
//# sourceMappingURL=auth-utils.js.map