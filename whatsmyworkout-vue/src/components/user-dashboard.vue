<template>
    <v-layout row wrap>
        <user-profile :user-auth="userAuth" :class="{'mb-4': $vuetify.breakpoint.smAndDown }"></user-profile>
        <v-flex xs12 offset-md1 md3>
                     <v-snackbar v-model="snackbar" :color="snackColor" :error="context === 'error'" :success="context === 'success'" :top="y === 'top'">
                            {{ snackbarText }}
                        </v-snackbar>

            <v-card v-if="recentWorkouts">
                <v-snackbar v-model="snackbar1" :error="context1 === 'error'" :success="context1 === 'success'" :top="y === 'top'">
                    {{ snackbarText1 }}
                </v-snackbar>
                <v-flex xs12>
                    <div class="pt-1 pl-1" style="display: inline-flex">
                        <v-avatar>
                            <img :src="userAuth.user.avatar">
                        </v-avatar>
                        <span class="title pl-2 pt-2 card-title grey--text">Next Workout </span>
                        <div style="position: absolute; right: 0; top: 0;">
                            <v-btn icon @click.native="isEmailWorkout = !isEmailWorkout" style="margin-right: 0">
                                <v-icon v-if="!isEmailWorkout">email</v-icon>
                                <v-icon class="red--text" v-if="isEmailWorkout">cancel</v-icon>
                            </v-btn>
                            <router-link to="/workout/edit/">
                                <v-btn icon class="mr-1" @click="commitToStore">
                                    <v-icon>edit</v-icon>
                                </v-btn>
                            </router-link>
                        </div>
                    </div>

                    <div style="margin-left: 15%; position:relative; top: -15px;">
                        <v-icon class="mr-1">event</v-icon>
                        <span class="caption">{{ recentWorkouts.date_for_completion | moment }}</span>
                    </div>
                </v-flex>

                    <v-card raised v-if="isEmailWorkout" style="border-color: lightslategray; border-bottom-width: 5px;
                                                            position: absolute; height: 200px; top: 50px; width: 100%; z-index: 2">

                        <form method="post" v-on:submit.prevent="sendWorkout">
                            <v-card-title>
                                Send this workout to a friend
                            </v-card-title>
                        <v-layout row>
                            <v-flex xs8 offset-xs2 md8 text-xs-center>
                            <v-select
                                    v-model="shareFriendWorkout"
                                    label="Search Friends"
                                    append-icon="search"
                                    return-object
                                    item-text="from_user.username"
                                    item-value="from_user.username"

                                    :items="friendsList"
                                    chips
                                    :loading="loadingFriendSearch"
                                    autocomplete
                                    :search-input.sync="searchFriends"
                                    required
                            >
                                <template slot="selection" slot-scope="data">

                                    <v-chip
                                      close
                                      @input="data.parent.selectItem(data.item.from_user)"
                                      :selected="data.selected"
                                      :key="JSON.stringify(data.item.from_user)"
                                    >
                                      <v-avatar>
                                        <img :src="data.item.from_user.avatar">
                                      </v-avatar>
                                      {{ data.item.from_user.username }}
                                    </v-chip>
                                  </template>
                                <template slot="item" slot-scope="data">
                                    <template v-if="typeof data.item !== 'object'">
                                        <v-list-tile-content v-text="data.item"></v-list-tile-content>
                                    </template>
                                <template v-else>
                                  <v-list-tile-avatar>
                                    <img :src="data.item.from_user.avatar">
                                  </v-list-tile-avatar>
                                  <v-list-tile-content>
                                    <v-list-tile-title v-html="data.item.from_user.username"></v-list-tile-title>
                                  </v-list-tile-content>
                                </template>
                              </template>
                            </v-select>
                            </v-flex>
                            </v-layout>
                            <v-layout>
                            <v-flex xs12 text-xs-center>
                                <v-btn color="primary" :loading="loading" type="submit" :disabled="loading" @click.native="loader = 'loading'">
                                    Send
                                    <span slot="loader" class="custom-loader">
                                        <v-icon>cached</v-icon>
                                    </span>
                                </v-btn>

                            </v-flex>
                                </v-layout>



                        </form>
                        </v-card>
                <v-divider></v-divider>
                <v-card-title>
                    <h3 class="headline">{{ recentWorkouts.title }}</h3>
                </v-card-title>
                <v-card-media id="workout-image" :src="recentWorkouts.workout_image" height="200px" contain>

                </v-card-media>
                <v-progress-circular style="position:absolute; top: 50%; right: 50%; "  v-if="loadingWorkout" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                <v-divider></v-divider>
                <v-card-actions>

                    <v-btn flat class="blue--text text--darken-4 pl-0 pt-0" @click.native="viewExercises = !viewExercises">View Exercises</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn icon @click.native="viewExercises = !viewExercises">
                        <v-icon class="blue--text text--darken-4">{{ viewExercises ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                    </v-btn>
                </v-card-actions>
                <v-slide-y-transition>
                    <v-card-text v-if="viewExercises">
                        <v-list three-line subheader>
                            <v-layout row justify-center>
                                <v-flex xs6>
                                    <v-subheader>Exercise</v-subheader>
                                </v-flex>
                                <v-flex xs3 offset-xs1>
                                    <v-subheader class="text-xs-center">sets/reps</v-subheader>
                                </v-flex>
                            </v-layout>

                            <template v-for="(exercise, i) in recentWorkouts.exercises">


                                <v-list-tile style="padding: 0">
                                    <v-list-tile-content>
                                        <v-layout style="width: 100%" row wrap :key="exercise.exercise_name">


                                            <v-flex style="display: flex;" xs12>
                                                <v-flex xs1 class="ml-1">
                                                    <div style="text-align: center;">{{ i+1 }}.</div>
                                                </v-flex>
                                                <v-flex xs8 class="body-1" style="word-wrap: break-word">
                                                    {{ exercise.exercise_name }}
                                                </v-flex>
                                                <v-flex xs2 offset-xs1>
                                                    <div>{{ exercise.sets }}/{{ exercise.reps }}</div>
                                                </v-flex>
                                            </v-flex>
                                            <div style="position: relative; margin-left: 5%"><v-icon style="position: absolute; top: 0;" color=" ">fa-sticky-note-o</v-icon></div>
                                            <div class="caption" style="word-wrap: break-word; margin: 2% 0 0 5%;">
                                                {{ exercise.notes }}
                                            </div>
                                        </v-layout>
                                        <v-layout style="text-align: center">
                                            <div style="word-wrap: break-word; font-size: small; font-weight: 500">
                                                Lifting Weight: <span style="font-style: italic" class="caption">{{ exercise.lifting_weight }}</span></div>
                                        </v-layout>

                                    </v-list-tile-content>

                                </v-list-tile>
                                <v-divider></v-divider>
                            </template>
                        </v-list>
                    </v-card-text>
                </v-slide-y-transition>
            </v-card>
         <v-card v-else="recentWorkouts">
                <v-card-text>
                    No upcoming workouts have been scheduled. Head on over <router-link to="/create-workout/">here</router-link> to create your workouts and see the next one scheduled show up here
                </v-card-text>
            </v-card>
        </v-flex>

        <!--<v-flex xs12  offset-md1 md3>
            <v-card>
                <v-card-title primary-title>
                    <div>
                        <h3 class="headline mb-0">Find Friends or Follow Experts</h3>
                    </div>
                </v-card-title>
                <v-container fluid>
                    <v-layout>
                      <v-flex xs12 offset-md1 md10>
                        <v-text-field
                          label="Search by username"
                          append-icon="search"
                          :loading="loading"

                          required
                          :items="items"
                          @keyup="search = $event.target.value"
                          v-model="select"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>
                </v-container>
              <v-layout>
                <v-flex xs12 offset md1 md12 v-if="items" >
                    <v-list subheader>
                  <v-subheader>Results</v-subheader>
                 <template v-for="(item, index) in items">
                     <add-follow :item="item" :index="index"></add-follow>
                     <v-divider v-bind:key="item.id"></v-divider>
                 </template>
                    </v-list>

                </v-flex>

              </v-layout>
            </v-card>
        </v-flex> -->
        <v-flex xs12 offset-md1 md3 :class="{'mt-4': $vuetify.breakpoint.smAndDown, 'pr-3': $vuetify.breakpoint.mdAndUp }">
    <v-card >
        <v-card-title>Friends</v-card-title>
        <v-tabs v-model="active" centered :scrollable="false" icons-and-text light fixed-tabs>

                  <v-tabs-slider color="blue-grey"></v-tabs-slider>
                <v-tab
                  href="#friends-1"
                  ripple
                >
                  <v-icon>search</v-icon>
                </v-tab>
                  <v-tab href="#friends-2">
                      <v-badge right color="primary" overlap>
                          <span slot="badge">{{ getReceivedRequests.length }}</span>
                          <v-icon color="grey lighten-1" large style="background-color: inherit!important;">people</v-icon>
                      </v-badge>
                  </v-tab>

                <v-tab-item
                  v-for="i in 2"
                  :key="i"
                  :id="'friends-' + i"
                >
                       <v-flex v-if="active == 'friends-1'">
                        <h4 class="subheading ma-3">Connect with others</h4>
                            </v-flex>
                    <v-layout v-if="active == 'friends-1'">

                      <v-flex xs10 offset-1 md10>
                        <v-text-field
                          label="username"
                          append-icon="search"
                          :loading="loading"

                          required
                          :items="items"
                          @keyup="search = $event.target.value"
                          v-model="select"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>

              <v-layout>

                <v-flex xs12 offset md1 md12 v-if="items.length != 0 && active == 'friends-1'">
                    <v-list subheader>
                  <v-subheader>Results</v-subheader>
                 <template v-for="(item, index) in items">
                     <add-follow :item="item" :index="index"></add-follow>
                     <v-divider v-bind:key="item.id"></v-divider>
                 </template>
                    </v-list>

                </v-flex>

                  <v-flex xs12 md12 v-if="active == 'friends-2'">
                          <div class="text-xs-center">
                                  <v-chip color="primary" class="text-xs-center mt-1 mb-1 white--text">
                                  Friends {{ getMyFriends.length }}
                                   </v-chip>
                                <v-chip color="accent" class="text-xs-center mt-1 mb-1 white--text">
                                  Sent {{ getSentRequests.length }}
                                </v-chip>
                                <v-chip color="orange lighten-1" class="text-xs-center mt-1 mb-1 white--text">

                                    Pending {{ getReceivedRequests.length  }}
                                </v-chip>
                          </div>
                        <v-divider class="mt-1" v-if="getReceivedRequests.length > 0"></v-divider>

                      <handle-received-friend-requests></handle-received-friend-requests>

                      <v-divider class="mt-1" v-if="getSentRequests.length > 0"></v-divider>
                      <handle-sent-friend-requests></handle-sent-friend-requests>

                       <v-divider></v-divider>
                      <h5 class="subheading grey--text text--darken-2 ma-3">Friends</h5>
                      <template v-for="friend in getMyFriends">

                                <v-chip

                                        :value="friend.toggleDisplay"
                                        v-model="friend.toggleDisplay"
                                        :key="friend.id"
                                        :disabled="friendRemoveDisabled"
                                        class="ml-2">

                                    <v-avatar>
                                        <img :src="friend.from_user.avatar">
                                    </v-avatar>
                                    <router-link :to="friend.url">{{ friend.from_user.username }}</router-link>
                                    <div class="chip__close red--text" @click="deleteDialog = true"><v-icon >cancel</v-icon></div>
                                </v-chip>



                      <v-dialog
                            v-model="deleteDialog"
                            transition="dialog-bottom-transition"
                            :overlay="false"
                            max-width="290"
                            >
                            <v-card>
                                <v-card-title class="title">Are you sure you want to remove {{ friend.from_user.username }} from your friends list?</v-card-title>

                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn flat :disabled="friendRemoveDisabled" color="warning" @click.native="onRemoveFriend(friend)">Delete</v-btn>
                                    <v-btn flat color="primary" @click.native="deleteDialog = false">Don't Delete</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>

                      </template>

                            <v-snackbar v-model="removeFriendSbModel" :color="removeFriendSbColor" top>{{ removeFriendSbText }}</v-snackbar>

                        </v-flex>


                    </v-layout>

                </v-tab-item>
            </v-tabs>
        </v-card>
         </v-flex>
    </v-layout>
</template>
<script>

import axios from 'axios'
import moment from 'moment'
import { baseURLLocal} from '../auth/auth-utils'

import addFollow from './add-follow.vue'
import userProfile from './user-profile.vue'
import HandleSentFriendRequests from './handle-sent-friend-requests.vue'
import HandleReceivedFriendRequests from './handle-received-friend-requests.vue'


export default {
    name: 'user-dashboard',
    data() {
        return {


            following: '',
            followers: '',
            active: null,
            tabs: ['search-tab', 'friend-tab'],
            search: null,
            select: [],
            items: [],
            recentWorkouts: {},
            userAuth: this.$store.state.userAuth,
            viewExercises: false,
            drawer: true,
            isEmailWorkout: false,
            isArchiveWorkout: false,
            nextWorkout: false,
            shareFriendWorkout: [],
            loader: null,
            loading: false,
            snackbar: false,
            snackbarText: ' ',
            y: 'top',
            context: '',
            context1: '',
            loadingWorkout: true,
            snackbar1: false,
            snackbarText1: '',
            snackColor: '',


            friends: this.$store.state.userDashboard.friends,
            pendingRequests: this.$store.state.userDashboard.sentFriendRequests,



            friendRemoveDisabled: false,
            deleteDialog: false,
            removeFriendSbPosition: 'top',
            removeFriendSbModel: false,
            removeFriendSbText: '',
            removeFriendSbColor: 'success',


            showFriendRequestsBadge: false,

            friendsList: [],
            loadingFriendSearch: false,
            searchFriends: null,

        }
    },
    computed: {


        //Going to stick with friend relationships instead of follow as they are bidirectional and user has more explicit control

        /*getFollows: function () {
            let self = this;

            axios.get(baseURLLocal+'v1/follow/').then(function (response) {
                self.following = response.data.length;
            }).catch(function (err) {
                return "error retrieving following number from server"
            });


            return this.following;
        },
        getFollowers: function () {
            let self = this;

            axios.get(baseURLLocal+'v1/follow/?followers=true').then(function (response) {
                self.followers = response.data.length;
            }).catch(function (err) {
                return "error retrieving following number from server"
            });

            return this.followers;
        }*/

        getSentRequests () {

            //this.getPendingRequests();
            return this.$store.state.userDashboard.sentFriendRequests;
        },

        getReceivedRequests () {

            return this.$store.state.userDashboard.receivedFriendRequests;
        },

        getMyFriends () {
            let friendsList = this.$store.state.userDashboard.friends;
            friendsList.map((fr) => {fr.toggleDisplay = true; fr.url = '/profile/'+fr.from_user.username;  return fr});

            return friendsList;
        },
    },
    watch: {
        search(val) {
            this.resolveSearch(val)
        },

        searchFriends(val) {
              val && this.querySelections(val)
        },

    },
    filters: {
        moment: function (date) {
            return moment(date).format("dddd, MMMM Do YYYY");
        }
    },
    props: ["computedAuth"],
    methods: {

        querySelections (v) {
                this.loadingFriendSearch = true;
                this.friendsList = [];


                if (v) {
                    axios.get(baseURLLocal+'v1/friends/find?search='+v).then(response => {

                    this.friendsList = response.data.results.filter(e => {
                        return (e || '').from_user.username.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.loadingFriendSearch = false;
                    }).catch(err => {
                        this.friendsList = [];
                        console.log(err);
                    })
                }

                else {
                    this.friendsList = [];
                }


        },

        onRemoveFriend(friend) {

            this.friendRemoveDisabled = true;

            axios.delete(baseURLLocal+'v1/user/friends/', { params: { id: friend.from_user.id } } ).then(response => {
                console.log(response);
                this.deleteDialog = false;
                friend.toggleDisplay = false;

                this.removeFriendSbColor = 'success';
                this.removeFriendSbModel = true;
                this.removeFriendSbText = 'Successfully removed '+friend.from_user.username+' from your friends list';
                console.log(response);
                this.getFriends();


            }).catch(err => {
                this.friendRemoveDisabled = false;
                console.log(err);

            });


        },

        getPendingRequests() {

            axios.get(baseURLLocal+ 'v1/friends/?sent_requests=true').then(response => {
                this.$store.commit('setSentFriendRequests', response.data.results);
            }).catch(err => {
                console.log(err);
            })


        },

        getPendingReceivedRequests() {
            axios.get(baseURLLocal+ 'v1/friends/?received_requests=true').then(response => {
                this.$store.commit('setReceivedFriendRequests', response.data.results);
            }).catch(err => {
                console.log(err);
            })
        },

        getFriends() {
            this.loading = true;

            axios.get(baseURLLocal +'v1/friends/').then(response => {
                this.friends = response.data.results;

                this.friends.map( (friend) => {friend.url = '/profile/'+friend.from_user.username; return friend});

                this.$store.commit('setFriends', this.friends);
                this.loading = false;
            }).catch(err => {
                console.log(err);
            })

        },
        resolveSearch(queryVal) {
            this.loading = true;
            this.items = [];
            var that = this;

            if (this.search) {
                axios.get(baseURLLocal + 'v1/users/find?search=' + queryVal).then(function (response) {

                    for (var i = 0; i < response.data.results.length; i++) {


                        that.items[i] = response.data.results[i];


                    }
                    that.loading = false;
                }).catch(function (err) {
                    that.items = [];
                    that.loading = false;
                })
            }
            else {
                this.items = [];
                this.loading = false;
            }
        },
        commitToStore: function () {
            this.$store.commit('setData', [this.recentWorkouts]);
            console.log("Commited to store");
        },
        sendWorkout: function () {
            var self = this;
            var payload = this.recentWorkouts;

            for (var i = 0; i < payload.exercises.length; i++) {
                payload.exercises[i].workout_id = this.recentWorkouts.id;
            }

            payload.to = this.shareFriendWorkout.from_user.username;

            this.loading = true;
            axios.post(baseURLLocal + 'v1/workout/send/', payload)
                .then(function () {
                    self.context = 'success';
                    self.snackbar = true;
                    self.snackbarText = "Successfully sent workout to " + payload.to;
                    self.snackColor = 'green';

                    self.loading = false;
                    console.log('Success')
                }).catch(function (err) {
                self.snackColor = 'error';
                self.snackbar = true;
                self.snackbarText = "Could not send workout to " + payload.to + " error " + err.response.data.status;

                self.loading = false;
                console.log(err)
            })
        }
    },
    created: function () {
        var self = this;


        this.loadingWorkout = true;

        axios.get(baseURLLocal + 'v1/workouts/?next_workout=true').then(function (response) {
            self.recentWorkouts = response.data.results[0];
            self.loadingWorkout = false;


            console.log(self.recentWorkouts);
        }).catch(function (e) {
            self.loadingWorkout = false;
            self.context1 = 'error';
            self.snackbar1 = true;
            self.snackbarText1 = "error loading workout";
            console.log('There was an error loading recent workouts');
        });


    },

    mounted () {
        //this.loading = true;
        axios.all([this.getFriends(), this.getPendingRequests(), this.getPendingReceivedRequests()]).then(axios.spread(function (acct, perms) {
            //this.loading = false;
            console.log(acct, perms);


        }))

    },
    components: {
        addFollow, userProfile, HandleSentFriendRequests, HandleReceivedFriendRequests
    }


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

    div.tabs__bar {
        border-bottom: 1px solid;
        border-bottom-color: rgba(0,0,0,.12);
    }

    div.tabs__wrapper {
        overflow-x: unset;
    }

    .custom-loader {
        animation: loader 1s infinite;
        display: flex;
    }

    @-moz-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-webkit-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-o-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }

    .card > .card__title {
        display: block;
    }

    .card-title {
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0;
    }

</style>
