<template>
    <div>

        <v-layout v-if="selectedWorkout" justify-center row wrap>

            <v-flex md3 xs12>
                <v-snackbar v-model="snackbar" :color="snackColor" :top="y === 'top'">
                    {{ snackText }}
                </v-snackbar>


                    <v-card>
                            <v-layout  row wrap>
                                <v-flex xs8>
                                    <v-avatar class="ml-4 mt-2"><img :src="userAuth.user.avatar"></v-avatar>
                                    <div class="d-inline subheading  grey--text text--lighten-1 mt-0 mb-0 text-sm-center"
                                                style="text-transform: uppercase; letter-spacing: 1px">
                                            {{ userAuth.user.username }}</div>

                                    <div class="caption text-md-center text-xs-right text-sm-center ml-4 pl-1" style="position: relative; top: -15px;">
                                        <v-icon small>event</v-icon>
                                        {{ tmp.date_for_completion | moment }}
                                    </div>
                                </v-flex>
                                <v-flex xs4 md3 text-md-right text-xs-center>

                                    <v-btn icon @click.native="isEmailWorkout = !isEmailWorkout" class="ml-0 mr-0">
                                            <v-icon v-if="!isEmailWorkout" small color="accent">send</v-icon>
                                            <v-icon class="red--text" small v-if="isEmailWorkout">cancel</v-icon>
                                    </v-btn>
                                </v-flex>
                                <v-flex xs10 class="pb-2 ">

                                    <v-card raised v-if="isEmailWorkout" style="border-color: lightslategray; border-bottom-width: 5px;
                                                            position: absolute; height: 200px; top: 50px; width: 100%; z-index: 2">

                                        <form method="post" v-on:submit.prevent="sendWorkout">
                                            <v-card-title>
                                                Send this workout to a friend
                                            </v-card-title>
                                        <v-layout row>
                                            <v-flex xs8 offset-xs2 md8 text-xs-center>
                                            <v-select
                                                    v-model="shareFriendWorkout"
                                                    label="Search Friends"
                                                    append-icon="search"
                                                    return-object
                                                    item-text="from_user.username"
                                                    item-value="from_user.username"

                                                    :items="friendsList"
                                                    chips
                                                    :loading="loadingFriendSearch"
                                                    autocomplete
                                                    :search-input.sync="searchFriends"
                                                    required
                                            >
                                                <template slot="selection" slot-scope="data">

                                                    <v-chip
                                                      close
                                                      @input="data.parent.selectItem(data.item.from_user)"
                                                      :selected="data.selected"
                                                      :key="JSON.stringify(data.item.from_user)"
                                                    >
                                                      <v-avatar>
                                                        <img :src="data.item.from_user.avatar">
                                                      </v-avatar>
                                                      {{ data.item.from_user.username }}
                                                    </v-chip>
                                                  </template>
                                                <template slot="item" slot-scope="data">
                                                    <template v-if="typeof data.item !== 'object'">
                                                        <v-list-tile-content v-text="data.item"></v-list-tile-content>
                                                    </template>
                                                <template v-else>
                                                  <v-list-tile-avatar>
                                                    <img :src="data.item.from_user.avatar">
                                                  </v-list-tile-avatar>
                                                  <v-list-tile-content>
                                                    <v-list-tile-title v-html="data.item.from_user.username"></v-list-tile-title>
                                                  </v-list-tile-content>
                                                </template>
                                              </template>
                                            </v-select>
                                            </v-flex>
                                            </v-layout>
                                            <v-layout>
                                            <v-flex xs12 text-xs-center>
                                                <v-btn color="primary" :loading="loading" type="submit" :disabled="loading" @click.native="loader = 'loading'">
                                                    Send
                                                    <span slot="loader" class="custom-loader">
                                                        <v-icon>cached</v-icon>
                                                    </span>
                                                </v-btn>

                                            </v-flex>
                                                </v-layout>
                                        </form>
                                        </v-card>

                                </v-flex>
                                <v-flex xs10 offset-xs1 class="pt-0"><v-divider class="mt-1"></v-divider></v-flex>

                            </v-layout>
                            <v-card-media :src="tmp.workout_image" contain height="300px">
                                <v-layout row justify-center>
                                    <v-flex text-xs-center xs12>
                                        <h6 class="display-1 primary--text text--darken-2 ">
                                            {{ tmp.title }}</h6></v-flex></v-layout>
                            </v-card-media>
                            <v-progress-circular style="position:absolute; top: 50%; right: 50%; "  v-if="loadingWorkout" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                            <v-divider></v-divider>
                            <v-card-actions>

                                <v-btn flat class="primary--text text--lighten-2 pl-0 pt-0" @click.native="viewExercises = !viewExercises">View Exercises</v-btn>
                                <v-spacer></v-spacer>
                                <v-btn icon @click.native="viewExercises = !viewExercises">
                                    <v-icon color="primary">{{ viewExercises ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                                </v-btn>
                            </v-card-actions>
                            <v-card-text v-if="viewExercises">
                                <v-list dense>
                                      <template v-for="(exercise, i) in tmp.exercises" v-if="tmp.exercises.length > 0">
                                    <v-list-tile  :key="exercise.id">

                                      <v-list-tile-content class="grey--text text--darken-4">{{ i+1 }}. {{ exercise.exercise_name }}</v-list-tile-content>
                                      <v-list-tile-content class="align-end grey--text text--darken-1 pt-2">{{ exercise.sets }} x {{ exercise.reps }}
                                      <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="exercise.lifting_weight">
                                          @ {{ exercise.lifting_weight }} lbs.
                                      </v-list-tile-content>
                                      </v-list-tile-content>


                                    </v-list-tile>
                                        <toggle-exercise-notes  v-if="exercise.notes" :exercise="exercise" :index="i" :opened="exercise.isOpened"></toggle-exercise-notes>
                                          <v-divider class="mt-2"></v-divider>
                                          </template>
                                  </v-list>
                            </v-card-text>
                        </v-card>
            </v-flex>

            <v-flex md6 xs12 offset-md1>
                <v-flex xs12 class="mb-2 mt-3 pb-0"><v-card color="grey lighten-4">
                    <v-card-title><h6 class="headline primary--text text--darken-2 pt-0 pb-0 mt-0 mb-0">Edit Workout</h6></v-card-title>
                </v-card>
                </v-flex>
                <v-flex xs12>
                <v-card>

                              <v-card-text>
                                  <v-form ref="copyWorkoutForm" v-model="workoutValid" style="width: 100%;">
                                      <v-layout row wrap>

                                          <v-flex xs11 offset-xs1 class="text-xs-left mb-3 ">
                                                <span class="title grey--text text--darken-3">Workout Details</span>
                                          </v-flex>
                                          <v-flex xs10 offset-xs1 md4 offset-md1 >
                                              <v-text-field
                                                      color="accent"
                                                      label="Workout Title"
                                                      hint="What would you like to call this workout?"
                                                      append-icon="edit"
                                                      v-model="tmp.title"
                                                      :rules="[rules.required, rules.workoutNameSpecialChars]"
                                                      ></v-text-field>
                                          </v-flex>
                                          <v-flex xs10 offset-xs1 md4 offset-md1 >
                                               <v-menu
                                                    ref="menu"
                                                    lazy
                                                    :close-on-content-click="false"
                                                    v-model="menu"
                                                    transition="scale-transition"
                                                    offset-y
                                                    full-width
                                                    :nudge-right="40"
                                                    min-width="290px"
                                                    :return-value.sync="tmp.date_for_completion"
                                                  >
                                                    <v-text-field
                                                      slot="activator"
                                                      label="Completion Date"
                                                      v-model="tmp.date_for_completion"
                                                      :value="tmp.date_for_completion"
                                                      hint="When will you complete this workout?"
                                                      prepend-icon="event"
                                                      readonly
                                                      :rules="[rules.required]"

                                                    ></v-text-field>
                                                    <v-date-picker v-model="date" no-title scrollable>
                                                      <v-spacer></v-spacer>
                                                      <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                                                      <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                                                    </v-date-picker>
                                                  </v-menu>
                                          </v-flex>
                                          <v-flex xs10 offset-xs1 md4 offset-md1 >
                                              <v-select
                                                      v-model="tmp.training_type"
                                                      label="Training Type"
                                                      :value="tmp.training_type"
                                                      :items="training_types"
                                                      :rules="[rules.required]"
                                                      title="Training Type">

                                              </v-select>
                                          </v-flex>
                                          <v-flex xs10 offset-xs1 md4 offset-md1>
                                              <v-select
                                                  v-model="targetMuscle"
                                                  label="Target Muscle"
                                                  :value="tmp.target_muscle"
                                                  :items="targetMuscles"
                                                  hint="Exercises displayed based on target muscle."
                                                  :rules="[rules.required]"
                                              >

                                              </v-select>
                                          </v-flex>


                                      </v-layout>
                                       </v-form>
                                  <v-divider class="mt-3 mb-3"></v-divider>
                                      <v-layout row wrap fill-height>
                                          <v-layout row class="mt-0">
                                              <v-flex xs5 offset-xs1 class="text-xs-left">
                                                <span class="title grey--text text--darken-3">Exercises</span>
                                              </v-flex>
                                            <v-flex xs5 text-xs-right class="pt-0 mt-0">
                                              <v-btn icon @click="addNewExercise" class="pt-0 mt-0">
                                                  <v-icon v-if="!getAddNewExerciseToggle">add</v-icon>
                                                  <v-icon v-if="getAddNewExerciseToggle" color="error">cancel</v-icon>
                                              </v-btn>
                                            </v-flex>
                                          </v-layout>
                                          <v-flex xs12 class="mt-3">
                                           <!--<v-flex xs12 md1 offset-md1 class="mt-3">

                                           </v-flex>
                                            <v-flex md4 xs12 class="ml-2">
                                                <v-select
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
                                                    >

                                                </v-select>
                                            </v-flex>-->
                                          <v-list dense>
                                              <template v-for="(cExercise, i) in getCopiedExercises">
                                                <div :class="{'mt-4': $vuetify.breakpoint.smAndDown, 'mb-5': $vuetify.breakpoint.smAndDown,}">
                                                    <edit-copied-exercises
                                                        :c-exercise="cExercise"
                                                        :index="i"
                                                        :copied-workout="tmp"
                                                        :target-muscle="targetMuscle"
                                                        :edit-exercise="cExercise.editExercise">

                                                    </edit-copied-exercises>
                                                </div>
                                                  <v-flex xs12 md10 offset-md1 v-if="i !== getCopiedExercises.length -1"><v-divider></v-divider></v-flex>
                                              </template>
                                           </v-list>
                                              </v-flex>
                                      </v-layout>
                              </v-card-text>

                </v-card>

            </v-flex>
                <v-divider></v-divider>


                <v-flex text-xs-right>
                    <v-btn
                            @click="saveEdits"
                            :disabled="saveChangesDisabled"
                            color="accent">
                        Save Changes

                        <v-icon right >save</v-icon>
                    </v-btn>
                </v-flex>
            </v-flex>
        </v-layout>
        <v-alert v-else="selectedWorkout" color="error">Could not load the desired workout to edit</v-alert>
    </div>
</template>

<script>

import { userAuth, baseURLLocal } from '../auth/auth-utils'
import axios from 'axios'
import moment from 'moment'
import updateExercise from './edit-exercise.vue'
import EditCopiedExercises from './edit-copied-exercises.vue'
import ToggleExerciseNotes from './toggle-exercise-notes.vue'


export default {
    name: 'workout-detail',
  data () {
    return {

        isEmailWorkout: false,
        friendsList: [],
        shareFriendWorkout: [],
        loadingFriendSearch: false,
        searchFriends: null,

        saveChangesDisabled: false,
        workoutValid: false,

        selectedWorkout: this.$store.state.data[0],
        userAuth: this.$store.state.userAuth,
        newWorkout: {},
        updateTitle: false,
        tmp: this.$store.state.data[0],
        updateDate: false,
        viewExercises: false,
        loader: null,
        loading: false,
        y: 'top',
        context: '',
        snackbar: false,
        snackbarText: '',
        showToolTip: false,
        show: false,
        tip: false,

        loadingWorkout: false,

        date: this.$store.state.data[0].date_for_completion,
        workoutTitle: this.$store.state.data[0].title,
        trainingType: this.$store.state.data[0].training_type,
        targetMuscle: this.$store.state.data[0].target_muscle,
        completed: this.$store.state.data[0].completed,
        created: this.$store.state.data[0].created? this.$store.state.data[0].created: '',


        rules: {

                    required: (val) => !!val || 'Cannot be blank.',
                    workoutNameSpecialChars: (val) => {
                        return !/[^a-zA-Z0-9 '!]/.test(val) || 'Workout Name is Alphanumeric and can only include space, apostrophe and exclamation.';
                    },
                    validSets: (val) => val > 0 || 'Enter valid Sets',
                    validReps: (val) => val > 0 || 'Enter Valid Reps',
                    validLW: (val) => val >= 0 || 'Enter Valid Lifting Weight (lbs)'
      },


        target_exercises: [],
        eSearchDisabled: false,
        eSelectLoading: false,
        selectedExercise: null,
        searchExercises: null,
        exerciseDisabled: false,

        saveDisabled: false,

        snackColor: '',
        snackText: '',



        targetMuscles: [
            { text: 'Chest', value: "Chest"},
          //{ text: 'Biceps', value: "Biceps"},
          { text: 'Abs', value: "Abs"},
          //{ text: 'Triceps', value: "Triceps"},
          { text: 'Back', value: 'Back'},
          { text: 'Legs', value: 'Legs'},
          { text: 'Arms', value: 'Arms'},
        ],
        training_types: [
                  { text: 'Strength Training', value: 'Strength Training'},
                  { text: 'Flexibility Focused', value: 'Flexibility Focused'},
                  { text: 'Endurance', value: 'Endurance'},
                  { text: 'Balance Focused', value: 'Balance Focused'}
        ],
        menu: false,



        newExercise: {},



    }
  },

    filters: {
        moment: function (date) {
            return moment(date).format("dddd, MMMM Do YYYY");
        }
      },

  computed: {

        getAddNewExerciseToggle (){
                return this.$store.state.friendProfile.addNewExerciseToggle;
            },
            getCopiedWorkout: {
                get: function() {
                    this.tmp.exercises.map((e) => {e.editExercise = false; return e});
                    return this.tmp;
                },
                set: function (newExercise) {

                    this.tmp.exercises.push(newExercise);
                }

            },

            getCopiedExercises: function () {
                return this.tmp.exercises
            },

            getTargetMuscle: function () {
                return this.targetMuscle;
            }

  },

  watch: {

        workoutValid () {

            this.saveChangesDisabled = !this.workoutValid;
        },
        searchFriends(val) {
              val && this.querySelectionsFriends(val)
        },


        searchExercises(val) {

                val && this.querySelections(val)
            },
  },
  methods: {

        sendWorkout: function () {
            var self = this;
            var payload = this.tmp;

            for (var i = 0; i < payload.exercises.length; i++) {
                payload.exercises[i].workout_id = this.tmp.id;
            }

            payload.to = this.shareFriendWorkout.from_user.username;

            this.loading = true;
            axios.post(baseURLLocal + 'v1/workout/send/', payload)
                .then(function () {
                    self.snackbar = true;
                    self.snackText = "Successfully sent workout to " + payload.to;
                    self.snackColor = 'green';

                    self.loading = false;
                    console.log('Success')
                }).catch(function (err) {
                self.snackColor = 'error';
                self.snackbar = true;
                self.snackText = "Could not send workout to " + payload.to + " error " + err.response.data.status;

                self.loading = false;
                console.log(err)
            })
        },
        querySelections (v) {
                this.eSelectLoading = true;
                //if (!this.target_muscle) { this.errorMessages = "Please choose target muscle before choosing an exercise. "}

                axios.get(baseURLLocal+'v1/exercises/?target_muscle='+this.getTargetMuscle).then(response => {

                    this.target_exercises = response.data.results.filter(e => {
                        return (e || '').exercise_name.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.eSelectLoading = false;
                }).catch(err => {
                    console.log(err);
                    this.eSelectLoading = false;
                })

        },
      querySelectionsFriends(v) {
            this.loadingFriendSearch = true;
            this.friendsList = [];


                if (v) {
                    axios.get(baseURLLocal+'v1/friends/find?search='+v).then(response => {

                    this.friendsList = response.data.results.filter(e => {
                        return (e || '').from_user.username.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.loadingFriendSearch = false;
                    }).catch(err => {
                        this.friendsList = [];
                        console.log(err);
                    })
                }

                else {
                    this.friendsList = [];
                }
      },
        addNewExercise() {
                let newExercise = {};
                this.$store.commit('setNewExerciseToggle', !this.$store.state.friendProfile.addNewExerciseToggle);
                //this.addNewExerciseToggle = this.$store.state.friendProfile.addNewExerciseToggle;

                if (!this.getAddNewExerciseToggle) {

                    this.tmp.exercises.splice(-1, 1); // user cancels addition of new exercise, so we remove last one from list
                    return
                }

                // construct new exercise object with default/stub values

                newExercise.user = this.$store.state.userAuth.user.id;
                newExercise.date_for_completion = '';
                newExercise.lifting_weight = 0;
                newExercise.sets = 0;
                newExercise.reps = 0;
                newExercise.workout_id = null;
                newExercise.editExercise = true;
                newExercise.exercises = [];

                // push onto copied workout exercises property list

                this.getCopiedWorkout = newExercise;


            },
      save: function (e) {
        this.updateTitle = false;

      },
      saveEdits: function () {
            this.saveChangesDisabled = true;
            var self = this;
            this.loader = 'loading';
            var payload = this.tmp;

            for (var i =0; i < payload.exercises.length; i++) {
                payload.exercises[i].workout_id = payload.id;
            }

            payload.workout_image = null;
            this.loading = true;
            axios.put(baseURLLocal+'v1/workouts/'+payload.id +'/', payload)
                .then(function (response) {
                    payload.workout_image = response.data.workout_image;

                    let arr = [];
                    arr.push(response.data);

                    self.$store.commit('setData', arr);

                    self.tmp = response.data;


                    self.snackColor = 'success';
                    self.snackbar = true;
                    self.snackText = "Successfully updated workout";


                    self.loading = false;

                    self.saveChangesDisabled = false;

                    console.log('Success')
            }).catch(function (err) {
                    self.snackColor = 'error';
                    self.snackbar = true;
                    self.snackText = "Could not update workout "+"error " + err;

                    self.loading = false;

                    self.saveChangesDisabled = false;

                    console.log(err)
            })
        },



  },


  components: {
      updateExercise, EditCopiedExercises, ToggleExerciseNotes
  }
}
</script>

<style>


            /* Enter and leave animations can use different */
        /* durations and timing functions.              */
        .slide-fade-enter-active {
          transition: all .3s ease;
        }
        .slide-fade-leave-active {
          transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
        }
        .slide-fade-enter, .slide-fade-leave-to
        /* .slide-fade-leave-active below version 2.1.8 */ {
          transform: translateX(10px);
          opacity: 0;
        }



    .custom-loader {
        animation: loader 1s infinite;
        display: flex;
    }

    @-moz-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-webkit-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-o-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }

    .card > .card__title {
        display: block;
    }

    .card-title {
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0;
    }

</style>
