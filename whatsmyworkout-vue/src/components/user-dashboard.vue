<template>
    <v-layout row wrap>
        <v-flex xs12 md4 >
            <user-profile :user-auth="userAuth" :class="{'mb-4': $vuetify.breakpoint.smAndDown }"></user-profile>
            <max-lifts-dashboard-widget class="mt-4"></max-lifts-dashboard-widget>
        </v-flex>
        <v-snackbar v-model="snackbar1" :error="context1 === 'error'" :success="context1 === 'success'" :top="y === 'top'">
                    {{ snackbarText1 }}
                </v-snackbar>
        <v-flex md3 xs12 offset-md1>
            <v-snackbar v-model="snackbar" :color="snackColor" :error="context === 'error'" :success="context === 'success'" :top="y === 'top'">
                            {{ snackbarText }}
                        </v-snackbar>
            <v-container fluid grid-list-md v-if="nextWorkoutItems.length > 0">
                    <v-data-iterator

                      content-tag="v-layout"
                      row
                      wrap
                      :items="nextWorkoutItems"
                      :rows-per-page-items="rowsPerPageItems"
                      :pagination.sync="pagination"
                    >
                      <v-flex
                        slot="item"
                        slot-scope="props"
                        xs12
                      >
                        <v-card>
                            <v-layout  row wrap>
                                <v-flex xs8 md9 class="pa-0">
                                    <v-avatar class="ml-2 mt-2"><img :src="userAuth.user.avatar"></v-avatar>
                                    <div class="d-inline subheading  grey--text text--lighten-1 mt-0 mb-0 text-sm-center"
                                                style="text-transform: uppercase; letter-spacing: 0.9px">
                                            Next Workout</div>

                                    <div class="caption text-md-center text-xs-right text-sm-center ml-4 pl-1" style="position: relative; top: -15px;">
                                        <v-icon small>event</v-icon>
                                        {{ props.item.date_for_completion | moment }}
                                    </div>
                                </v-flex>
                                <v-flex xs4 md3 text-xs-right align-end class="pa-0">

                                    <v-btn icon @click.native="isEmailWorkout = !isEmailWorkout" class="ml-0 mr-0">
                                            <v-icon v-if="!isEmailWorkout" small color="accent">send</v-icon>
                                            <v-icon class="red--text" small v-if="isEmailWorkout">cancel</v-icon>
                                    </v-btn>
                                        <router-link to="/workout/edit/">
                                            <v-btn icon class="mr-0 ml-0" @click="commitToStore">
                                                <v-icon small color="primary">edit</v-icon>
                                            </v-btn>
                                        </router-link>

                                </v-flex>
                                <v-flex xs10 class="pb-2 ">

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

                                </v-flex>
                                <v-flex xs12 class="pt-0"><v-divider class="mt-1"></v-divider></v-flex>

                            </v-layout>
                            <v-card-media :src="props.item.workout_image" contain height="300px">
                                <v-layout row justify-center>
                                    <v-flex text-xs-center xs12>
                                        <h6 class="display-1 primary--text text--darken-2 ">
                                            {{ props.item.title }}</h6></v-flex></v-layout>
                            </v-card-media>
                            <v-progress-circular style="position:absolute; top: 50%; right: 50%; "  v-if="loadingWorkout" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                            <v-divider></v-divider>
                            <v-card-actions>

                                <v-btn flat class="primary--text text--lighten-2 pl-0 pt-0" @click.native="viewExercises = !viewExercises">View Exercises</v-btn>
                                <v-spacer></v-spacer>
                                <v-btn icon @click.native="viewExercises = !viewExercises">
                                    <v-icon color="primary">{{ viewExercises ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                                </v-btn>
                            </v-card-actions>
                            <v-card-text v-if="viewExercises">
                                <v-list dense class="hidden-sm-and-down">
                                      <template v-for="(exercise, i) in props.item.exercises" v-if="props.item.exercises.length > 0">
                                    <v-list-tile  :key="exercise.id">

                                      <v-list-tile-content class="grey--text text--darken-4">{{ i+1 }}. {{ exercise.exercise_name }}</v-list-tile-content>
                                      <v-list-tile-content class="align-end grey--text text--darken-1 pt-2">{{ exercise.sets }} x {{ exercise.reps }}
                                      <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="exercise.lifting_weight">
                                          @ {{ exercise.lifting_weight }} lbs.
                                      </v-list-tile-content>
                                      </v-list-tile-content>


                                    </v-list-tile>
                                        <toggle-exercise-notes  v-if="exercise.notes" :exercise="exercise" :index="i" :opened="exercise.isOpened"></toggle-exercise-notes>
                                          <v-divider v-if="i !== props.item.exercises.length - 1"  class="mt-2"></v-divider>
                                          </template>
                                  </v-list>
                                <v-layout row wrap class="hidden-md-and-up" v-for="(exercise, i) in props.item.exercises" v-if="props.item.exercises.length > 0">
                                    <!--<v-list-tile  :key="exercise.id">

                                      <v-list-tile-content class="grey--text text--darken-4">{{ i+1 }}. {{ exercise.exercise_name }}</v-list-tile-content>
                                      <v-list-tile-content class="align-end grey--text text--darken-1 pt-2">{{ exercise.sets }} x {{ exercise.reps }}
                                      <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="exercise.lifting_weight">
                                          @ {{ exercise.lifting_weight }} lbs.
                                      </v-list-tile-content>
                                      </v-list-tile-content>


                                    </v-list-tile>-->
                                    <v-flex xs8 text-xs-left>
                                        <span class="grey--text text--darken-2">{{ i+1 }}.  {{ exercise.exercise_name }}</span>
                                    </v-flex>
                                    <v-flex xs4 text-xs-right>
                                        <span  class="align-end grey--text text--darken-1 pt-2" style="font-size: 13px">{{ exercise.sets }} x {{ exercise.reps }}</span>
                                        <p class="pb-0 mb-0 align-end caption grey--text text--lighten-1" v-if="exercise.lifting_weight">
                                          @ {{ exercise.lifting_weight }} lbs.
                                      </p>
                                    </v-flex>
                                        <toggle-exercise-notes  v-if="exercise.notes" :exercise="exercise" :index="i" :opened="exercise.isOpened"></toggle-exercise-notes>
                                          <v-flex xs12 class="pa-0"><v-divider v-if="i !== props.item.exercises.length - 1"  class="mt-1 mb-2"></v-divider></v-flex>
                                </v-layout>
                            </v-card-text>
                        </v-card>
                      </v-flex>
                    </v-data-iterator>

            </v-container>
            <v-card v-else="nextWorkoutItems">
                    <v-card-text>
                        No upcoming workouts have been scheduled. Head on over <router-link to="/create-workout/">here</router-link> to create your workouts and see the next one scheduled show up here
                    </v-card-text>
                </v-card>
        </v-flex>
        <v-flex xs12 offset-md1 md3 :class="{'mt-4': $vuetify.breakpoint.smAndDown }">
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

                      <v-flex xs10 offset-xs1 md10>
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


                        </v-flex>


                    </v-layout>

                </v-tab-item>
            </v-tabs>
        </v-card>
           <v-flex xs12 class="mt-4">
            <v-card>
                <v-card-title>
                    <v-icon>people</v-icon>
                    <h5 class=" d-inline-flex subheading grey--text text--darken-2 ma-3">
                        My Friends
                    </h5>
                </v-card-title>
                <v-divider></v-divider>
                    <v-list  v-if="getMyFriends.length > 0" id="friends-list">
                        <template v-for="(friend, i) in getMyFriendsListPagination">
                        <v-list-tile >
                            <v-list-tile-avatar>
                                <img :src="friend.from_user.avatar">
                            </v-list-tile-avatar>
                            <v-list-tile-content>
                                <v-list-tile-title><router-link :to="friend.url">{{ friend.from_user.username }}</router-link></v-list-tile-title>
                            </v-list-tile-content>
                            <v-list-tile-action>
                                <v-btn :key="friend.id"  icon @click="onClickRemoveDialog(friend)"><v-icon color="error">remove_circle_outline</v-icon></v-btn>
                            </v-list-tile-action>

                        </v-list-tile>


                              <v-dialog
                                    v-model="deleteDialog"
                                    transition="dialog-bottom-transition"
                                    :overlay="false"
                                    max-width="290"
                                    >
                                    <v-card>
                                        <v-card-title class="title">Are you sure you want to remove {{ getFriendToDelete? getFriendToDelete.from_user.username: 'None' }}  from your friends list?</v-card-title>

                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn flat :disabled="friendRemoveDisabled" color="warning" @click.native="onRemoveFriend(getFriendToDelete)">Remove</v-btn>
                                            <v-btn flat color="primary" @click.native="deleteDialog = false">Cancel</v-btn>
                                        </v-card-actions>
                                    </v-card>
                              </v-dialog>
                            <v-divider inset v-if="i !== getMyFriendsListPagination.length - 1"></v-divider>
                        </template>
                    </v-list>
                    <v-layout flex justify-center v-else>
                        <v-card-text>
                            <p class="subheading"> No Friends to Display.</p>
                        </v-card-text>
                    </v-layout>


                            <v-snackbar v-model="removeFriendSbModel" :color="removeFriendSbColor" top>{{ removeFriendSbText }}</v-snackbar>

            </v-card>
               <v-pagination :length="getFriendNumberOfPages" v-model="friendPagination.page"></v-pagination>
               </v-flex>
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
import ToggleExerciseNotes from './toggle-exercise-notes.vue'
import MaxLiftsDashboardWidget from './max-lifts-dashboard-widget.vue'


export default {
    name: 'user-dashboard',
    data() {
        return {
            rowsPerPageItems: [1, ],
            pagination: {
                rowsPerPage: 1
            },
            nextWorkoutItems: this.$store.state.userDashboard.recentWorkouts,


            friendPagination: {
                page: 1,
                total: this.$store.state.userDashboard.friendsCount,
                perPage: 5,
            },

            seeNotes: false,

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
            friendToDelete: null,
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

        getFriendToDelete: {
            get: function () {
                return this.friendToDelete;
            },

            set: function (toDelete) {
                this.friendToDelete = toDelete;
            }
        },
        getMyFriends () {
            let friendsList = this.$store.state.userDashboard.friends;
            friendsList.map((fr) => {fr.toggleDisplay = true; fr.url = '/profile/'+fr.from_user.username;  return fr});

            return friendsList;
        },


        getFriendOffset () {
            return ((this.friendPagination.page - 1) * this.friendPagination.perPage);
        },
        getFriendLimit () {

            return (this.getFriendOffset + this.friendPagination.perPage);
        },

        getFriendNumberOfPages () {
           return Math.ceil(this.$store.state.userDashboard.friendsCount / this.friendPagination.perPage)
        },

        getMyFriendsListPagination () {
          let friends = this.$store.state.userDashboard.friends;
          friends.map((fr) => {fr.toggleDisplay = true; fr.url = '/profile/'+fr.from_user.username;  return fr});

          return friends.slice(this.getFriendOffset, this.getFriendLimit);

        },



        getNextWorkoutItems: {
            get: function () {

                return this.nextWorkoutItems;
            },

            set: function (item) {
                console.log(item)
            }
        },
        getSentRequests () {

            //this.getPendingRequests();
            return this.$store.state.userDashboard.sentFriendRequests;
        },

        getReceivedRequests () {

            return this.$store.state.userDashboard.receivedFriendRequests;
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

        onClickRemoveDialog(friend) {

            console.log(friend? friend.from_user.username: 'none');
            this.getFriendToDelete = friend;
            this.deleteDialog = true;
        },

        toggleNotes (workout, exercise) {

            console.log(workout, exercise)

            let workoutIndex = this.nextWorkoutItems.findIndex(workoutIndex => workoutIndex.id === workout.id);
            let exerciseIndex = this.nextWorkoutItems[workoutIndex].exercises.findIndex(eIndex => eIndex.id === exercise.id);

            console.log(workoutIndex);
            console.log(exerciseIndex);

            this.nextWorkoutItems[workoutIndex].exercises[exerciseIndex].isOpened = true;

        },
        querySelections: _.debounce(function(v) {
            this.loadingFriendSearch = true;
            this.friendsList = [];


            if (v) {
                axios.get(baseURLLocal + 'v1/friends/find?search=' + v).then(response => {

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

            500
            ),


        onRemoveFriend(friend) {

            this.friendRemoveDisabled = true;

            axios.delete(baseURLLocal+'v1/user/friends/', { params: { id: friend.from_user.id } } ).then(response => {
                console.log(response);
                this.deleteDialog = false;

                this.removeFriendSbColor = 'success';
                this.removeFriendSbModel = true;
                this.removeFriendSbText = 'Successfully removed '+friend.from_user.username+' from your friends list';
                console.log(response);
                this.getFriends();

                this.friendRemoveDisabled = false;
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
                this.friendsCount = response.data.count;

                this.$store.commit('setFriendCount', this.friendsCount);

                this.friends.map( (friend) => {friend.url = '/profile/'+friend.from_user.username; return friend});

                this.$store.commit('setFriends', this.friends);
                this.loading = false;
            }).catch(err => {
                console.log(err);
            })

        },
        resolveSearch: _.debounce(function(queryVal) {
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
            500
        ),
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

            self.nextWorkoutItems = response.data.results;
            self.recentWorkouts = response.data.results[0];

            self.loadingWorkout = false;
            if (self.nextWorkoutItems) {
                    self.nextWorkoutItems.map((w) => {
                        if (w.exercises) {
                            w.exercises.map((e) => {
                                e.isOpened = false;
                                return e;
                            });

                            return w;
                        }
                    })
                }


                self.$store.commit('setRecentWorkouts', response.data.results);



            console.log(self.recentWorkouts);
        }).catch(function (e) {
            self.loadingWorkout = false;
            self.context1 = 'error';
            self.snackbar1 = true;
            self.snackbarText1 = "error loading workout";
            console.log('There was an error loading recent workouts');
            console.log(e);
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
        addFollow, userProfile, HandleSentFriendRequests, HandleReceivedFriendRequests, ToggleExerciseNotes, MaxLiftsDashboardWidget
    }


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

    div.tabs__bar {
        border-bottom: 1px solid;
        border-bottom-color: rgba(0,0,0,.12);
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

  #friends-list a:hover {
      color: #263238;
  }

  .widget-title {
      letter-spacing: 2px!important;
      text-transform: uppercase!important;

  }
</style>
