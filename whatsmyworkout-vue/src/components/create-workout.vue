<template>
    <div>
        <v-layout row v-bind="binding" >
            <v-flex md5 sm12 xs12 v-if="createWorkout" style="margin-left: 1%">
                <v-stepper v-model="e6" vertical>
                    <v-stepper-step step="1" v-bind:complete="e6 > 1">
                        Create Your Workout
                    </v-stepper-step>
                    <v-stepper-content step="1">
                        <v-form v-on:submit.prevent="onSubmit" id="workoutform" method="post" ref="workoutForm">
                            <v-flex md8 offset-md1 xs12>
                                <v-text-field v-model="title" id="id-title" type="text" name="title" label="Workout Name" counter max="99"></v-text-field>
                            </v-flex>
                            <v-flex xs12 md8 offset-md1>
                                <v-menu
                                        lazy
                                        :close-on-content-click="false"
                                        v-model="dateMenu"
                                        transition="scale-transition"
                                        offset-y full-width
                                        :nudge-left="40"
                                        max-width="290px"
                                        ref="menuDate"
                                        :return-value.sync="completionDate">
                                    <v-text-field slot="activator" label="Completion Date" v-model="completionDate" prepend-icon="event" readonly></v-text-field>
                                    <v-date-picker v-model="completionDate" no-title scrollable actions>
                                        <template slot-scope="{ save, cancel }">
                                            <v-card-actions>
                                                <v-btn flat color="primary" @click.native="menu = false">Cancel</v-btn>
                                                <v-btn flat color="primary" @click.native="$refs.menuDate.save(completionDate)">Save</v-btn>
                                            </v-card-actions>
                                        </template>
                                    </v-date-picker>
                                </v-menu>
                            </v-flex>
                            <v-flex md8 xs12 offset-md1>
                                <div class="py-2">
                                    <v-select title="Target Muscle" id="id_target_muscle" name="target_muscle"
                                              v-model="target_muscle" v-bind:items="target_muscles" label="Target Muscles"
                                              ></v-select>
                                </div>
                            </v-flex>
                            <v-flex md8 xs12 offset-md1>
                                <div class="py-2">
                                    <v-select title="Training Type" id="id_training_type" name="training_type"
                                              v-model="training_type" label="Training Type" v-bind:items="training_types"
                                              required="" >
                                    </v-select>
                                </div>
                            </v-flex>
                            <div class="form-group row">
                                <div class="col-8">
                                    <input id="id_slug" name="slug" :value="slug" hidden>
                                </div>
                            </div>
                            <div class="form-group row">
                                <div class="col-8">
                                    <input id="id_user" name="user" :value="userAuth.user.id" hidden>
                                </div>
                            </div>

                            <div class="form-group row">
                                <div class="col-8">
                                    <v-btn color="primary" @click.native="onFocus" :loading="loading2" :disabled="loading2">
                                        <input type="submit" ref="workoutSubmit" value="Continue">
                                        <span slot="loader" class="custom-loader">
                                            <v-icon>cached</v-icon>
                                        </span>
                                    </v-btn>
                                </div>
                            </div>

                        </v-form>
                    </v-stepper-content>
                    <v-stepper-step step="2" v-bind:complete="e6 > 2">Add Exercises </v-stepper-step>
                    <v-stepper-content step="2">
                        <v-form v-on:submit.prevent="onSubmitExercise" id="exerciseform" method="post" ref="exerciseRefSubmit">
                            <v-flex md8 offset-md1 xs12>
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
                            <v-flex md8 xs12 offset-md1>
                                <div class="py-2">
                                    <v-text-field title="Sets" label="Sets" type="number" v-model="sets"></v-text-field>
                                </div>
                            </v-flex>
                            <v-flex md8 xs12 offset-md1>
                                <div class="py-2">
                                    <v-text-field title="Reps" label="Reps" v-model="reps" type="number">
                                    </v-text-field>
                                </div>
                            </v-flex>
                            <v-flex md8 xs12 offset-md1>
                                <div class="py-2">
                                    <v-text-field title="Lifting weight" label="Lifting Weight" type="number" v-model="lifting_weight" placeholder="lbs."></v-text-field>
                                </div>
                            </v-flex>
                            <v-flex md8 xs12 offset-md1>
                                <v-text-field title="exercise_notes" label="Notes about this exercise" v-model="exercise_notes"
                                              multi-line counter max="255"></v-text-field>
                            </v-flex>
                            <div class="form-group row">
                                <div class="col-8">
                                    <input id="id_user" name="user" :value="userAuth.user.id" hidden>
                                </div>
                            </div>

                            <v-flex md9 offset-md1 xs12>
                                <v-btn color="primary" @click.native="onFocusExercise" :loading="loading1" :disabled="loading1">
                                    <input type="submit" ref="exerciseSubmit" value="Save & Add">
                                    <span slot="loader" class="custom-loader">
                                        <v-icon>cached</v-icon>
                                    </span>
                                </v-btn>
                                <v-btn secondary @click.native="e6 = 1">Back</v-btn>
                                <v-btn class="blue-grey white--text" @click.native="e6 = 3">Continue</v-btn>
                            </v-flex>

                        </v-form>
                    </v-stepper-content>
                    <v-stepper-step step="3" v-bind:complete="e6 > 3">Complete</v-stepper-step>
                    <v-stepper-content step="3">
                        <v-btn color="primary" @click.native="createMore">Create More</v-btn>
                        <v-btn flat @click="createWorkout">Done</v-btn>
                    </v-stepper-content>
                </v-stepper>

                <v-snackbar :top="y === 'top'" v-model="snackbar" :color="snackbarColor" :success="context === 'success'" :error="context === 'error'">
                    {{ snackbarMessage }}
                    <v-btn flat class="red--text" @click.native="snackbar = false">Close</v-btn>
                </v-snackbar>

            </v-flex>

            <v-flex md6 xs12 class="non-mobile-margin">
                <div style="text-align: center" class="pt-5 pb-3">
                    <v-icon large>history</v-icon>
                    <span>Recently Created Workouts</span>
                </div>
                <template >
                    <v-alert error :value="alert" transition="scale-transition">Error loading last 5 workouts</v-alert>
                    <v-expansion-panel>
                        <v-progress-circular style="position: absolute; left: 25%;" v-if="loading" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                        <v-expansion-panel-content v-for="recentWorkout in recentWorkouts" :key="recentWorkouts.id">
                            <div slot="header">
                                <span class="pr-2"><img src="https://s3.amazonaws.com/wmw-static/static/img/weights.png"> </span> {{ recentWorkout.date_for_completion | moment }}
                            </div>
                            <v-layout row>
                                <v-flex xs12>
                                    <v-card>
                                        <v-card-title>
                                            <div class="title" style="margin: 0 15% 0 15%">{{ recentWorkout.title }}</div>
                                        </v-card-title>
                                        <v-card-media :src="recentWorkout.workout_image" height="250px" contain>

                                        </v-card-media>
                                        <v-card-title class="hidden-md-and-up">
                                            <div>
                                                <v-icon>account_circle</v-icon><span class="pl-2 text-xs">{{ userAuth.user.username }}</span>
                                                <div class="pb-3"></div>
                                                <v-icon>schedule</v-icon><span class="pl-2">{{ recentWorkout.date_for_completion | moment}}</span>
                                                <div class="pb-3"></div>
                                                <img src="../assets/img/muscle.png">
                                                <span class="pl-2 grey--text text--darken-3">{{ recentWorkout.target_muscle }}</span>
                                            </div>
                                        </v-card-title>
                                        <v-card-title class="hidden-sm-and-down">
                                            <v-flex md3>
                                                <v-icon>account_circle</v-icon><span class="pl-2 text-xs">{{ userAuth.user.username }}</span>
                                            </v-flex>
                                            <v-flex md5 class="mt-2">
                                                <v-icon>schedule</v-icon><span class="pl-2">{{ recentWorkout.date_for_completion | moment}}</span></v-flex>

                                            <v-flex md3 class="mt-2"><img src="../assets/img/muscle.png">
                                                <span class="pl-2 grey--text text--darken-3">{{ recentWorkout.target_muscle }}</span></v-flex>
                                        </v-card-title>
                                        <v-divider></v-divider>
                                        <v-card-actions>
                                            <v-btn flat class="blue--text text--darken-4 pl-0 pt-0" @click.native="showExercises = !showExercises">View Exercises</v-btn>
                                            <v-spacer></v-spacer>
                                            <v-btn class="pt-0" icon @click.native="showExercises = !showExercises" ref="clickShowExercises">
                                                <v-icon>{{ showExercises ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                                            </v-btn>
                                        </v-card-actions>
                                        <v-slide-y-transition>
                                            <v-list three-line v-show="showExercises">
                                                <v-layout row justify-center>
                                                    <v-flex xs6>
                                                        <v-subheader>Exercise</v-subheader>
                                                    </v-flex>
                                                    <v-flex xs3 offset-xs1>
                                                        <v-subheader class="text-xs-center">sets/reps</v-subheader>
                                                    </v-flex>
                                                </v-layout>
                                                <template v-for="(exercise, i) in recentWorkout.exercises">

                                                    <v-list-tile style="padding: 0">
                                                        <v-list-tile-content>
                                                                <v-layout style="width: 100%" row wrap :key="exercise.exercise_name">


                                                                    <v-flex style="display: flex;" xs12>
                                                                        <v-flex xs1 class="ml-1">
                                                                            <div style="text-align: right;">{{ i+1 }}.</div>
                                                                        </v-flex>
                                                                        <v-flex xs8 class="body-1" style="word-wrap: break-word; margin-left: 5px">
                                                                            {{ exercise.exercise_name }}
                                                                        </v-flex>
                                                                        <v-flex xs2 offset-xs1>
                                                                            <div>{{ exercise.sets }}/{{ exercise.reps }}</div>
                                                                        </v-flex>
                                                                    </v-flex>
                                                                    <!--<v-layout><v-flex>{{ exercise.lifting_weight }}</v-flex></v-layout>-->
                                                                    <div style="position: relative; margin-left: 5%"><v-icon style="position: absolute; top: 0;" color=" ">fa-sticky-note-o</v-icon></div>
                                                                    <div class="caption" style="word-wrap: break-word; margin: 2% 0 0 5%;">
                                                                        {{ exercise.notes }}
                                                                    </div>

                                                                </v-layout>
                                                        </v-list-tile-content>

                                                    </v-list-tile>
                                                    <v-divider></v-divider>
                                                </template>
                                            </v-list>
                                            </v-card-text>
                                        </v-slide-y-transition>
                                    </v-card>
                                </v-flex>
                            </v-layout>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </template>
            </v-flex>
        </v-layout>
        <v-fab-transition>
            <v-btn :class="activeFab.class" :key="activeFab.icon" v-model="fab" @click.native="addWorkoutClick" fab fixed bottom right>
                <v-icon>{{ activeFab.icon }}</v-icon>
            </v-btn>
        </v-fab-transition>
    </div>
</template>
<script>
 import moment from 'moment'
 import axios from 'axios'
 import { devServer, baseURLLocal, login, userAuth } from '../auth/auth-utils'




  export default {
      name: 'create-workout',
    data () {
      return {
      completionDate: null,
      dateMenu: false,
      e6:1,
      direction: "top",
      fab: false,
      fling: false,
      hover: false,
      top: false,
      showExercises: false,
      right: true,
      bottom: true,
      left: false,
      transition: 'slide-y-reverse-transition',
      snackbarMessage: '',
      snackbar: false,
      hidden:false,
      createWorkout: false,
      y: 'top',
      context: '',
      title: '',
      exercise_title: '',
      sets: '',
      reps: '',
      lifting_weight: '',
      exercise_notes: '',
      target_muscle: '',
      training_type: null,
      workout_id: '',
      recentWorkouts: {},
      submittedWorkout: {},
      userAuth: this.$store.state.userAuth,
      loading: false,
      alert: false,
      loading1: false,
      loading2: false,
      loader: null,
      snackbarColor: ' ',

      target_exercises: [],
      eSearchDisabled: false,
      eSelectLoading: false,
      selectedExercise: null,
      searchExercises: null,
      exerciseDisabled: false,
          

      training_types: [
          { text: 'Strength Training', value: 'Strength Training'},
          { text: 'Flexibility Focused', value: 'Flexibility Focused'},
          { text: 'Endurance', value: 'Endurance'},
          { text: 'Balance Focused', value: 'Balance Focused'}

      ],
      target_muscles: [
          { text: 'Traps', value: 'Traps'},
          { text: 'Neck', value: "Neck"},
          { text: 'Chest', value: "Chest"},
          { text: 'Biceps', value: "Biceps"},
          { text: 'Forearm', value: "Forearm"},
          { text: 'Abdominal', value: "Abdominal"},
          { text: 'Quads', value: "Quads"},
          { text: 'Calves', value: "Calves"},
          { text: 'Triceps', value: "Triceps"},
          { text: 'Lats', value: "Lats"},
          { text: 'Middle Back', value: "Middle Back"},
          { text: 'Lower Back', value: "Lower Back"},
          { text: 'Glutes', value: "Glutes"},
          { text: 'Hamstrings', value: "Hamstrings"}

      ],


    }

  },
      filters: {
        moment: function (date) {
            return moment(date).format("dddd, MMMM Do YYYY");
        }
      },
      watch: {
          target_muscle (v) {

                this.eSearchDisabled = !v;
            },
          searchExercises(val) {

                val && this.querySelections(val)
            }

      },
      computed: {
        binding: function () {
          const binding = {};

          if (this.$vuetify.breakpoint.smAndDown) binding.column = true;

          return binding;

        },
        slug: function getSlug(e) {
            var date;
            var title = this.title;
            if (!this.completionDate){ date = Date.now(); }
            else { date = this.completionDate; }
            title = title.replace(/ /g, '-');
            return title + '-' + date + '-' + this.target_muscle;
        },
        activeFab: function (e) {
            if (this.createWorkout) {
                return {'class': 'red', icon: 'cancel'}
            }
            else {
                return {'class': 'blue-grey', icon: 'add'}
            }
        },

      },
      methods: {
          querySelections (v) {
                this.eSelectLoading = true;
                //if (!this.target_muscle) { this.errorMessages = "Please choose target muscle before choosing an exercise. "}

                axios.get(baseURLLocal+'v1/exercises/?target_muscle='+this.target_muscle).then(response => {

                    this.target_exercises = response.data.results.filter(e => {
                        return (e || '').exercise_name.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.eSelectLoading = false;
                }).catch(err => {
                    console.log(err);
                    this.eSelectLoading = false;
                })

            },
        onFocus: function () {
            this.$refs.workoutSubmit.click();
            this.loader = 'loading2';

        },
        onFocusExercise: function () {
            this.$refs.exerciseSubmit.click();
            this.loader = 'loading1';
        },
        addWorkoutClick: function () {
            this.createWorkout = !this.createWorkout;
        },
        onSubmit: function (event) {
            var self = this;


            var data = {
                title: this.title,
                date_for_completion: this.completionDate,
                target_muscle: this.target_muscle,
                training_type: this.training_type,
                slug: this.slug,
                user: this.userAuth.user.id,
                exercises: [],
            };

            // No changes to sync
            if (JSON.stringify(data) === JSON.stringify(this.submittedWorkout)) {

                this.e6 = 2;
                return 
            }

            if (this.workout_id && JSON.stringify(data) !== JSON.stringify(this.submittedWorkout)) {
                this.loading2 = true;

                axios.put(baseURLLocal+'v1/workouts/'+this.workout_id + '/', data)
                .then(function (response) {
                    self.snackbarMessage = "Successfully updated your workout";
                    self.context = 'success';
                    self.snackbarColor = 'success';
                    self.snackbar = true;
                    self.e6 = 2;
                    self.workout_id = response.data.id;
                    self.submittedWorkout = data;

                }).catch(function (error) {
                    self.loading2 = false;
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx

                    self.snackbarMessage = "There was an error updating workouts: \n" + 'Status' + '\n' + error.response.status;
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarColor = 'error';

                    console.log(error.response.data);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in node.js

                    self.snackbarMessage = "There was an error generating a response from the server: \n" + error.request;
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarColor = 'error';
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error

                    self.snackbarMessage = "There was an error in the request: " + error.message;
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarColor = 'error';
                    console.log('Error', error.message);
                }

                console.log(error.config);
            });

                return
            }

            this.loading2 = true;
            axios.post(baseURLLocal+'v1/workouts/', data)
                .then(function (response) {
                    self.loading2 = false;
                    self.snackbarMessage = "Successfully created your workout";
                    self.context = 'success';
                    self.snackbar = true;
                    self.snackbarColor = 'success';
                    self.e6 = 2;
                    self.workout_id = response.data.id;
                    self.submittedWorkout = data;

                }).catch(function (error) {
                    self.loading2 = false;
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx

                    self.snackbarMessage = "There was an error creating workouts: \n" + 'Status' + '\n' + error.response.status;
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarColor = 'error';


                    console.log(error.response.data);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in node.js

                    self.snackbarMessage = "There was an error generating a response from the server: \n" + error.request;
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarColor = 'error';
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error

                    self.snackbarMessage = "There was an error in the request: " + error.message;
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarColor = 'error';
                    console.log('Error', error.message);
                }

                console.log(error.config);
            });
        },
        createMore: function () {
            this.$refs.workoutForm.reset();
            this.workout_id = '';
            this.e6 = 1;

        },
        onSubmitExercise: function (event) {
              var self = this;
              var exercises = this.selectedExercise ;


              if (!exercises){
                  exercises = {};
                  exercises.exercise_name = this.exercise_title;
                  exercises.target_muscle = this.target_muscle;
              }

              var data = {
                  exercise_name: this.exercise_title,
                  sets: this.sets,
                  reps: this.reps,
                  lifting_weight: this.lifting_weight,
                  notes: this.exercise_notes,
                  user: this.userAuth.user.id,
                  exercises: exercises,
                  workout_id: this.workout_id,
              };

              this.loading1 = true;
              axios.post(baseURLLocal+'v1/exercise/', data)
                  .then(function (response) {
                      self.snackbarMessage = "Successfully added exercise " +self.exercise_title;
                      self.context = 'success';
                      self.snackbarColor = 'success';
                      self.snackbar = true;
                      self.e6 = 2;
                      self.loading1 = false;
                      self.$refs.exerciseRefSubmit.reset();


                  }).catch(function (error) {
                      self.loading1 = false;
                  if (error.response) {
                      // The request was made and the server responded with a status code
                      // that falls out of the range of 2xx

                      self.snackbarMessage = "There was an error creating workouts: \n" + 'Status' + '\n' + error.response.status;
                      self.context = 'error';
                      self.snackbarColor = 'error';
                      self.snackbar = true;
                      self.loading1 = false;


                      console.log(error.response.data);
                      console.log(error.response.status);
                      console.log(error.response.headers);
                  } else if (error.request) {
                      // The request was made but no response was received
                      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                      // http.ClientRequest in node.js

                      self.snackbarMessage = "There was an error generating a response from the server: \n" + error.request;
                      self.context = 'error';
                      self.snackbarColor = 'error';
                      self.snackbar = true;
                      console.log(error.request);
                  } else {
                      // Something happened in setting up the request that triggered an Error

                      self.snackbarMessage = "There was an error in the request: " + error.message;
                      self.context = 'error';
                      self.snackbarColor = 'error';
                      self.snackbar = true;
                      console.log('Error', error.message);
                  }

                  console.log(error.config);
              });
          },
      },
      mounted: function () {
            var self = this;

            this.loading = true;
            axios.get(baseURLLocal+'v1/workouts/?recent=5').then(function (response) {
                self.loading = false;
                self.recentWorkouts = response.data.results;



            }).catch(function (e) {
                console.log('There was an error loading recent workouts');
                self.loading = false;
                self.alert = true;


            })
      },
}
</script>

<style>
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

    .non-mobile-margin {
            margin-left: 5%;
        }
    

    @media only screen and (max-width: 768px) {

        div > div.row-margin-top {
            margin: 0;
        }
        div.stepper > div.stepper__content {
            padding: 16px 30px 16px 23px;
        }
        .non-mobile-margin {
            margin-left: 0;
        }

    }


    div > div.row-margin-top {
        display: inline-block;
        width: 90%;
    }
    div.row > div.row {
        margin-top: 5%;
    }
    h3 {
        letter-spacing: 5px;
        color: dimgrey;
        padding-left: 4px;
    }
</style>