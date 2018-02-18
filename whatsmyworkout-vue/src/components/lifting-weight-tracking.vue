<template>
     <v-container  fluid grid-list-md>
         <v-layout row wrap>
             <v-flex xs12 md6>
                 <h3 class="headline text--primary">Track Exercises</h3>
             </v-flex>
             <v-flex xs12 offset-md2 md4>
                <v-text-field
                    append-icon="search"
                    v-model="search"
                >
                </v-text-field>
             </v-flex>
         </v-layout>
         <v-layout row wrap class="mt-3 mb-3">
                 <v-flex md2 xs10>
                 <p class="caption blue-grey--text">Filter & Sort</p>
                     </v-flex>
                <v-flex md2 xs2>
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
                        <v-icon right>send</v-icon>
                    </v-btn>

                </v-flex>
         </v-layout>
            <v-data-iterator
              content-tag="v-layout"
              :search="search"
              loading="primary"

              row
              wrap
              :no-data-text="noDataAvailable"
              :items="items"
              :rows-per-page-items="rowsPerPageItems"
              :pagination.sync="pagination"
            >
              <v-flex
                slot="item"
                slot-scope="props"
                xs12
                sm6
                md4
                lg3
              >
                <v-card>
                  <v-card-title class="pt-0 pb-0"><h6 class="title grey--text text--darken-3 mt-3 mb-2">{{ props.item.title }}</h6>
                      <span><v-icon class="pr-2">event</v-icon>{{ props.item.date_for_completion | moment }}</span>
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-list dense >
                    <v-list-tile>
                      <v-list-tile-content >Exercise:</v-list-tile-content>
                      <v-list-tile-content class="align-end" v-for="exercise in props.item.exercises">{{ exercise.exercise_name}}</v-list-tile-content>
                    </v-list-tile>

                  </v-list>
                </v-card>
              </v-flex>
            </v-data-iterator>
  </v-container>
</template>

<script>
    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'

    export default {
        name: "lifting-weight-tracking",
        data () {
            return {
                rowsPerPageItems: [4, 8, 12],
                pagination: {
                    rowsPerPage: 4
                },
                noDataAvailable: 'No Data Retrieved. Please create a workout and begin adding exercises to track.',
                loading: false,
                search: "",
              items: [

              ],
                enteredReps: null,
                selectedMuscle: null,
                selectedExercise: null,
                searchExercises: null,
                target_exercises: [],
                eSelectLoading: false,
                eSearchDisabled: true,
                btnDisabled: false,

            }
        },

        filters: {
          moment(date) {
              return moment(date).format("MMM Do YY");
          }
        },
        watch: {

            selectedMuscle (v) {

                this.eSearchDisabled = !v;
            },

            searchExercises(val) {

                val && this.querySelections(val)
            }

        },
        computed: {

        },
        methods: {

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
                let queryParamSelectedExercise = this.selectedExercise.exercise_name != null ? this.selectedExercise.exercise_name: '';


                axios.get(baseURLLocal + 'v1/workouts/?target_muscle='
                    +queryParamTargetMuscle+'&reps='+queryParamReps+'&exercise_name='+queryParamSelectedExercise).then(response => {
                    this.items = response.data.results;
                    this.loading = false;
                    this.btnDisabled = false;

                }).catch(err => {

                    this.btnDisabled = false;
                    console.log(err);


                })
            },

        },

        mounted: function () {
            this.loading = true;

            axios.get(baseURLLocal + 'v1/workouts/').then(response => {
                this.items = response.data.results;
                this.loading = false;

            }).catch(err => {


            })






        },


    }








</script>

<style>

    div.btn-height {
        height: auto!important;
    }



</style>