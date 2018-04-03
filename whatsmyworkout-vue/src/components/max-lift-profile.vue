<template>
    <v-container class="pa-0">
        <v-layout row wrap>
            <v-flex xs12>
                <v-tabs icons-and-text fixed-tabs centered color="accent" dark v-model="active">
                       <v-tabs-slider color="white"></v-tabs-slider>
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
                               <v-layout row wrap justify-center>
                                   <v-flex xs12  >
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
                                       <v-card v-if="active == 'tab-1'" class="mt-2" >
                                           <v-card-title class="mb-0 pb-0">
                                               <span class="title grey--text text--darken-2">
                                                   {{ maxChest !== 'Not Recorded'? 'Current Max': 'No Data to Display.' }}</span>
                                           </v-card-title>
                                           <v-divider class="mt-2"></v-divider>
                                           <v-card-text class="ma-0 px-2 py-2">
                                               <v-layout row wrap justify-center>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Recorded</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">
                                                               {{ maxChest? ($options.filters.moment(maxChest.created)): 'No Data'}}</h6>
                                                       </v-flex>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Max Type</h6>
                                                            <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">3 Rep</h6>
                                                       </v-flex>

                                                        <v-flex xs4 text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Weight (lbs.)</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">
                                                               {{maxChest !== 'Not Recorded'? maxChest.weight: 'No Data' }}</h6>
                                                       </v-flex>
                                               </v-layout>
                                           </v-card-text>

                                       </v-card>
                                       <v-card v-if="active == 'tab-2'" color="blue-grey lighten-5">
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
                                       <v-card v-if="active == 'tab-2'" class="mt-2">
                                           <v-card-title class="mb-0 pb-0">
                                               <span class="headline grey--text text--darken-2">
                                                   {{ maxBack !== 'Not Recorded'? 'Current Max': 'No Data to Display.' }}</span>
                                           </v-card-title>
                                           <v-divider class="mt-1"></v-divider>
                                           <v-card-text class="ma-0 px-2 py-2">
                                               <v-layout row wrap justify-center>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Recorded</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">
                                                               {{ maxBack !== 'Not Recorded'? ($options.filters.moment(maxBack.created)): 'No Data'}}</h6>
                                                       </v-flex>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Max Type</h6>
                                                            <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">3 Rep</h6>
                                                       </v-flex>

                                                        <v-flex xs4 text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Weight (lbs.)</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">
                                                               {{ maxBack !== 'Not Recorded'? maxBack.weight: 'No Data' }}</h6>
                                                       </v-flex>
                                               </v-layout>
                                           </v-card-text>

                                       </v-card>
                                       <v-card v-if="active == 'tab-3'" color="blue-grey lighten-5">
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
                                       <v-card v-if="active == 'tab-3'" class="mt-2">
                                           <v-card-title class="mb-0 pb-0">
                                               <span class="headline grey--text text--darken-2">
                                                   {{ maxLegs !== 'Not Recorded'? 'Current Max': 'No Data to Display.' }}</span>
                                           </v-card-title>
                                           <v-divider class="mt-1"></v-divider>
                                           <v-card-text class="ma-0 px-2 py-2">
                                               <v-layout row wrap justify-center>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Recorded</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">
                                                               {{ maxLegs !== 'Not Recorded'? ($options.filters.moment(maxLegs.created)): 'No Data'}}</h6>
                                                       </v-flex>
                                                        <v-flex xs4 style="border-right: 1px solid teal" text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Max Type</h6>
                                                            <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">3 Rep</h6>
                                                       </v-flex>

                                                        <v-flex xs4 text-xs-center>
                                                           <h6 class="caption grey--text text--darken-2 mb-1">Weight (lbs.)</h6>
                                                           <h6 class="subheading grey--text text--darken-4 text-xs-center mb-0">
                                                               {{ maxLegs !== 'Not Recorded'? maxLegs.weight: 'No Data' }}</h6>
                                                       </v-flex>
                                               </v-layout>
                                           </v-card-text>

                                       </v-card>
                                   </v-flex>
                                   <v-flex xs12 >
                                       <v-card class="pa-2 mt-3">

                                           <max-lift-profile-chart
                                                   :css-classes="cssClasses"
                                                   :options="options"
                                                   :chart-data="getGraphData"
                                                   :graph-labels="getGraphLabels"
                                                   :exercise-name="queryExerciseName"></max-lift-profile-chart>

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
    import MaxLiftProfileChart from './max-lift-profile-chart.vue'

    export default {
        name: "max-lift-profile",
        components: {MaxLiftProfileChart, },
        data () {
            return {
                friendProfile: this.$store.state.data.profile_id,
                friendUsername: this.$route.params.username,

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

                data: [],
                labels: [],

                cssClasses: '',
                chartOptions: {

                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        mode: 'index',

                    },
                    title: {
                        text: '',
                        display: true,
                        fontSize: 24,
                        fontStyle: 'normal',
                        fontColor: '#424242',
                    },
                   scales: {
                        xAxes: [{
                            gridLines: {
                                display:false
                            }
                        }],
                        yAxes: [{
                            gridLines: {
                                display:false
                            }
                        }]
                    },


               },




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

            options: {
                get() {
                    this.chartOptions.title.text = this.active === 'tab-1'? 'Bench Press':
                        (this.active === 'tab-2')? 'Deadlifts': (this.active === 'tab-3')? 'Squats': 'None';
                    return this.chartOptions;
                },
                set(val) {

                    this.chartOptions = val;
                }
            },

            getGraphData: {
                get() {
                    return this.data
                },

                set(val) {
                   this.data = val;
                }


            },

            getGraphLabels: {
                get() {
                    return this.labels
                },
                set(val) {
                    this.labels = val;
                }
            },

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

                axios.all([this.getEarliest(), this.getLatest(), this.getMax(), this.fetchData()]).then(axios.spread(function (acct, perms) {

                })).catch(err => {
                    console.log(err)
                })
            }

        },
        methods: {

            getEarliest() {

                axios.get(baseURLLocal+ 'v1/max-lifts/?friend='+this.friendUsername+
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
                    this.friendUsername+'&latest=latest&exercise_name='+this.queryExerciseName+'&max_type=3')
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

                axios.get(baseURLLocal+ 'v1/max-lifts/?friend='+this.friendUsername+'&exercise_name='+this.queryExerciseName+
                    '&max_type=3&max=max').then(response => {

                        if (this.targetMuscle === 'Chest') {
                            this.maxChest = response.data.results.length > 0?
                                response.data.results[0]: {result: 'Not Recorded'};
                        }
                        else if (this.targetMuscle === 'Back') {
                            this.maxBack = response.data.results.length > 0?
                                response.data.results[0]: 'Not Recorded';
                        }

                        else if (this.targetMuscle === 'Legs') {
                            this.maxLegs = response.data.results.length > 0?
                                response.data.results[0]: 'Not Recorded';
                        }

                        console.log(response);
                }).catch(err => {
                        console.log(err);
                })


            },

            fetchData() {

                axios.get(baseURLLocal+ 'v1/max-lifts/?friend='+this.friendUsername+'&exercise_name='+this.queryExerciseName+
                    '&max_type=3').then(response => {

                        this.getGraphLabels = response.data.results.filter(obj => {
                            return obj.created = moment(obj.created).format("MMM Do YY");
                        }).map(obj => { return obj.created });


                        this.getGraphData = response.data.results.map(obj => { return obj.weight });


                        this.cssClasses = response.data.results.length < 1? 'opacity': '';



                        console.log(response);
                }).catch(err => {
                        console.log(err);
                })

            },

        },

        created() {

            axios.all([this.getEarliest(), this.getLatest(), this.fetchData(), this.getMax()]).then(axios.spread(function (acct, perms) {

            })).catch(err => {
                console.log(err);
            })





        }



    }
</script>

<style scoped>
    .opacity {
        opacity: 0.4;
    }

</style>