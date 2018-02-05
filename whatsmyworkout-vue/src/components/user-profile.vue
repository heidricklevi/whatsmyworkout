<template>
<v-layout>
    <v-flex xs12 md10 offset-md1>
        <v-card>
            <v-card-media :src="userAuth.user.avatar" height="200px"></v-card-media>
            <v-card-title>
                <h4 class="headline mb-0">Profile Stat Tracking</h4>
            </v-card-title>
            <span class="ml-3 grey--text">Body Stats</span>
            <span class="caption grey--text text--lighten-1 mr-3 mt-3" style="font-style: italic; float: right;">{{ currentBodyStats.created }}</span>
            <v-layout class="ma-4">
                <v-flex md6 xs6 class="pr-2" style="border-right: solid 1px black; text-align: right;">
                    <p class="blue-grey--text text--lighten-2">Height</p>
                    <p class="blue-grey--text text--lighten-2">Weight</p>
                    <p class="blue-grey--text text--lighten-2">BMI</p>
                    <p class="blue-grey--text text--lighten-2">Body Fat</p>

                </v-flex>
                <v-flex md6 xs6 class="pl-2" style="text-align: left;">
                    <p class=" blue-grey--text">{{ currentBodyStats.height }} in</p>
                    <p class=" blue-grey--text">{{ currentBodyStats.weight }} lbs.</p>
                    <p class=" blue-grey--text">{{ currentBodyStats.bmi }}</p>
                    <p class=" blue-grey--text">{{ currentBodyStats.body_fat }}%</p>

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
        name: "user-profile",
        data () {
            return {
                currentBodyStats: {},
                bodyStats: [{}],


            }
        },
        methods: {


        },
        props: ['userAuth', ],
        created: function () {
            var self = this;
            axios.get(baseURLLocal+'v1/body-stats/').then(function (response) {
                for (var i = 0; i < response.data.count; i++) {
                    self.bodyStats[i] = response.data.results[i];
                }

                self.currentBodyStats = response.data.results[0]; //get most recent stats
                self.currentBodyStats.created = moment(response.data.results[0].created).format("MMM Do YY, h:m a");
            }).catch(function (err) {

            })
        }

    }
</script>

<style scoped>

</style>