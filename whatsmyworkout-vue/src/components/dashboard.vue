<template >
 <div>
    <div class="sidenav">
        <div class="close-button"><a href="#"><i class="fa fa-times fa-close"></i></a></div>
        <ul class="side-nav-list">
                <li><router-link to="/" ><img class="side-nav-img" src="../assets/img/dashboard.svg">Dashboard</router-link></li>
                <li><router-link to="/create-workout/"><img class="side-nav-img" src="../assets/img/clipboard.svg">Create Workouts</router-link></li>
                <li><a href="#"><img class="side-nav-img" src="../assets/img/calendar.svg">Schedule</a></li>
                <li><a href="#"><img class="side-nav-img" src="../assets/img/envelope.svg">Share</a></li>
                <li><a href="#"><img class="side-nav-img" src="../assets/img/archive.svg">Archives</a></li>
        </ul>

    </div>
     <div id="side-nav" class="side-nav-main">
        <ul class="side-nav-list-main">
                    <li class="side-nav-dashboard-li"><router-link to="/" class="dashboard-workout-text"><img class="side-nav-img" src="../assets/img/dashboard.svg"></router-link></li>
                    <li><router-link class="create-workout-text" to="/create-workout/" ><img class="side-nav-img" src="../assets/img/clipboard.svg"></router-link></li>
                    <li class="side-nav-li"><a class="calendar-workout-text" href="#"><img class="side-nav-img" src="../assets/img/calendar.svg"></a></li>
                    <li class="side-nav-li"><a class="share-workout-text" href="#"><img class="side-nav-img" src="../assets/img/envelope.svg"></a></li>
                    <li class="side-nav-li"><a class="archive-workout-text" href="#"><img class="side-nav-img" src="../assets/img/archive.svg"></a></li>
        </ul>
    </div>
    <div id="main" class="main">
        <nav class="header">
            <div class="header-logo">
                <div class="header-toggle">
                    <i class="fa fa-bars ham-menu" aria-hidden="true"></i>
                    <a class="navbar-brand" href="#"><img src="../assets/img/logo.png" class="rounded-circle size-for-mobile"></a>
                </div>
            </div>
            <div class="header-nav">
                <div class="header-nav-item logout"><router-link to="/" class="header-nav-link" >
                    <img src="../assets/img/logout.svg"> </router-link></div>
                <div class="header-nav-item settings " > <div class="header-nav-link" >
                    <img src="../assets/img/settings.svg">
                    </div>
                </div>
                <div class="header-nav-item user-avatar">
                    <div class="header-nav-link" id="dd">
                        <img  data-toggle="dropdown" :src="userAuth.user.avatar"
                                                  class="avatar cursor-point">
                        <ul class="dropdown-header-settings dropdown-menu">
                            <li><div><img src="../assets/img/settings.svg"> <a href="#">Account Settings</a></div></li>
                            <li><div><img src="../assets/img/Name_24.png"><a href="#">Profile Settings</a></div></li>
                            <div class="dropdown-divider"></div>
                            <li><div><img src="../assets/img/logout.svg"><a @click="logout" href="">Logout</a></div></li>
                        </ul>
                    </div>
                </div>
            </div>
        </nav>
        <div class="container-fluid">
            <router-view></router-view>
        </div>
    </div>
</div>
</template>

<script>

import { userAuth, login, authenticationStatus, logout, getUserAccount, getJWTHeader, setUserAuth } from '../auth/auth'
import router from '../router/index'
import jwt_decode from 'jwt-decode'
import axios from 'axios'

export default {
    name: 'dashboard',
    data () {
        return {
            userAuth: userAuth,
        }
    },
    methods: {
      logout: function (){
          logout();
          router.go('/')
      },

    },
}

</script>