<template>
    <v-layout>
        <v-flex xs12 md4>
            <v-card>
                <v-card-title primary-title>
                    <h3 class="headline mb-0">Max Lift Tracking</h3>
                </v-card-title>
                <span class="ml-4 grey--text">Core Muscle Groups Tracked</span>
                <span class="caption grey--text text--lighten-1 mr-3 mt-3" style="font-style: italic; float: right;"></span>
                <v-divider></v-divider>
                <v-layout>
                    <v-flex md4 offset-1 xs10>
                            <v-select class="mt-0 blue-grey--text text--darken-2"
                                      v-bind:items="target_muscles" v-model="selectedMuscle" label="Choose Muscle"></v-select>
                    </v-flex>
                </v-layout>
                    <v-layout class="ma-4" v-if="maxLiftsObjects && !isLoading ">
                        <v-flex md6 xs12 class="pr-2" style="border-right: solid 1px black; text-align: right;">
                            <p class="blue-grey--text text--lighten-2">Exercise</p>
                            <p class="blue-grey--text text--lighten-2">Max Type</p>
                            <p class="blue-grey--text text--lighten-2">Weight</p>
                            <p class="blue-grey--text text--lighten-2">Recorded</p>

                        </v-flex>
                        <v-flex md6 xs12 class="pl-2" style="text-align: left;" >
                            <p class=" blue-grey--text">{{ maxLiftsObjects.exercise.exercise_name }}</p>
                            <p class=" blue-grey--text">{{ maxLiftsObjects.max_type }}</p>
                            <p class=" blue-grey--text">{{ maxLiftsObjects.weight }} lbs.</p>
                            <p class=" blue-grey--text">{{ maxLiftsObjects.created }}</p>
                        </v-flex>
                    </v-layout>
                    <v-layout class="ma-4" v-if="!maxLiftsObjects && !isLoading">
                        <v-flex xs12>
                            <v-alert color="info" icon="info" value="true">
                                Please record a Max with an exercise that targets this muscle.
                            </v-alert>
                        </v-flex>
                    </v-layout>
                    <v-layout class="ma-4" v-if="isLoading">
                        <v-flex offset-4 xs9>
                             <v-progress-circular indeterminate v-bind:size="60" v-bind:width="5" color="primary"></v-progress-circular>
                        </v-flex>
                    </v-layout>
            </v-card>
        </v-flex>
        <v-flex xs12 md6 offset-md1>
            <v-card class="pa-3">
                <lift-progress-chart :chart-data="datacollection" :height="400" :options="{responsive: true, maintainAspectRatio: false}"></lift-progress-chart>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>

    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'
    import LiftProgressChart from '../components/lift-progress-chart.vue'

    export default {
        name: "workout-stats",
        data () {
            return {
                datacollection: null,
                target_muscles: [

                              { text: 'Chest', value: "Chest"},
                              { text: 'Arms', value: "Arms"},
                              { text: 'Legs', value: "Legs"},
                              { text: 'Back', value: "Back"}
                          ],
                chestMax: [],
                selectedMuscle: null,
                isLoading: false,
                maxLiftsObjects: [],
                graphLabels: this.$store.state.muscleHistoryGraphLabels,
                graphData: this.$store.state.muscleHistoryGraphData,
            }
        },
        watch: {

            selectedMuscle: function (queryVal) {
                this.isLoading = true;
                let self = this;
                console.log(queryVal);


                axios.get(baseURLLocal+'v1/max-lifts/?target_muscle='+queryVal).then(function (response) {
                    self.isLoading = false;
                    self.maxLiftsObjects = response.data.results[0];
                    self.maxLiftsObjects.created = moment(response.data.results[0].created).format("MMM Do YY, h:m a");

                }).catch(function (err) {
                    console.log(err)
                })

            },

        },
        computed: {
            getGraphLabels: function () {
                return this.$store.state.muscleHistoryGraphLabels
            },

        },
        methods: {
            fillData: function () {
                console.log(this.chestMax);
                this.datacollection = {
                  labels: this.graphLabels.reverse(),
                  datasets: [
                    {
                      label: '3 Rep Max (lbs.)',
                      backgroundColor: '#90a4ae',
                      data: this.graphData.reverse()
                    }, /*{
                      label: 'Data One',
                      backgroundColor: '#f87979',
                      data: [this.getRandomInt(), this.getRandomInt()]
                    }*/
                  ]
                }
              },

        },
        created: function () {
            this.isLoading = true;
            let self = this;
            let queryVal = this.target_muscles[0].text;

            axios.get(baseURLLocal+'v1/max-lifts/?target_muscle='+queryVal).then(response => {
                self.isLoading = false;
                self.selectedMuscle = queryVal;
                self.maxLiftsObjects = response.data.results[0];
                self.maxLiftsObjects.created = moment(response.data.results[0].created).format("MMM Do YY, h:m a");
                //self.graphData = this.$store.state.muscleHistoryGraphData;

            }).catch(err => {
                console.log(err)
            })
        },
        mounted: function () {
            let queryVal = this.target_muscles[0].text;
            let self = this;
            this.$store.dispatch('fetchGraphLabels', queryVal).then(() => {
                self.graphLabels = this.$store.state.muscleHistoryGraphLabels;
                self.graphData = this.$store.state.muscleHistoryGraphData;

                self.fillData();
            }).catch(() => {

            });

        },
        components: { LiftProgressChart },
    }
</script>

<style  scoped>

</style>