<template>
    <v-layout row wrap>
        <v-flex xs12 md4 :class="{'mb-4': $vuetify.breakpoint.smAndDown, 'ml-3': $vuetify.breakpoint.mdAndUp}">
            <v-card>
                 <v-layout >
                    <v-flex md10>
                        <v-card-title primary-title class="pl-0 pb-0">
                            <h3 class="headline mb-0 ml-2 pl-0">Max Lift Tracking</h3>

                        </v-card-title>
                        <span class="ml-2 grey--text">Core Muscle Groups Tracked</span>
                    </v-flex>
                            <v-flex md2 class="mt-4">
                                <v-btn icon @click="dialogSet()">
                                    <v-icon color="accent" large>add_circle</v-icon>
                                </v-btn>
                                <add-max-lift-tracking v-if="dialog"></add-max-lift-tracking>
                            </v-flex>
                </v-layout>

                <v-divider></v-divider>
                <v-layout wrap>
                    <v-flex class="ml-2"><p class="caption">Choose a target muscle; then search for an exercise.</p></v-flex>
                    <v-flex md4 offset-md1 offset-xs1 xs10>
                            <v-select class="mt-0 blue-grey--text text--darken-2"
                                      v-bind:items="target_muscles" v-model="selectedMuscle" label="Target Muscle"></v-select>
                    </v-flex>
                    <v-flex md6 offset-md1 offset-xs1 xs10>
                            <v-select class="mt-0 blue-grey--text text--darken-2"
                                      dense
                                      :disabled="disabled"
                                      :loading="eSelectLoading"
                                      item-text="exercise_name"
                                      item-value="exercise_name"
                                      autocomplete
                                      :search-input.sync="search"
                                      return-object
                                      :items="target_exercises"
                                      v-model="selectedExercise"
                                      label="Exercise"
                            ></v-select>
                    </v-flex>
                </v-layout>
                <v-layout class="ma-4" v-if="loading" v-model="computeLoading">
                        <v-flex offset-4 xs9>
                             <v-progress-circular  indeterminate v-bind:size="60" v-bind:width="5" color="primary"></v-progress-circular>
                        </v-flex>
                </v-layout>
                <v-layout class="ma-4" v-if="noResults == true">
                        <v-flex xs12>
                            <v-alert color="error" icon="info" value="true">
                                No data could be retrieved.
                            </v-alert>
                        </v-flex>
                </v-layout>
                <v-layout class="ma-1" v-if="!noResults && !loading">
                    <v-flex xs12>
                        <p class="title ml-3 blue-grey--text text--darken-3">Most Recent</p>
                    </v-flex>
                </v-layout>
                <render-max-data v-model="computeLoading" :max-lifts="getMaxLiftsObjects"></render-max-data>
            </v-card>
        </v-flex>
        <v-flex xs12 md6 offset-md1>
            <v-card class="mb-1 blue-grey lighten-5">
                <v-card-text>
                    <p class="subheading grey--text text--darken-3 text-center mb-1 pb-1">Progress Chart Options</p>
                    <v-layout row wrap justify-center>
                        <v-flex xs4>
                            <v-flex xs12>
                                <p class="grey--text text--darken-1 my-0 py-0 text-xs-center">Max Type:</p>
                            </v-flex>
                        </v-flex>
                        <v-flex xs12 md8>
                            <v-flex xs12 class="text-xs-center">
                                <v-radio-group :disabled="maxTypeRadioDisabled" v-model="maxTypeRadio" row class="py-0 my-0" @change="chartMaxType">
                                    <v-radio label="1 Rep Max" value="1" class="my-0"></v-radio>
                                    <v-radio label="3 Rep Max" value="3" class="my-0"></v-radio>
                                </v-radio-group>
                            </v-flex>
                        </v-flex>
                        <!--<v-flex xs4 style="border-right: 1px solid #4b5257">

                        </v-flex>
                        <v-flex xs4>

                        </v-flex>-->
                    </v-layout>
                </v-card-text>
            </v-card>
            <v-card class="pa-2">
                <v-alert outline color="warning" icon="warning" :value="noResults">
                        Chart Data not loaded. Please ensure you have recorded a Max for this target exercise.
                </v-alert>

                <max-progress-chart ref="liftProgressChart" :graphLabels="getGraphLabels"  :css-classes="cssClasses" :max-type="maxTypeRadio"
                                     :chart-data="getGraphData" :options="{responsive: true, maintainAspectRatio: false}"></max-progress-chart>

            </v-card>
        </v-flex>
        <v-flex xs12 md12>
            <v-divider></v-divider>
        </v-flex>
        <v-flex xs12 md10 offset-md1>
            <lifting-weight-tracking></lifting-weight-tracking>
        </v-flex>
    </v-layout>
</template>

<script>

    import {baseURLLocal} from '../../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'
    import MaxProgressChart from './max-progress-chart.vue'
    import RenderMaxData from './render-max-data.vue'
    import AddMaxLiftTracking from './add-max-lift-tracking.vue'
    import LiftingWeightTracking from './lifting-weight-tracking.vue'

    export default {
        name: "workout-stats",
        data () {
            return {
                maxTypeRadio: '3',
                loading: this.computeLoading,
                eSelectLoading: false,
                target_muscles: [

                              { text: 'Chest', value: "Chest"},
                              { text: 'Arms', value: "Arms"},
                              { text: 'Legs', value: "Legs"},
                              { text: 'Back', value: "Back"},
                              { text: 'Shoulders', value: 'Shoulders'},
                          ],
                defaultTargetExercise: [

                    { target_muscle: 'Chest', exercise_name: 'Bench Press'} , // chest

                ],
                target_exercises: [{ target_muscle: 'Chest', exercise_name: 'Bench Press'},],
                disabled: false,
                chestMax: [],
                selectedMuscle: null,
                dialog: this.$store.state.dialog,
                isLoading: false,
                graphLabels: this.$store.state.muscleHistoryGraphLabels,
                graphData: this.$store.state.muscleHistoryGraphData,
                max_type: '3',
                noResults: false,
                cssClasses: "",
                selectedExercise: [],
                search: null,

                maxTypeRadioDisabled: false,
            }
        },
        watch: {

            selectedMuscle (val) {

                this.disabled = !val;

            },

            search (val) {
              val && this.querySelections(val)
            },

            selectedExercise (queryVal) {

                this.loadingSet(true);
                this.setAndFetchMaxData(queryVal);
            },

            dialog: function () {
              this.dialog = this.$store.state.dialog;
            },

        },
        computed: {

            computeLoading () {

               this.loading =  this.$store.state.loading;

            },

            computeDialog () {

                this.dialog = this.$store.state.dialog;

            },
            getMaxLiftsObjects: function () {

                if (this.$store.state.recentTargetedMuscleExercises) {
                    this.cssClasses = '';
                    this.noResults = false;
                    return this.$store.state.recentTargetedMuscleExercises[0]
                }

                this.cssClasses = 'opacity';
                this.noResults = true;
                this.loadingSet(false);

            },
            getGraphLabels: function () {
                return this.$store.state.muscleHistoryGraphLabels;
            },
            getGraphData: function ()  {
                return this.$store.state.muscleHistoryGraphData
            },
        },
        methods: {
            chartMaxType(e) {
                let queryVal = this.selectedExercise;
                queryVal.maxType = this.maxTypeRadio;

                this.maxTypeRadioDisabled = true;
                this.setAndFetchMaxData(queryVal);



            },

            querySelections: _.debounce(function(v) {
                this.eSelectLoading = true;
                if (!this.selectedMuscle) { this.errorMessages = "Please choose target muscle before choosing an exercise. "}

                axios.get(baseURLLocal+'v1/exercises/?target_muscle='+this.selectedMuscle).then(response => {

                    this.target_exercises = response.data.results.filter(e => {
                        return (e || '').exercise_name.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.eSelectLoading = false;
                }).catch(err => {
                    console.log(err);
                    this.eSelectLoading = false;
                })

            },

                500

            ),

            dialogSet () {
              this.$store.commit('setDialog', !this.dialog);
              this.dialog = this.$store.state.dialog;
            },

            loadingSet (lStatus) {
                this.$store.commit('setLoading', lStatus);
                this.loading = this.$store.state.loading;
            },

            setAndFetchMaxData: function (queryVal) {

                this.selectedMuscle = queryVal.target_muscle;
                this.selectedExercise = queryVal;

                queryVal.maxType = this.maxTypeRadio;

                console.log('queryVal', queryVal);

                this.$store.dispatch('fetchGraphData', queryVal)
                    .then(() => {
                        this.graphLabels = this.$store.state.muscleHistoryGraphLabels;
                        this.graphData = this.$store.state.muscleHistoryGraphData;
                        this.maxTypeRadioDisabled = false;
                        //this.loadingSet(false);

                    }).catch((err) => {
                        //this.loadingSet(false);
                        this.maxTypeRadioDisabled = false;
                        console.log("Workout-stats.vue setAndFetch: fetchGraphData error:", err);
                    });

            },

        },
        mounted: function () {
            let queryVal = this.selectedExercise.length > 0 ? this.selectedExercise: this.target_exercises[0];
            queryVal.maxType = this.maxTypeRadio;

            this.loadingSet(true);
            this.setAndFetchMaxData(queryVal);

            //this.setAndFetchMaxData(this.target_exercises[0]);




        },
        components: { MaxProgressChart, RenderMaxData, AddMaxLiftTracking, LiftingWeightTracking },
    }
</script>

<style  scoped>

    .opacity {
        opacity: 0.4;
    }

</style>