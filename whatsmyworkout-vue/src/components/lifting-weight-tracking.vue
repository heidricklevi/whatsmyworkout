<template>
     <v-container  fluid grid-list-md>
         <v-layout row wrap>
             <v-flex xs12 md6>
                 <h3 class="headline text--primary">Track Exercises</h3>
                 <p class="subheading grey--text text--lighten-1 ml-1">Find your suggested lifting weight based on past exercises.</p>
             </v-flex>
         </v-layout>
         <v-layout row wrap class="mt-3 mb-3">
                 <v-flex md2 xs10>
                 <p class="caption blue-grey--text">Find & Narrow Results</p>
                     </v-flex>
                <v-flex md2 xs12>
                    <v-text-field
                        label="No. Reps"
                        v-model="enteredReps"
                        type="number"
                        light
                        persistent-hint
                        hint="Enter the number of reps to sort by"
                        ></v-text-field>
                </v-flex>
                <v-flex md2 xs12>
                    <v-select
                        label="Target Muscle"
                        v-model="selectedMuscle"
                        :items="['Arms', 'Chest', 'Back', 'Legs']"
                        ></v-select>

                </v-flex>
                <v-flex md4 xs12>
                    <v-select class="mt-0 blue-grey--text text--darken-2"
                        dense
                        :disabled="eSearchDisabled"
                        :loading="eSelectLoading"
                        item-text="exercise_name"
                        item-value="exercise_name"
                        autocomplete
                        :search-input.sync="searchExercises"
                        return-object
                        :items="target_exercises"
                        v-model="selectedExercise"
                        label="Exercise"
                    ></v-select>
                </v-flex>
                <v-flex md2 xs12>
                    <v-btn class="text-center" :disabled="btnDisabled" style="height: auto" color="accent" @click="fetchWorkoutData">

                        Search
                        <v-icon right>search</v-icon>
                    </v-btn>

                </v-flex>
         </v-layout>
         <v-layout row wrap>
             <v-flex md6 xs12>
                     <v-tabs icons-and-text centered dark color="accent">
                        <v-tabs-slider color="white"></v-tabs-slider>
                        <!--<v-tab href="#tab-1">
                          Recents
                          <v-icon>phone</v-icon>
                        </v-tab>
                        <v-tab href="#tab-2">
                          Favorites
                          <v-icon>favorite</v-icon>
                        </v-tab>-->
                        <v-tab href="#tab-3">
                          Exercise History
                          <v-icon>history</v-icon>
                        </v-tab>
                        <v-tab-item
                          v-for="i in 3"
                          :key="i"
                          :id="'tab-' + i"
                          class="mt-2"
                        >
                            <v-flex md12 class="mb-2">
                                <v-card color="blue-grey lighten-5">
                                    <v-card-text class="pt-1 pb-1">
                                        <p class="grey--text text--darken-3 text-center mb-0 pb-0">Results</p>
                                        <v-layout>
                                            <v-flex md4 xs4 class="text-md-center text-xs-left grey--text text--darken-2 caption">
                                                Exercise | <span class="grey--text text--darken-4">{{ resultTextExercise  }}</span>
                                            </v-flex>
                                            <v-flex md4 xs4 class="text-md-center text-xs-center grey--text text--darken-2 caption">
                                                Target Muscle | <span class="grey--text text--darken-4">{{ resultTextTargetMuscle }}</span>
                                            </v-flex>
                                            <v-flex md4 xs4 class="text-md-center text-xs-right grey--text text--darken-2 caption">
                                                # Reps | <span class="grey--text text--darken-4"> {{ resultTextReps }}</span>
                                            </v-flex>
                                        </v-layout>
                                    </v-card-text>

                                </v-card>
                            </v-flex>
                          <v-data-iterator
                                  content-tag="v-layout"
                                  :search="search"
                                  loading="primary"

                                  row
                                  wrap
                                  :no-data-text="noDataAvailable"
                                  :items="exerciseData"
                                  :rows-per-page-items="rowsPerPageItems"
                                  :pagination.sync="pagination"
                                >
                                      <v-flex
                                        slot="item"
                                        slot-scope="props"
                                        xs12
                                        md6
                                        >
                                        <v-card>
                                          <v-card-title class="pt-0 pb-0"><h6 class="subheading grey--text text--darken-3 mt-3 mb-2">{{ props.item.exercise_name}}</h6>
                                              <span class="caption pr-2"><v-icon class="pr-2" small>event</v-icon>{{ props.item.created | moment }}</span>
                                              |
                                              <span class="caption pl-2 pr-2">
                                                  <img style="height: 16px; width: 16px;" src="../assets/img/muscle.png">
                                                  {{ props.item.target_muscle }} </span>
                                          </v-card-title>
                                          <v-divider></v-divider>
                                              <v-list dense  >
                                                        <v-list-tile >
                                                            <v-list-tile-content >Weight</v-list-tile-content>
                                                            <v-list-tile-content class="align-end" >
                                                              {{ props.item.lifting_weight }} lbs.</v-list-tile-content>
                                                        </v-list-tile>
                                                        <v-list-tile >
                                                            <v-list-tile-content >Reps</v-list-tile-content>
                                                            <v-list-tile-content class="align-end" >
                                                              {{ props.item.reps }}</v-list-tile-content>
                                                        </v-list-tile>
                                                </v-list-tile>

<!--                    <v-list-group v-for="exercise in props.item.exercises" >
                        <v-list-tile v-if="!selectedExercise || (exercise.exercise_name == selectedExercise.exercise_name)">
                              <v-list-tile-content >Exercise:</v-list-tile-content>
                              <v-list-tile-content class="align-end">{{ exercise.exercise_name}}</v-list-tile-content>
                            </v-list-tile>
                            <v-list-tile v-if="!selectedExercise || exercise.exercise_name == selectedExercise.exercise_name">
                                <v-list-tile-content >Weight</v-list-tile-content>
                                <v-list-tile-content class="align-end" >
                                  {{ exercise.lifting_weight }}lbs</v-list-tile-content>
                            </v-list-tile>
                            <v-list-tile v-if="!selectedExercise || exercise.exercise_name == selectedExercise.exercise_name">
                                <v-list-tile-content >Reps</v-list-tile-content>
                                <v-list-tile-content class="align-end" >
                                  {{ exercise.reps }}</v-list-tile-content>
                            </v-list-tile>
                    </v-list-group>-->
                                  </v-list>
                                </v-card>
                              </v-flex>
                            </v-data-iterator>

                        </v-tab-item>
                      </v-tabs>
                </v-flex>
             <v-flex xs12 md6>
                 <v-card class="pa-2">
                         <lifting-weight-chart
                                 ref="liftProgressChart"
                                 :graphLabels="getGraphLabels"
                                 :rep-data="getRepData"
                                 :exercise-data="exerciseData"
                                 :chart-data="getGraphData"
                         ></lifting-weight-chart>
                 </v-card>
             </v-flex>

         </v-layout>

  </v-container>
</template>

<script>
    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'
    import LiftingWeightChart from '../components/lifting-weight-chart.vue'

    export default {
        name: "lifting-weight-tracking",
        data () {
            return {
                rowsPerPageItems: [2, 4, 6],
                pagination: {
                    rowsPerPage: 2
                },
                noDataAvailable: 'No Data Retrieved.',
                loading: false,
                search: "",
              items: [

              ],
                graphData: [],
                graphLabels: [],
                repData: [],
                exerciseData: [],

                enteredReps: null,
                selectedMuscle: null,
                selectedExercise: null,
                searchExercises: null,
                target_exercises: [],
                eSelectLoading: false,
                eSearchDisabled: true,
                btnDisabled: false,

                chartOptions: this.getChartOptions,


                resultTextExercise: 'All',
                resultTextReps: 'Not Filtered',
                resultTextTargetMuscle: 'Not Filtered',

            }
        },

        filters: {
          moment(date) {
              return moment(date).format("MMM Do YY");
          }
        },
        watch: {

            exerciseData () {

                return this.exerciseData;

            },

            selectedMuscle (v) {

                this.eSearchDisabled = !v;
            },

            searchExercises(val) {

                val && this.querySelections(val)
            }

        },
        computed: {


            getGraphLabels: function () {
                return this.graphLabels;
            },

            getGraphData: function () {
                return this.graphData;
            },

            getRepData: function () {

                return this.repData;
            },

        },
        methods: {

            getChartOptions: function () {

                return {




                }

            },

            sortResults() {



            },

            querySelections (v) {
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

            fetchWorkoutData() {
                this.loading = true;
                this.btnDisabled = true;

                let queryParamReps = this.enteredReps != null ? this.enteredReps: '';
                let queryParamTargetMuscle = this.selectedMuscle != null ? this.selectedMuscle: '';
                let queryParamSelectedExercise = this.selectedExercise != null ? this.selectedExercise.exercise_name: '';


                let temp = [];
                let dataTemp = [];
                let reps = [];

                axios.get(baseURLLocal + 'v1/exercise/?target_muscle='
                    +queryParamTargetMuscle+'&reps='+queryParamReps+'&exercise_name='+queryParamSelectedExercise).then(response => {
                    let results = response.data.results;

                    for (let i = 0; i < results.length; i++) {
                        temp[i] = moment(results[i].created).format("MMM Do YY");
                        dataTemp[i] = results[i].lifting_weight !== null? results[i].lifting_weight: 0;
                        reps[i] = results[i].reps;

                    }

                    this.exerciseData = results;
                    //this.exerciseData.push(reps);

                    this.graphData = dataTemp;
                    this.graphLabels = temp;
                    this.repData = reps;

                    this.loading = false;
                    this.btnDisabled = false;

                    this.resultTextExercise = this.selectedExercise? this.selectedExercise.exercise_name: 'All';
                    this.resultTextReps = this.enteredReps? this.enteredReps: 'Not Filtered';
                    this.resultTextTargetMuscle = this.selectedMuscle? this.selectedMuscle: 'Not Filtered';




                }).catch(err => {

                    this.btnDisabled = false;
                    console.log(err);


                })
            },

        },

        mounted: function () {
            this.fetchWorkoutData();
        },
        components: { LiftingWeightChart, }


    }








</script>

<style>
    .opacity {
        opacity: 0.4;
    }
    div.btn-height {
        height: auto!important;
    }



</style>