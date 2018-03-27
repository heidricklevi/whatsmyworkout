<template>
    <v-list-tile >


        <v-layout row wrap >

                                                      <v-flex md3 offset-md1 xs8 v-if="getEditExercise" class="hidden-sm-and-down">
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
                                                                :disabled="exerciseSearchDisabled"
                                                                >

                                                            </v-select>
                                                      </v-flex>
                                                      <v-flex v-if="!getEditExercise" xs8 offset-md1 md5 text-xs-left class="pl-2 hidden-md-and-up mt-2">
                                                          <span class="grey--text text--darken-4">{{ index+1 }}. {{ selectedExercise? selectedExercise.exercise_name: cExercise.exercise_name }}</span>
                                                      </v-flex>
                                                      <v-flex v-if="!getEditExercise" xs8 offset-md1 md5 text-xs-left class="pl-2 hidden-sm-and-down">
                                                          <span class="grey--text text--darken-4">{{ index+1 }}. {{ selectedExercise? selectedExercise.exercise_name: cExercise.exercise_name }}</span>
                                                      </v-flex>


                                                  <v-list-tile-content class="align-end grey--text text--darken-1 hidden-sm-and-down" v-if="!getEditExercise">
                                                      {{ sets? sets: cExercise.sets }} x {{ reps? reps: cExercise.reps }}
                                                  <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="!getEditExercise">

                                                      @ {{ workingWeight? workingWeight: cExercise.lifting_weight }} lbs.
                                                  </v-list-tile-content>
                                                  </v-list-tile-content>
                                                    <v-layout flex class="hidden-md-and-up pr-2 mt-2" wrap justify-center>
                                                        <v-flex xs12 text-xs-right v-if="!getEditExercise">
                                                            <span class="grey--text text--darken-1">
                                                                {{ sets? sets: cExercise.sets }} x {{ reps? reps: cExercise.reps }}</span>
                                                        </v-flex>
                                                        <v-flex xs12 text-xs-right v-if="!getEditExercise">
                                                            <span class="caption grey--text text--lighten-1">
                                                                @ {{ workingWeight? workingWeight: cExercise.lifting_weight }} lbs.</span>
                                                        </v-flex>
                                                    </v-layout>
                                                    <v-flex
                                                            xs2
                                                            md1
                                                            offset-md1
                                                            v-if="getEditExercise"
                                                            >
                                                          <v-text-field
                                                              label="Sets"
                                                              type="number"
                                                              v-model="cExercise.sets"
                                                              hint="# of sets">

                                                          </v-text-field>

                                                      </v-flex>
                                                      <v-flex xs3 offset-xs1 md1 text-xs-right class="ml-1" v-if="getEditExercise">
                                                          <v-text-field
                                                              label="Reps"
                                                              type="number"
                                                              v-model="cExercise.reps"
                                                              hint="# of reps">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex xs3 md2 offset-xs1 text-xs-right offset-md1 align-end v-if="getEditExercise">
                                                          <v-text-field
                                                              label="Weight"
                                                              type="number"
                                                              suffix="lbs."
                                                              v-model="cExercise.lifting_weight"
                                                              hint="Total weight lifted per rep">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex md2 xs4 offset-xs1 v-if="!getEditExercise" text-xs-left class="hidden-sm-and-down">
                                                            <v-btn icon class="align-end pa-0 ma-0"   @click="copiedExerciseEdit(cExercise)">
                                                                <v-icon color="primary lighten-3">edit</v-icon>
                                                            </v-btn>
                                                            <v-btn icon absolute  class="align-end pa-0 ma-0" @click="removeExercise(cExercise)">
                                                                <v-icon color="error">remove_circle</v-icon>
                                                            </v-btn>
                                                      </v-flex>
                                                      <v-flex md1 xs3  v-if="getEditExercise" text-xs-right class="hidden-sm-and-down">
                                                            <v-btn icon class="align-end" absolute style="right: 50px; " @click="saveExerciseEdit(cExercise)">
                                                                <v-icon color="accent">check_circle</v-icon>
                                                            </v-btn>
                                                            <v-btn icon absolute  class="align-end" @click="editExercise = false" v-if="!newExerciseToggle">
                                                                <v-icon color="error">cancel</v-icon>
                                                            </v-btn>
                                                      </v-flex>
                                                      <v-flex md2 xs4   v-if="!getEditExercise" text-xs-right class="hidden-md-and-up">
                                                            <v-btn icon absolute  right class="text-xs-right pa-0 ma-1 bottom" style="right: 50px;"     @click="copiedExerciseEdit(cExercise)">
                                                                <v-icon color="primary lighten-3">edit</v-icon>
                                                            </v-btn>
                                                            <v-btn icon absolute  right  class="align-end pa-0 ma-1" @click="removeExercise(cExercise)">
                                                                <v-icon color="error">remove_circle</v-icon>
                                                            </v-btn>
                                                      </v-flex>
                                                      <!--<v-flex md1 xs4   v-if="getEditExercise" text-xs-right class="hidden-md-and-up">
                                                            <v-btn icon class="align-end pa-0 ma-0"   style="" @click="saveExerciseEdit(cExercise)">
                                                                <v-icon color="accent">check_circle</v-icon>
                                                            </v-btn>
                                                            <v-btn icon   class="pa-0 ma-0" @click="editExercise = false" v-if="!newExerciseToggle">
                                                                <v-icon color="error">cancel</v-icon>
                                                            </v-btn>
                                                      </v-flex>-->

                                            <v-layout row wrap justify-center class="hidden-md-and-up">
                                                    <v-dialog
                                                            v-model="mobileEditExerciseDialog"
                                                            fullscreen
                                                            transition="dialog-bottom-transition"
                                                            :overlay="false"
                                                            class="hidden-md-and-up">
                                                      <v-card>
                                                        <v-toolbar dark color="primary">
                                                          <v-btn icon @click.native="editExercise = false" dark>
                                                            <v-icon>close</v-icon>
                                                          </v-btn>
                                                          <v-toolbar-title>Edit Exercise</v-toolbar-title>
                                                          <v-spacer></v-spacer>
                                                          <v-toolbar-items>
                                                            <v-btn dark flat @click.native="saveExerciseEdit(cExercise)">Save</v-btn>
                                                          </v-toolbar-items>
                                                        </v-toolbar>
                                                        <v-layout row wrap>
                                                          <v-flex md3 offset-md1 xs10 offset-xs1>
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
                                                                :disabled="exerciseSearchDisabled"
                                                                >

                                                            </v-select>
                                                      </v-flex>
                                                          <v-flex
                                                            xs4 offset-xs1
                                                            md1
                                                            offset-md1
                                                            v-if="getEditExercise"
                                                            >
                                                          <v-text-field
                                                              label="Sets"
                                                              type="number"
                                                              v-model="cExercise.sets"
                                                              hint="# of sets">

                                                          </v-text-field>

                                                      </v-flex>
                                                      <v-flex xs4 offset-xs2 md1 text-xs-right>
                                                          <v-text-field
                                                              label="Reps"
                                                              type="number"
                                                              v-model="cExercise.reps"
                                                              hint="# of reps">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex xs3 offset-xs1 md2 offset-xs1 text-xs-right offset-md1 align-end>
                                                          <v-text-field
                                                              label="Weight"
                                                              type="number"
                                                              suffix="lbs."
                                                              v-model="cExercise.lifting_weight"
                                                              hint="Total weight lifted per rep">

                                                          </v-text-field>

                                                      </v-flex>
                                                            </v-layout>

                                                      </v-card>
                                                    </v-dialog>
                                                  </v-layout>

</v-layout>

                                                </v-list-tile>


</template>

<script>
    import { baseURLLocal } from "../auth/auth-utils";
    import axios from 'axios';


    export default {
        name: "edit-copied-exercises",
        props: ['cExercise', 'index', 'editExercise', 'targetMuscle', 'copiedWorkout'],
        data () {
            return {

                sbColor: '',
                sbModel: false,
                sbText: '',

                target_exercise: [],
                eSearchDisabled: false,
                eSelectLoading: false,
                selectedExercise: null,
                searchExercises: null,
                exerciseSearchDisabled: false,

                sets: null,
                reps: null,
                workingWeight: null,

                localExercises: [],
                newExerciseToggle: this.$store.state.friendProfile.addNewExerciseToggle,

                eTargetMuscle: this.targetMuscle,

                targetMuscles: [
                    { text: 'Chest', value: "Chest"},
                  //{ text: 'Biceps', value: "Biceps"},
                  { text: 'Abs', value: "Abs"},
                  //{ text: 'Triceps', value: "Triceps"},
                  { text: 'Back', value: 'Back'},
                  { text: 'Legs', value: 'Legs'},
                  { text: 'Arms', value: 'Arms'},
                ],


            }
        },
        computed: {

            mobileEditExerciseDialog: {
                get: function () {
                    if (this.$vuetify.breakpoint.mdAndUp) return false;

                    return this.editExercise
                },
                set: function (val) {
                    this.editExercise = val;
                }
            },

            workoutToEdit () {
                let arr = [];

                arr.push(this.copiedWorkout);
                return arr
            },
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

            eTargetMuscle() {

                this.exerciseSearchDisabled = !this.eTargetMuscle
            },
            searchExercises(val) {

                val && this.querySelections(val)
            },
        },
        methods: {

            removeExercise(exerciseToDelete) {
                let exercises = this.workoutToEdit[0].exercises;

                if (this.workoutToEdit[0].isCopiedFromFriend || !exerciseToDelete.id) {
                    exercises = exercises.filter(exercise => exercise !== exerciseToDelete);
                    this.workoutToEdit[0].exercises = exercises;

                    return
                }

                this.deleteExercise(exerciseToDelete);
            },

            deleteExercise(toDelete) {

                let exercises = this.workoutToEdit[0].exercises;

                axios.delete(baseURLLocal+ 'v1/exercise/'+toDelete.id+'/', { params: { id: toDelete.id } } ).then(response => {

                    exercises = exercises.filter(exercise => exercise !== toDelete);
                    this.workoutToEdit[0].exercises = exercises;
                    this.$store.commit('setData', this.workoutToEdit);
                    console.log(response)


                    this.sbModel = true;
                    this.sbText = response.data;
                    this.sbColor = 'success';
                }).catch(err => {


                    this.sbModel = true;
                    this.sbText = err.message;
                    this.sbColor = 'error';
                    console.log(err)
                })

            },
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
                this.$store.commit('setNewExerciseToggle', false);
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