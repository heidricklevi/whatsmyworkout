<template>
    <v-list-tile class="pt-4">


        <v-layout row wrap >

                                                      <v-flex md3 offset-md1 xs8 v-if="getEditExercise && $vuetify.breakpoint.mdAndUp" class="hidden-sm-and-down">
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

                                                                :rules="[rules.required]"
                                                                :disabled="exerciseSearchDisabled"
                                                                ref="selectedExercise"
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
                                                    <!--<v-form ref="editExerciseForm" v-model="exerciseValid">-->
                                                    <v-flex
                                                            xs2
                                                            md1
                                                            offset-md1
                                                            v-if="getEditExercise && $vuetify.breakpoint.mdAndUp"
                                                            >
                                                          <v-text-field
                                                              label="Sets"
                                                              type="number"
                                                              v-model="sets"
                                                              :rules="[rules.required, rules.validSets]"
                                                              ref="sets"
                                                              hint="# of sets">

                                                          </v-text-field>

                                                      </v-flex>
                                                      <v-flex xs3 offset-xs1 md1 text-xs-right class="ml-1" v-if="getEditExercise && $vuetify.breakpoint.mdAndUp">
                                                          <v-text-field
                                                              label="Reps"
                                                              type="number"
                                                              v-model="reps"
                                                              ref="reps"
                                                              :rules="[rules.required, rules.validReps]"
                                                              hint="# of reps">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex xs3 md2 offset-xs1 text-xs-right offset-md1 align-end v-if="getEditExercise && $vuetify.breakpoint.mdAndUp">
                                                          <v-text-field
                                                              label="Weight"
                                                              type="number"
                                                              suffix="lbs."
                                                              ref="workingWeight"
                                                              v-model="workingWeight"
                                                              :rules="[rules.validLW]"
                                                              hint="Total weight lifted per rep">

                                                          </v-text-field>

                                                      </v-flex>
                                                   <!--</v-form>-->
                                                    <v-flex md2 xs4 offset-xs1 v-if="!getEditExercise" text-xs-left class="hidden-sm-and-down">
                                                            <v-btn icon class="align-end pa-0 ma-0"   @click="copiedExerciseEdit(cExercise)">
                                                                <v-icon color="primary lighten-3">edit</v-icon>
                                                            </v-btn>
                                                            <v-btn icon absolute  class="align-end pa-0 ma-0" @click="removeExercise(cExercise)">
                                                                <v-icon color="error">remove_circle</v-icon>
                                                            </v-btn>
                                                      </v-flex>
                                                      <v-flex md1 xs3  v-if="getEditExercise" text-xs-right class="hidden-sm-and-down">
                                                            <v-btn icon class="align-end"
                                                                   absolute
                                                                   style="right: 50px; "
                                                                   @click="saveExerciseEdit(cExercise)"
                                                                   :disabled="hasErrors">
                                                                <v-icon color="accent">check_circle</v-icon>
                                                            </v-btn>
                                                            <v-btn icon absolute  class="align-end" @click="cancelEditExercise(cExercise)" v-if="!newExerciseToggle">
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
                                                          <v-form ref="mobileExerciseEditForm" v-model="valid" lazy-validation>
                                                        <v-toolbar dark color="primary">
                                                          <v-btn icon @click.native="cancelEditExercise(cExercise)" dark>
                                                            <v-icon>close</v-icon>
                                                          </v-btn>
                                                          <v-toolbar-title>Edit Exercise</v-toolbar-title>
                                                          <v-spacer></v-spacer>
                                                          <v-toolbar-items>
                                                            <v-btn dark flat
                                                                   @click.native="saveExerciseEdit(cExercise)"
                                                                   :disabled="!valid">Save</v-btn>
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
                                                                :rules="[rules.required]"
                                                                >

                                                            </v-select>
                                                      </v-flex>
                                                          <v-flex
                                                            xs4 offset-xs1
                                                            md1
                                                            offset-md1

                                                            >
                                                          <v-text-field
                                                              label="Sets"
                                                              type="number"
                                                              v-model="sets"
                                                              :rules="[rules.required, rules.validSets]"
                                                              hint="# of sets">

                                                          </v-text-field>

                                                      </v-flex>
                                                      <v-flex xs4 offset-xs2 md1 text-xs-right>
                                                          <v-text-field
                                                              label="Reps"
                                                              type="number"
                                                              v-model="reps"
                                                              :rules="[rules.required, rules.validReps]"
                                                              hint="# of reps">

                                                          </v-text-field>

                                                      </v-flex>
                                                    <v-flex xs3 offset-xs1 md2 offset-xs1 text-xs-right offset-md1 align-end>
                                                          <v-text-field
                                                              label="Weight"
                                                              type="number"
                                                              suffix="lbs."
                                                              :rules="[rules.validLW]"
                                                              v-model="workingWeight"
                                                              hint="Total weight lifted per rep">

                                                          </v-text-field>

                                                      </v-flex>
                                                            </v-layout>
                                                    </v-form>

                                                      </v-card>
                                                    </v-dialog>
                                                  </v-layout>

</v-layout>

                                                </v-list-tile>


</template>

<script>
    import { baseURLLocal } from "../../auth/auth-utils";
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
                selectedExercise: this.cExercise.exercises,
                searchExercises: null,
                exerciseSearchDisabled: false,

                setsVal: this.cExercise.sets,
                repsVal: this.cExercise.reps,
                liftingWeightVal: this.cExercise.lifting_weight,


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

                rules: {

                    required: (val) => !!val || 'Cannot be blank.',
                    workoutNameSpecialChars: (val) => {
                        return !/[^a-zA-Z0-9 '!]/.test(val) || 'Workout Name is Alphanumeric and can only include space, apostrophe and exclamation.';
                    },
                    validSets: (val) => val > 0 || 'Enter valid Sets',
                    validReps: (val) => val > 0 || 'Enter Valid Reps',
                    validLW: (val) => val >= 0 || 'Enter Valid Lifting Weight (lbs)'
                },

                mobileExerciseEditSave: false,
                valid: false,

                exerciseEditSave: false,
                exerciseValid: false,

                hasErrors: false,




            }
        },
        computed: {

            exercisePayload () {

                return {

                        selectedExercise: this.selectedExercise,
                        sets: this.sets,
                        reps: this.reps,
                        workingWeight: this.workingWeight
                    }
            },

            sets: {
                get () {

                    return this.setsVal;

                },

                set(val) {

                    this.setsVal = val;

                }
            },

            reps: {
                get () {

                    return this.repsVal;

                },

                set(val) {

                    this.repsVal = val;

                }
            },

            workingWeight: {
                get () {

                    return this.liftingWeightVal;

                },

                set(val) {

                    this.liftingWeightVal = val;

                }
            },



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

            exercisePayload() {

                this.hasErrors = false;

                Object.keys(this.exercisePayload).forEach(field => {
                    if (!this.$refs[field].validate()) this.hasErrors = true;
                })



            },

            eTargetMuscle() {

                this.exerciseSearchDisabled = !this.eTargetMuscle
            },
            searchExercises(val) {

                val && this.querySelections(val)
            },
        },
        methods: {

            cancelEditExercise(exercise) {

                this.sets = exercise.sets;
                this.reps = exercise.reps;
                this.workingWeight = exercise.lifting_weight;
                this.selectedExercise = exercise.exercises;

                this.editExercise = false;

            },


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
            querySelections: _.debounce(function (v) {
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
                500
            ),
            saveExerciseEdit(exercise) {
                this.getEditExercise = !this.getEditExercise;
                this.$store.commit('setNewExerciseToggle', false);

                exercise.exercises = this.selectedExercise;
                exercise.exercise_name = this.selectedExercise.exercise_name;
                exercise.sets = this.sets;
                exercise.reps = this.reps;
                exercise.lifting_weight = this.workingWeight? this.workingWeight: 0;




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