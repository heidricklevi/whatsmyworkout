<template>
    <v-container fluid>
        <h3 class="hidden-sm-and-down">Create Your Workouts</h3>
        <v-layout row v-show="createWorkout">
            <v-flex md4 sm12>
                <form v-on:submit.prevent="onSubmit" id="workoutform" method="post">
                    <div class="form-group row">
                        <div class="col-8">
                            <input v-model="title" id="id-title" type="text" name="title" placeholder="Give this workout a name">
                        </div>
                    </div>
                    <div class="form-group row">
                        <div class="col-8">
                            <date-picker id="id_date_for_completion" name="date_for_completion" :date="date"></date-picker>
                        </div>
                    </div>
                    <div class="form-group row">
                        <div class="col-8">
                            <select title="Target Muscle" id="id_target_muscle" name="target_muscle" v-model="target_muscle">
                                <option disabled value="">Target Muscle</option>

                                <option v-for="target_muscle in target_muscles" v-bind:value="target_muscle.value">
                                    {{ target_muscle.text }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group row">
                        <div class="col-8">
                            <select title="Training Type" id="id_training_type" name="training_type" v-model="training_type" required="">
                                <option disabled value="">Training Type</option>
                                <option value="Endurance">Endurance</option>
                                <option value="Strength Training">Strength Training</option>
                                <option value="Balance Focused">Balance Focused</option>
                                <option value="Flexibility Focused">Flexibility Focused</option>
                            </select>
                        </div>
                    </div>
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
                            <input class="btn btn-primary" type="submit" value="add exercises">
                        </div>
                    </div>

                </form>
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
    </v-container>
</template>
<script>
 import myDatepicker from 'vue-datepicker'

 import axios from 'axios'
 import { login, userAuth } from '../auth/auth'



  export default {
    name: 'create-workout',
    data () {
      return {
      date: {
          time: ''
      },
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
      target_muscle: '',
      training_type: '',
      userAuth: userAuth,
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
            if (!this.date.time){ date = Date.now(); }
            else { date = this.date.time; }
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
        addWorkoutClick: function () {
            this.createWorkout = !this.createWorkout;
        },
        onSubmit: function (event) {
            var self = this;
            var baseURL = "http://127.0.0.1:8000/";

            var data = {
                title: this.title,
                date_for_completion: this.date.time,
                target_muscle: this.target_muscle,
                training_type: this.training_type,
                slug: this.slug,
                user: this.userAuth.user.id,
                exercises: [],
            };


            axios.post(baseURL + 'v1/workouts/', data)
                .then(function (response) {
                    self.snackbarMessage = "Successfully created your workout";
                    self.context = 'success';
                    self.snackbar = true;

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
      components: {
          'date-picker': myDatepicker
        }
}
</script>

<style>
    @media only screen and (max-width: 768px) {

        div > div.row-margin-top {
            margin: 0;
        }

    }

    input, select {
        display: inline-block;
        padding: 6px;
        line-height: 22px;
        font-size: 16px;
        border: 2px solid rgb(255, 255, 255);
        box-shadow: rgba(0, 0, 0, 0.2) 0px 1px 3px 0px;
        border-radius: 2px;
        color: rgb(95, 95, 95);
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