<template>
    <v-layout>
        <v-flex xs12 md6>
            <v-card>
                <v-card-title primary-title>
                    <h3 class="headline mb-0">Max Lift Tracking</h3>
                </v-card-title>
                <span class="ml-3 grey--text">Core Movements Tracked</span>
                <span class="caption grey--text text--lighten-1 mr-3 mt-3" style="font-style: italic; float: right;"></span>
                <v-divider></v-divider>
                    <v-layout class="ma-4">
                        <p class="subheading blue-grey--text text--darken-2">Chest</p>
                        <v-flex md4 xs6 class="pr-2" style="border-right: solid 1px black; text-align: right;">
                            <p class="blue-grey--text text--lighten-2">Exercise</p>
                            <p class="blue-grey--text text--lighten-2">Max Type</p>
                            <p class="blue-grey--text text--lighten-2">Weight</p>
                            <p class="blue-grey--text text--lighten-2">Recorded</p>

                        </v-flex>
                        <v-flex md4 xs6 class="pl-2" style="text-align: left;" v-if="chestMax != 0">
                            <p class=" blue-grey--text">{{ chestMax[0].exercise.exercise_name }}</p>
                            <p class=" blue-grey--text">{{ chestMax[0].max_type }}</p>
                            <p class=" blue-grey--text">{{ chestMax[0].weight }} lbs.</p>
                            <p class=" blue-grey--text">{{ chestMax[0].created }}</p>

                        </v-flex>
                    </v-layout>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>

    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'

    export default {
        name: "workout-stats",
        data () {
            return {
                coreMuscles: ['Arms', 'Chest', 'Back', 'Legs'],
                chestMax: [],
                isLoading: false,
                maxLiftsObjects: [],
            }
        },
        computed: {

        },
        methods: {

        },
        created: function () {
            this.isLoading = true;
            let self = this;


            axios.get(baseURLLocal+'v1/max-lifts/').then(function (response) {
                console.log(response);
                for (var i = 0; i < response.data.results.length; i++) {
                    self.maxLiftsObjects[i] = response.data.results[i];
                    self.maxLiftsObjects[i].created = moment(response.data.results[i].created).format("MMM Do YY, h:m a");
                    if (response.data.results[i].target_muscle === self.coreMuscles[1]) {
                        self.chestMax.push(response.data.results[i]);
                    }
                }



            }).catch(function (err) {
                console.log(err)
            })
        },
    }
</script>

<style scoped>

</style>