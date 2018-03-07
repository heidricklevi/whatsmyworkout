<template>
    <v-layout row wrap v-if="!forbidden">
        <v-flex md4 xs12>
            <!--<v-flex md6 xs12>
                <v-card class="mb-2">
                    <router-link to="/user/dashboard/"><v-btn icon class="pa-0 ma-0"><v-icon large>chevron_left</v-icon></v-btn><span class=" text-xs-center">Your Dashboard</span></router-link>
                </v-card>
            </v-flex>-->
            <user-friend-profile :user-auth="userProfileProp" :username="username"></user-friend-profile>
        </v-flex>
        <v-flex md8 xs12>
            <v-flex md8 offset-md2 xs12>
                    <v-card class="blue-grey lighten-5" :class="{'mt-4': $vuetify.breakpoint.smAndDown }">
                          <v-layout row wrap >
                            <v-flex xs6 text-xs-center>
                                <v-avatar><img :src="userProfileProp.user.avatar"></v-avatar>
                                 <span class="subheading grey--text text--darken-1">{{ userProfileProp.user.username }}</span>
                            </v-flex>
                            <v-flex  xs6 text-xs-center fill-height>
                                <v-avatar icon class="pr-0 mr-0"><v-icon color="primary">access_time</v-icon></v-avatar>
                                <span class="grey--text text--darken-1">{{ userProfileProp.user.date_joined | moment }}</span>
                            </v-flex>
                            <!--<v-flex md4 xs6 text-xs-center>
                                <v-avatar icon class="pr-0 mr-0">
                                    <v-icon color="primary">event</v-icon>
                                </v-avatar>
                                <span class="grey--text text--darken-1">{{ userProfileProp.user.date_joined | moment }}</span>
                            </v-flex>-->
                          </v-layout>
                        </v-card>
            </v-flex>
            <v-flex md10 offset-md1 class="mt-4">
                <v-tabs icons-and-text centered color="grey lighten-3">
                   <v-tabs-slider color="primary"></v-tabs-slider>
                   <v-tab href="#tab-1">
                        Last 5 Workouts
                    </v-tab>

                   <v-tab-item
                      v-for="i in 1"
                      :key="i"
                      :id="'tab-' + i"
                      >
                      <v-container fluid grid-list-md>
                            <v-data-iterator
                              content-tag="v-layout"
                              row
                              wrap
                              :items="items"
                              :rows-per-page-items="rowsPerPageItems"
                              :pagination.sync="pagination"
                            >
                              <v-flex
                                slot="item"
                                slot-scope="props"
                                md6
                                xs12
                              >
                                <v-card>
                                  <v-card-title class="pt-2 pl-2 pb-0">
                                      <v-avatar  ><img :src="userProfileProp.user.avatar"></v-avatar>
                                      <span class="body grey--text text--darken-2">{{ username }}</span>
                                      <span class="caption d-inline-block" style="float: right"><v-icon small color="primary">event </v-icon>
                                          {{ props.item.date_for_completion | moment }}</span>
                                      <v-layout row>
                                          <v-flex text-md-right text-xs-center xs8>
                                              <p class="headline primary--text">{{ props.item.title }}</p>
                                          </v-flex>
                                         <v-flex class="pt-0" xs4 text-xs-right>
                                             <span class="caption grey--text text--darken-1 ">
                                                <img height="16px" width="16px" src="../assets/img/muscle.png">
                                                    {{ props.item.target_muscle }}
                                            </span>
                                         </v-flex>
                                      </v-layout>
                                  </v-card-title>
                                  <v-divider class="mt-0"></v-divider>
                                  <v-list dense>
                                      <template v-for="(exercise, i) in props.item.exercises" v-if="props.item.exercises.length > 0">
                                    <v-list-tile  >

                                      <v-list-tile-content class="grey--text text--darken-4">{{ i+1 }}. {{ exercise.exercise_name }}</v-list-tile-content>
                                      <v-list-tile-content class="align-end grey--text text--darken-1">{{ exercise.sets }} x {{ exercise.reps }}
                                      <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="exercise.lifting_weight">
                                          @ {{ exercise.lifting_weight }} lbs.
                                      </v-list-tile-content>
                                      </v-list-tile-content>


                                    </v-list-tile>
                                          <v-divider></v-divider>
                                          </template>
                                  </v-list>
                                  <v-flex text-xs-center xs12 v-if="props.item.exercises.length <= 0">
                                      <p class="title grey--text text--darken-3">No exercises were created for this workout.</p>
                                  </v-flex>
                                </v-card>
                              </v-flex>
                            </v-data-iterator>
                          </v-container>
                   </v-tab-item>
                </v-tabs>
            </v-flex>
        </v-flex>
    </v-layout>
    <v-container v-else-if="forbidden">
        <v-layout>
            <v-flex md6 offset md-3 xs12>
                <p class="headline">You do not have the necessary permissions to view this profile.</p>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import { baseURLLocal} from '../auth/auth-utils'

    import UserFriendProfile from './user-friend-profile.vue'

    export default {
        name: "user-public-profile",
        components: { UserFriendProfile, },
        props: [],
        data () {
            return {

                username: this.$route.params.username,
                loading: false,
                forbidden: false,
                userProfileProp: {
                    user: {},
                },
                profile_id: null,
                rowsPerPageItems: [2, 8, 12],
                pagination: {
                    rowsPerPage: 2
                  },
                items: [],
                loadLastFive: false,

            }
        },
        filters: {
            moment(date) {
                return moment(date).format("MMM Do YY");
            }
        },
        computed: {

        },
        watch: {

            '$route' (to, from) {
                this.fetchProfileData();
            },


        },
        methods: {

            fetchProfileData () {
                //this.loading = true;
                axios.get(baseURLLocal+"v1/users/" + this.username +'/').then(response => {
                    //this.userProfileProp.user.profile_id = response.data.user.profile_id;

                    this.userProfileProp.user = response.data;
                    this.$store.commit('setData', response.data);
                    //this.loading = false;


                }).catch( err => {

                    let status_FORBIDDEN_403 = 403;

                    this.forbidden = status_FORBIDDEN_403 === err.response.status;

                    //this.loading = false;
                    console.log(err.status);
                    console.log(err.response.status);
                    console.log(err)
                })
            },

            fetchLastFive () {
                this.loadLastFive = true;

                axios.get(baseURLLocal+'v1/friend-workouts/?friend='+this.username).then(response => {
                    this.loadLastFive = false;
                    this.items = response.data.results;

                }).catch(err => {
                    this.loadLastFive = false;
                    console.log(err);
                })

            },
        },

        created () {

            axios.all([this.fetchProfileData(), this.fetchLastFive()]).then(axios.spread(function (acct, perms) {
                //this.loading = false;
                console.log(acct, perms);


            }))
        }
    }
</script>

<style scoped>

</style>