<template>
<v-layout>
    <v-flex xs12 md10 offset-md1>
        <v-card>
            <v-card-media :src="userAuth.user.avatar" height="290px"></v-card-media>
            <v-card-title >
                <v-layout row wrap>
                    <v-flex md8>
                        <router-link :to=" authUserProfileId === viewedUserProfileId ? '/user/profile-stats/detail/' : '' ">
                            <h4 class="headline mb-0 ml-3" >Profile Stat Tracking</h4>
                        </router-link>
                    </v-flex>
                    <v-flex md1 offset-xs2 v-if="authUserProfileId === viewedUserProfileId">
                        <v-btn  icon to="/user/profile-stats/detail/" ><v-icon color="accent">edit</v-icon></v-btn>
                    </v-flex>
                </v-layout>
            </v-card-title>
            <span class="ml-3 grey--text">Body Stats</span>
            <span class="caption grey--text text--lighten-1 mr-3 mt-3" style="font-style: italic; float: right;">{{ currentBodyStats.created }}</span>
            <v-layout class="ma-4" v-if="!loading">
                <v-flex md6 xs6 class="pr-2" style="border-right: solid 1px black; text-align: right;">
                    <p class="blue-grey--text text--lighten-2">Height</p>
                    <p class="blue-grey--text text--lighten-2">Weight</p>
                    <p class="blue-grey--text text--lighten-2">BMI</p>
                    <p class="blue-grey--text text--lighten-2">Body Fat</p>

                </v-flex>
                <v-flex md6 xs6 class="pl-2" style="text-align: left;">
                    <p class=" blue-grey--text">{{ currentBodyStats.height | heightDisplay }}</p>
                    <p class=" blue-grey--text">{{ currentBodyStats.weight }} lbs.</p>
                    <p class=" blue-grey--text">{{ currentBodyStats.bmi }}</p>
                    <p class=" blue-grey--text">{{ currentBodyStats.body_fat }}%</p>

                </v-flex>
            </v-layout>
            <v-layout>
                <v-flex text-xs-center>
                    <v-progress-circular indeterminate :size="40" :width="5" color="purple" v-if="loading"></v-progress-circular>
                </v-flex>
            </v-layout>
        </v-card>
    </v-flex>
</v-layout>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import {baseURLLocal} from '../auth/auth-utils'

    export default {
        name: "user-friend-profile",
        data () {
            return {
                currentBodyStats: {},
                bodyStats: [{}],
                authUserProfileId: this.$store.state.userAuth.user.profile_id,
                viewedUserProfileId: this.userAuth.user.profile_id,
                loading: false,


            }
        },
        filters: {
          heightDisplay: function (hInches) {

                return Math.floor(hInches / 12).toString() + '\'' + ' '+ (hInches%12).toString()+'\'\'';
            }
        },
        computed: {

        },
        methods: {


        },
        props: ['userAuth', 'username'],
        created: function () {

        },
        mounted() {
            console.log(this.userAuth);
            console.log(this.viewedUserProfileId);
            console.log(this.authUserProfileId);
            this.loading = true;

            axios.get(baseURLLocal+'v1/body-stats/' +this.username+'/').then(response => {
                this.loading = false;
                
                this.currentBodyStats = response.data; //get most recent stats
                this.currentBodyStats.created = moment(response.data.created).format("MMM Do YY, h:m a");
            }).catch(err =>  {
                this.loading = false;
                console.log(err)
            })
        },

    }
</script>

<style scoped>

</style>