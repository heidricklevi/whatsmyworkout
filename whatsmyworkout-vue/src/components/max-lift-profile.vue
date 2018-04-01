<template>
    <v-container>
        <v-layout row wrap>
            <v-flex xs12>
                <v-tabs icons-and-text fixed-tabs centered color="grey lighten-4" v-model="active">
                       <v-tabs-slider color="primary darken-3"></v-tabs-slider>
                       <v-tab href="#tab-1">
                            Chest
                        </v-tab>
                        <v-tab href="#tab-2">
                            Back
                        </v-tab>

                        <v-tab href="#tab-3">
                            Legs
                        </v-tab>

                       <v-tab-item
                          v-for="i in 3"
                          :key="i"
                          :id="'tab-' + i"
                          >

                           <v-container>
                               <v-layout row wrap>
                                   <v-flex xs12 md6>
                                       <v-card v-if="active == 'tab-1'" color="blue-grey lighten-5">
                                           <v-card-text class="ma-0 pa-2">
                                               <v-layout row wrap>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-2 mb-1 caption"><em>Exercise</em></h6>
                                                        <h6 class="grey--text text--darken-3">Bench Press</h6>
                                                   </v-flex>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>Recent Attempt</em></h6>
                                                        <h6 class="grey--text text--darken-3">{{ latestChest? latestChest: 'None' }}</h6>
                                                   </v-flex>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>First Attempt</em></h6>
                                                        <h6 class="grey--text text--darken-3">{{ earliestChest? earliestChest: 'None' }}</h6>
                                                   </v-flex>

                                                </v-layout>

                                           </v-card-text>


                                       </v-card>
                                       <v-card v-if="active == 'tab-1'" class="mt-2">
                                           <v-card-title class="mb-0 pb-0">
                                               <span class="headline grey--text text--darken-3">Current Max</span>
                                           </v-card-title>
                                           <v-divider class="mt-1"></v-divider>
                                           <v-card-text class="ma-0 px-2 py-2">
                                               <v-layout row wrap justify-center>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Recorded</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">{{ maxChest.created | moment}}</h6>
                                                       </v-flex>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Max Type</h6>
                                                            <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">3 Rep</h6>
                                                       </v-flex>

                                                        <v-flex xs4 text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Weight (lbs.)</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">{{ maxChest.weight }}</h6>
                                                       </v-flex>
                                               </v-layout>
                                           </v-card-text>

                                       </v-card>
                                       <v-card v-if="active == 'tab-2'">
                                           <v-card-text>
                                               <v-layout row wrap>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>Exercise</em></h6>
                                                        <h6 class="grey--text text--darken-3">Deadlift</h6>
                                                   </v-flex>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>Recent Recording</em></h6>
                                                        <h6 class="grey--text text--darken-3">{{ latestBack? latestBack: 'None' }}</h6>
                                                   </v-flex>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>First Recorded</em></h6>
                                                        <h6 class="grey--text text--darken-3">{{ earliestBack? earliestBack: 'None' }}</h6>
                                                   </v-flex>

                                                </v-layout>

                                           </v-card-text>


                                       </v-card>
                                       <v-card v-if="active == 'tab-3'">
                                           <v-card-text>
                                               <v-layout row wrap>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>Exercise</em></h6>
                                                        <h6 class="grey--text text--darken-3">Squat</h6>
                                                   </v-flex>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>Recent Recording</em></h6>
                                                        <h6 class="grey--text text--darken-3">{{ latestLegs? latestLegs: 'None' }}</h6>
                                                   </v-flex>
                                                   <v-flex xs4 text-xs-center>
                                                        <h6 class="grey--text text--darken-1 mb-1 caption"><em>First Recorded</em></h6>
                                                        <h6 class="grey--text text--darken-3">{{ earliestLegs? earliestLegs: 'None' }}</h6>
                                                   </v-flex>

                                                </v-layout>

                                           </v-card-text>


                                       </v-card>
                                   </v-flex>
                               </v-layout>
                           </v-container>
                       </v-tab-item>


                </v-tabs>
            </v-flex>







        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import { baseURLLocal} from '../auth/auth-utils'
    export default {
        name: "max-lift-profile",
        data () {
            return {
                friendProfile: this.$store.state.data.profile_id,
                friendUsername: this.$store.state.data.username,

                active: null,

                earliestChest: '',
                latestChest: '',

                earliestBack: '',
                latestBack: '',

                earliestLegs: '',
                latestLegs: '',

                maxChest: {},
                maxBack: {},
                maxLegs: {},



                muscle: 'Chest',
                exercise: 'Bench Press',



            }
        },
        filters: {
            moment(date) {
                return moment(date).format("MMM Do YY");
            }
        },
        computed:{

            queryExerciseName: {
                get() {
                    return this.exercise
                },
                set() {

                    this.exercise = this.active === 'tab-1'? 'Bench Press':
                        (this.active === 'tab-2')? 'Deadlifts': (this.active === 'tab-3')? 'Squats': 'None'

                }
            },

            targetMuscle: {
                get() {
                    return this.muscle;
                },

                set() {
                    this.muscle = this.active === 'tab-1'? 'Chest':
                        (this.active === 'tab-2')? 'Back': (this.active === 'tab-3')? 'Legs': 'None'
                }
            }

        },
        watch: {

            active() {

                this.targetMuscle = this.active;
                this.queryExerciseName = this.active;

                axios.all([this.getEarliest(), this.getLatest(), this.getMax()]).then(axios.spread(function (acct, perms) {

                })).catch(err => {
                    console.log(err)
                })
            }

        },
        methods: {

            getEarliest() {

                axios.get(baseURLLocal+ 'v1/max-lifts/?friend='+this.friendProfile+
                    '&earliest=earliest&exercise_name='+this.queryExerciseName+'&max_type=3')
                    .then(response => {
                        if (this.targetMuscle === 'Chest') {
                            this.earliestChest = response.data.results.length > 0?
                                moment(response.data.results[0].created).format("MMM Do YY"): 'Not Recorded';
                        }
                        else if (this.targetMuscle === 'Back') {
                            this.earliestBack = response.data.results.length > 0?
                                moment(response.data.results[0].created).format("MMM Do YY"): 'Not Recorded';
                        }

                        else if (this.targetMuscle === 'Legs') {
                            this.earliestLegs = response.data.results.length > 0?
                                moment(response.data.results[0].created).format("MMM Do YY"): 'Not Recorded';
                        }
                        console.log(response)
                    }).catch(err => {
                        console.log(err)
                })

            },

            getLatest() {

                axios.get(baseURLLocal+ 'v1/max-lifts/?friend='+
                    this.friendProfile+'&latest=latest&exercise_name='+this.queryExerciseName+'&max_type=3')
                    .then(response => {

                        if (this.targetMuscle === 'Chest') {
                            this.latestChest = response.data.results.length > 0?
                                moment(response.data.results[0].created).format("MMM Do YY"): 'Not Recorded';
                        }
                        else if (this.targetMuscle === 'Back') {
                            this.latestBack = response.data.results.length > 0?
                                moment(response.data.results[0].created).format("MMM Do YY"): 'Not Recorded';
                        }

                        else if (this.targetMuscle === 'Legs') {
                            this.latestLegs = response.data.results.length > 0?
                                moment(response.data.results[0].created).format("MMM Do YY"): 'Not Recorded';
                        }

                        console.log(response)
                    }).catch(err => {
                        console.log(err)
                })

            },

            getMax() {

                axios.get(baseURLLocal+ 'v1/max-lifts/?friend='+this.friendProfile+'&exercise_name='+this.queryExerciseName+
                    '&max_type=3&max=max').then(response => {
                        this.maxChest = response.data.results[0];
                        console.log(response);
                }).catch(err => {
                        console.log(err);
                })


            },

        },

        created() {

            axios.all([this.getEarliest(), this.getLatest()]).then(axios.spread(function (acct, perms) {

            })).catch(err => {
                console.log(err);
            })





        }



    }
</script>

<style scoped>

</style>