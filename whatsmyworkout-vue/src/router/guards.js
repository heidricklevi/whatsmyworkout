import store from '../store.js';

export default function requireAuth(to, from, next) {
    console.log('to', to);
    if (store.state.userAuth.isAuthenticated){

        next();
    }
    else {
        next('/login/');
    }
}