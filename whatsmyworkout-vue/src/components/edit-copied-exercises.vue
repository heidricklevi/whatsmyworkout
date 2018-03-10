<template>
    <v-list-tile >
                                                      <v-flex md4 offset-md1 xs12 v-if="getEditExercise">
                                                          <v-select
                                                                dense

                                                                :readonly="eSearchDisabled"
                                                                :loading="eSelectLoading"
                                                                item-text="exercise_name"
                                                                item-value="exercise_name"
                                                                autocomplete
                                                                :search-input.sync="searchExercises"
                                                                return-object
                                                                :items="target_exercise"
                                                                v-model="selectedExercise"
                                                                label="Exercise"
                                                                :value="cExercise.exercise_name"
                                                                >

                                                            </v-select>
                                                      </v-flex>
                                                      <v-flex v-if="!getEditExercise" xs12 offset-md1 md5>
                                                          {{ index+1 }}. {{ selectedExercise? selectedExercise.exercise_name: cExercise.exercise_name }}
                                                      </v-flex>


                                                  <v-list-tile-content class="align-end grey--text text--darken-1" v-if="!getEditExercise">
                                                      {{ sets? sets: cExercise.sets }} x {{ reps? reps: cExercise.reps }}
                                                  <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="!getEditExercise">

                                                      @ {{ workingWeight? workingWeight: cExercise.lifting_weight }} lbs.
                                                  </v-list-tile-content>
                                                  </v-list-tile-content>
                                                    <v-flex xs5 md1 offset-md1 v-if="getEditExercise">
                                                          <v-text-field
                                                              label="Sets"
                                                              type="number"
                                                              v-model="cExercise.sets"
                                                              class="body"
                                                              hint="# of sets">

                                                          </v-text-field>

                                                      </v-flex>
                                                      <v-flex xs5 md1 class="ml-1" v-if="getEditExercise">
                                                          <v-text-field
                                                              label="Reps"
                                                              type="number"
                                                              v-model="cExercise.reps"
                                                              hint="# of reps">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex xs6 md2 offset-md1 align-end v-if="getEditExercise">
                                                          <v-text-field
                                                              label="Weight"
                                                              type="number"
                                                              suffix="lbs."
                                                              v-model="cExercise.lifting_weight"
                                                              hint="Total weight lifted per rep">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex md1 xs3 v-if="!getEditExercise" text-xs-right>
                                                            <v-btn icon class="align-end" @click="copiedExerciseEdit(cExercise)">
                                                                <v-icon color="primary lighten-3">edit</v-icon>
                                                            </v-btn>
                                                      </v-flex>
                                                      <v-flex md1 xs3 v-if="getEditExercise" text-xs-right>
                                                            <v-btn icon class="align-end" @click="saveExerciseEdit(cExercise)">
                                                                <v-icon color="accent">check</v-icon>
                                                            </v-btn>
                                                      </v-flex>


                                                </v-list-tile>


</template>

<script>
    import { baseURLLocal } from "../auth/auth-utils";
    import axios from 'axios';


    export default {
        name: "edit-copied-exercises",
        props: ['cExercise', 'index', 'editExercise', 'targetMuscle'],
        data () {
            return {
                target_exercise: [],
                eSearchDisabled: false,
                eSelectLoading: false,
                selectedExercise: null,
                searchExercises: null,
                exerciseDisabled: false,

                sets: null,
                reps: null,
                workingWeight: null,

                localExercises: [],

            }
        },
        computed: {
            getEditExercise: {
                get() {
                    return this.editExercise;
                },
                set(val) {
                    this.editExercise = !this.editExercise;
                    this.cExercise.editExercise = !this.cExercise.editExercise;
                }

            }
        },
        watch: {
            searchExercises(val) {

                val && this.querySelections(val)
            },
        },
        methods: {
            querySelections (v) {
                this.eSelectLoading = true;
                //if (!this.target_muscle) { this.errorMessages = "Please choose target muscle before choosing an exercise. "}

                axios.get(baseURLLocal+'v1/exercises/?target_muscle='+this.targetMuscle).then(response => {

                    this.target_exercise = response.data.results.filter(e => {
                        return (e || '').exercise_name.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.eSelectLoading = false;
                }).catch(err => {
                    console.log(err);
                    this.eSelectLoading = false;
                })

            },
            saveExerciseEdit(exercise) {
                this.getEditExercise = !this.getEditExercise;
                exercise.exercises = this.selectedExercise;
                exercise.exercise_name = this.selectedExercise.exercise_name;




            },
            copiedExerciseEdit(exercise) {
                this.getEditExercise = !this.getEditExercise;
            },
        },
        mounted () {

        },
    }
</script>

<style scoped>

</style>