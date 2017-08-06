<template>
    <div>
        <h3 class="hidden-sm-and-down">Create Your Workouts</h3>

        <v-layout row v-show="createWorkout">
            <v-flex md6 sm12 xs12>
                <v-stepper v-model="e6" vertical>
                    <v-stepper-step step="1" v-bind:complete="e6 > 1">
                      Create Your Workout
                    </v-stepper-step>
                    <v-stepper-content step="1">
                           <form v-on:submit.prevent="onSubmit" id="workoutform" method="post">
                    <v-flex md8 offset-md1 xs12 >
                            <v-text-field v-model="title" id="id-title" type="text"
                                          name="title" label="Workout Name"
                                          counter max="99"
                            ></v-text-field>
                    </v-flex>
                               <v-flex xs12 md8 offset-md1>
                                    <v-menu
                                      lazy
                                      :close-on-content-click="false"
                                      v-model="dateMenu"
                                      transition="scale-transition"
                                      offset-y
                                      full-width
                                      :nudge-left="40"
                                      max-width="290px"
                                    >
                                      <v-text-field
                                        slot="activator"
                                        label="Completion Date"
                                        v-model="completionDate"
                                        prepend-icon="event"
                                        readonly
                                      ></v-text-field>
                                      <v-date-picker v-model="completionDate" no-title scrollable actions>
                                        <template scope="{ save, cancel }">
                                          <v-card-actions>
                                            <v-btn flat primary @click.native="cancel()">Cancel</v-btn>
                                            <v-btn flat primary @click.native="save()">Save</v-btn>
                                          </v-card-actions>
                                        </template>
                                      </v-date-picker>
                                    </v-menu>
                                  </v-flex>
                    <v-flex md8 xs12 offset-md1>
                        <div class="py-2">
                            <v-select title="Target Muscle" id="id_target_muscle" name="target_muscle"
                                      v-model="target_muscle" :items="target_muscles"
                                      label="Target Muscles" segmented></v-select>
                        </div>
                    </v-flex>
                    <v-flex md8 xs12 offset-md1>
                        <div class="py-2">
                            <v-select title="Training Type" id="id_training_type"
                                    name="training_type" v-model="training_type"
                                    label="Training Type" :items="training_types"
                                    required="" segmented>
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
                            <v-btn primary @click.native="onFocus">
                                <input type="submit" ref="workoutSubmit" value="Continue">
                            </v-btn>
                        </div>
                    </div>

                </form>
                    </v-stepper-content>
                    <v-stepper-step step="2" v-bind:complete="e6 > 2">Add Exercises </v-stepper-step>
                    <v-stepper-content step="2">
                        <form v-on:submit.prevent="onSubmitExercise" id="exerciseform" method="post">
                    <v-flex md8 offset-md1 xs12 >
                            <v-text-field v-model="exercise_title" id="id-exercise-title" type="text"
                                          name="exercise-title" label="Exercise Name"
                                          counter max="99"
                            ></v-text-field>
                    </v-flex>
                    <v-flex md8 xs12 offset-md1>
                        <div class="py-2">
                            <v-text-field title="Sets" label="Sets" type="number" v-model="sets"></v-text-field>
                        </div>
                    </v-flex>
                    <v-flex md8 xs12 offset-md1>
                        <div class="py-2">
                            <v-text-field title="Reps" label="Reps" v-model="reps">
                            </v-text-field>
                        </div>
                    </v-flex>
                    <v-flex md8 xs12 offset-md1>
                        <v-text-field title="exercise_notes" label="Notes about this exercise" v-model="exercise_notes" multi-line counter max="255"></v-text-field>
                    </v-flex>
                    <div class="form-group row">
                        <div class="col-8">
                            <input id="id_user" name="user" :value="userAuth.user.id" hidden>
                        </div>
                    </div>

                    <v-flex md8 offset-md1 xs12>
                            <v-btn primary @click.native="onFocusExercise">
                                <input type="submit" ref="exerciseSubmit" value="Continue">
                            </v-btn>
                            <v-btn secondary @click.native="e6 = 1">Back</v-btn>
                    </v-flex>

                </form>

                    </v-stepper-content>
                    <v-stepper-step step="3" v-bind:complete="e6 > 3">Select an ad format and name ad unit</v-stepper-step>
                    <v-stepper-content step="3">
                      <v-card class="grey lighten-1 z-depth-1 mb-5" height="200px"></v-card>
                      <v-btn primary @click.native="e6 = 4">Continue</v-btn>
                      <v-btn flat>Cancel</v-btn>
                    </v-stepper-content>
                    <v-stepper-step step="4">View setup instructions</v-stepper-step>
                    <v-stepper-content step="4">
                      <v-card class="grey lighten-1 z-depth-1 mb-5" height="200px"></v-card>
                      <v-btn primary @click.native="e6 = 1">Continue</v-btn>
                      <v-btn flat>Cancel</v-btn>
                    </v-stepper-content>
                  </v-stepper>

                <v-snackbar :top="y === 'top'" v-model="snackbar" :success="context === 'success'" :error="context === 'error'">
                    {{ snackbarMessage }}
                    <v-btn flat class="red--text" @click.native="snackbar = false">Close</v-btn>
                </v-snackbar>
            </v-flex>
        </v-layout>
        <v-speed-dial v-model="fab" fixed bottom right :direction="direction" :hover="hover" :transition="transition">
            <v-btn :class="activeFab.class" slot="activator" fab dark hover v-model="fab" @click.native="addWorkoutClick">
                <v-icon>add</v-icon>
                <v-icon>check_circle</v-icon>
            </v-btn>
            <v-btn fab dark small class="red" @click.native="addWorkoutClick">
                <v-icon>cancel</v-icon>
            </v-btn>
        </v-speed-dial>
        </div>
</template>
<script>
 import myDatepicker from 'vue-datepicker'

 import axios from 'axios'
 import { login, userAuth } from '../auth/auth'



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
      exercise_notes: '',
      target_muscle: '',
      training_type: '',
      workout_id: '',
      submittedWorkout: {},
      userAuth: userAuth,
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
      computed: {
        slug: function getSlug(e) {
            var date;
            if (!this.completionDate){ date = Date.now(); }
            else { date = this.completionDate; }
            this.title = this.title.replace(/ /g, '-');
            return this.title + '-' + date + '-' + this.target_muscle;
        },
        activeFab: function (e) {
            if (this.createWorkout) {
                return {'class': 'green'}
            }
            else {
                return {'class': 'blue-grey'}
            }
        },

      },
      methods: {
        onFocus: function () {
            this.$refs.workoutSubmit.click();

        },
        onFocusExercise: function () {
            this.$refs.exerciseSubmit.click();
        },
        addWorkoutClick: function () {
            this.createWorkout = !this.createWorkout;
        },
        onSubmit: function (event) {
            var self = this;
            var baseURL = "http://127.0.0.1:8000/";

            var data = {
                title: this.title,
                date_for_completion: this.completionDate,
                target_muscle: this.target_muscle,
                training_type: this.training_type,
                slug: this.slug,
                user: this.userAuth.user.id,
                exercises: [],
            };
            console.log(data);
            console.log(this.submittedWorkout);
            console.log(JSON.stringify(data) === JSON.stringify(this.submittedWorkout));

            // No changes to sync
            if (JSON.stringify(data) === JSON.stringify(this.submittedWorkout)) {

                this.e6 = 2;
                return 
            }


            axios.post(baseURL + 'v1/workouts/', data)
                .then(function (response) {
                    self.snackbarMessage = "Successfully created your workout";
                    self.context = 'success';
                    self.snackbar = true;
                    self.e6 = 2;
                    self.workout_id = response.data.id;
                    self.submittedWorkout = data;

                }).catch(function (error) {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx

                    self.snackbarMessage = "There was an error creating workouts: \n" + 'Status' + '\n' + error.response.status;
                    self.context = 'error';
                    self.snackbar = true;


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
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error

                    self.snackbarMessage = "There was an error in the request: " + error.message;
                    self.context = 'error';
                    self.snackbar = true;
                    console.log('Error', error.message);
                }

                console.log(error.config);
            });
        },
        onSubmitExercise: function (event) {
              var self = this;
              var baseURL = "http://127.0.0.1:8000/";
              var exercises = null;
              if (!exercises){
                  exercises = {};
                  exercises.exercise_name = this.exercise_title;
                  exercises.target_muscle = this.target_muscle;
              }

              var data = {
                  exercise_name: this.exercise_title,
                  sets: this.sets,
                  reps: this.reps,
                  notes: this.exercise_notes,
                  user: this.userAuth.user.id,
                  exercises: exercises,
                  workout_id: this.workout_id,
              };


              axios.post(baseURL + 'v1/exercise/', data)
                  .then(function (response) {
                      self.snackbarMessage = "Successfully added exercise " +self.exercise_title;
                      self.context = 'success';
                      self.snackbar = true;
                      self.e6 = 2;

                  }).catch(function (error) {
                  if (error.response) {
                      // The request was made and the server responded with a status code
                      // that falls out of the range of 2xx

                      self.snackbarMessage = "There was an error creating workouts: \n" + 'Status' + '\n' + error.response.status;
                      self.context = 'error';
                      self.snackbar = true;


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
                      console.log(error.request);
                  } else {
                      // Something happened in setting up the request that triggered an Error

                      self.snackbarMessage = "There was an error in the request: " + error.message;
                      self.context = 'error';
                      self.snackbar = true;
                      console.log('Error', error.message);
                  }

                  console.log(error.config);
              });
          },
      },
}
</script>

<style>
    @media only screen and (max-width: 768px) {

        div > div.row-margin-top {
            margin: 0;
        }
        div.stepper > div.stepper__content {
            padding: 16px 30px 16px 23px;
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
        border-left: 4px solid #270989;
        padding-left: 4px;
    }
</style>