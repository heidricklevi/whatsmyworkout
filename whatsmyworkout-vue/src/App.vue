<template >
 <div v-if="isAuthenticated">
    <div class="sidenav">
        <div class="close-button"><a href="#"><i class="fa fa-times fa-close"></i></a></div>
        <ul class="side-nav-list">
                <li><router-link to="/" ><img class="side-nav-img" src="../src/assets/img/dashboard.svg">Dashboard</router-link></li>
                <li><router-link to="/create-workout/"><img class="side-nav-img" src="../src/assets/img/clipboard.svg">Create Workouts</router-link></li>
                <li><a href="#"><img class="side-nav-img" src="../src/assets/img/calendar.svg">Schedule</a></li>
                <li><a href="#"><img class="side-nav-img" src="../src/assets/img/envelope.svg">Share</a></li>
                <li><a href="#"><img class="side-nav-img" src="../src/assets/img/archive.svg">Archives</a></li>
        </ul>

    </div>
     <div id="side-nav" class="side-nav-main">
        <ul class="side-nav-list-main">
                    <li class="side-nav-dashboard-li"><a class="dashboard-workout-text" href="#"><img class="side-nav-img" src="../src/assets/img/dashboard.svg"></a></li>
                    <li><router-link class="create-workout-text" to="/create-workout/" ><img class="side-nav-img" src="../src/assets/img/clipboard.svg"></router-link></li>
                    <li class="side-nav-li"><a class="calendar-workout-text" href="#"><img class="side-nav-img" src="../src/assets/img/calendar.svg"></a></li>
                    <li class="side-nav-li"><a class="share-workout-text" href="#"><img class="side-nav-img" src="../src/assets/img/envelope.svg"></a></li>
                    <li class="side-nav-li"><a class="archive-workout-text" href="#"><img class="side-nav-img" src="../src/assets/img/archive.svg"></a></li>
        </ul>
    </div>
    <div id="main" class="main">
        <nav class="header">
            <div class="header-logo">
                <div class="header-toggle">
                    <i class="fa fa-bars ham-menu" aria-hidden="true"></i>
                    <a class="navbar-brand" href="#"><img src="../src/assets/img/logo.png" class="rounded-circle size-for-mobile"></a>
                </div>
            </div>
            <div class="header-nav">
                <div class="header-nav-item logout"><a class="header-nav-link" href="{% url 'logout' %}">
                    <img src="../src/assets/img/logout.svg"> </a></div>
                <div class="header-nav-item settings " > <div class="header-nav-link" >
                    <img src="../src/assets/img/settings.svg">
                    </div>
                </div>
                <div class="header-nav-item user-avatar">
                    <div class="header-nav-link" id="dd">
                        <img  data-toggle="dropdown" src="../src/assets/img/levi_heidrick.jpg"
                                                  class="avatar cursor-point">
                        <ul class="dropdown-header-settings dropdown-menu">
                            <li><div><img src="../src/assets/img/settings.svg"> <a href="#">Account Settings</a></div></li>
                            <li><div><img src="../src/assets/img/Name_24.png"><a href="#">Profile Settings</a></div></li>
                            <div class="dropdown-divider"></div>
                            <li><div><img src="../src/assets/img/logout.svg"><a href="#">Logout</a></div></li>
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
<div class="container-fluid" v-else="isAuthenticated">
    <div class="row">
        <div class="col-sm-12 col-md-8 push-md-2">
            <div class="card text-center">
              <div class="card-header">
                <ul class="nav nav-tabs card-header-tabs">
                  <li class="nav-item">
                    <a class="nav-link active" href="#">Active</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link disabled" href="#">Disabled</a>
                  </li>
                </ul>
              </div>
              <div class="card-block">
                <h4 class="card-title">Special title treatment</h4>
                <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                  <form v-on:submit.prevent="userLogin" id="loginform" method="post">
                    <div class="form-group row">
                      <label for="username" class="col-2 col-form-label">Username</label>
                      <div class="col-10">
                        <input v-model="username" class="form-control" type="text" id="username">
                      </div>
                    </div>
                    <div class="form-group row">
                      <label for="password" class="col-2 col-form-label">Password</label>
                      <div class="col-10">
                        <input v-model="password" class="form-control" type="password" id="password">
                      </div>
                    </div>
                    <div class="form-group row">
                      <div class="col-10">
                        <input class="btn btn-primary" type="submit" value="Login">
                      </div>
                    </div>
                  </form>
              </div>
            </div>
         </div>
    </div>
</div>
</template>

<script>

import { userAuth, login, authenticationStatus } from '../src/auth/auth'
import router from '../src/router/index'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      isAuthenticated: authenticationStatus(),
      username: '',
      password: '',
    }
  },
    watch: {
      isAuthenticated: function (val) {
          router.go('/');
      }
    },
    methods: {
      userLogin: function () {
          login(this.username, this.password);
          console.log(userAuth);
      },
        
    }
}
</script>

