<template>
    <div>

        <v-layout v-if="selectedWorkout">

            <v-flex md5 offset-md1>
                <v-card>
                <v-snackbar v-model="snackbar" :error="context === 'error'" :success="context === 'success'" :top="y === 'top'">
                    {{ snackbarText }}
                </v-snackbar>
                     <v-tooltip v-model="show" top style="float: right; opacity: 1; z-index: 150">
                      <v-btn icon slot="activator">
                        <v-icon color="grey lighten-1" style="opacity: 1">help_outline</v-icon>
                      </v-btn>
                      <span class="caption">Click on the fields to edit this workout; then click save edits.</span>
                        </v-tooltip>

                    <v-layout>
                        <v-avatar class="ma-3" style="display: inline-flex;">
                            <img :src="userAuth.user.avatar">
                        </v-avatar>

                    </v-layout>
                     <span class="subheading mt-0" style="position: absolute; top: 5px; left: 65px">{{ userAuth.user.username }}</span>
                    <v-menu lazy :close-on-content-click="false"
                            v-model="updateDate"
                            transition="scale-transition"
                            offset-y
                            full-width
                            :nudge-right="40"
                            max-width="295px"
                            style="top: -25px">
                        <div slot="activator"
                         v-model="tmp.date_for_completion"
                         label="edit date"
                         style="position: absolute; left: 60px; top: 20%;"
                         @click="updateDate = !updateDate">
                        <v-icon class="pr-1">event</v-icon>
                        {{ tmp.date_for_completion }}</div>
                        <v-date-picker v-model="tmp.date_for_completion" no-title  actions>
                            <template slot-scope="{ save, cancel }">
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn primary @click.native="updateDate = !updateDate">Cancel</v-btn>
                                    <v-btn primary @click.native="updateDate = !updateDate">Save</v-btn>
                                </v-card-actions>
                            </template>
                        </v-date-picker>
                    </v-menu>
                    <v-card-title >
                        <h3 class="headline mb-0" @click="updateTitle = !updateTitle">{{ tmp.title }}</h3>
                    </v-card-title>
                    <v-card raised v-if="updateTitle" style="position:absolute; width: 100%; top: 0px">
                         <v-flex xs12>
                            <v-text-field
                                v-model="tmp.title"
                                name="input-1"
                                label="Update Title"
                                id="title"
                            ></v-text-field>
                            <v-btn primary @click="save">save</v-btn>
                        </v-flex>
                    </v-card>
                    <v-card-media :src="tmp.workout_image" contain height="250px"></v-card-media>
                    <v-card-actions>
                        <v-btn flat class="blue--text text--darken-4 pl-0 pt-0" @click.native="viewExercises = !viewExercises">View Exercises</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn icon @click.native="viewExercises = !viewExercises">
                            <v-icon>{{ viewExercises ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
                        </v-btn>
                    </v-card-actions>
                    <v-slide-y-transition>
                        <v-card-text v-if="viewExercises">
                            <v-list three-line subheader>
                            <v-layout row justify-center>
                                <v-flex xs6>
                                    <v-subheader>Exercise</v-subheader>
                                </v-flex>
                                <v-flex xs3 offset-xs1>
                                    <v-subheader class="text-xs-center">sets/reps</v-subheader>
                                </v-flex>
                            </v-layout>

                            <template v-for="(exercise, index) in tmp.exercises" >
                                <v-list-tile>
                                    <update-exercise @click="updateExercise = !updateExercise" :exercise="exercise" :index="index"></update-exercise>
                                </v-list-tile>
                                <v-divider :key="exercise.id"></v-divider>
                            </template>
                            </v-list>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn primary :loading="loading" :disabled="loading" @click.native="saveEdits">
                                    Save Edits
                                    <span slot="loader" class="custom-loader">
                                        <v-icon>cached</v-icon>
                                    </span>
                                </v-btn>
                        </v-card-actions>

                    </v-slide-y-transition>
                </v-card>
            </v-flex>
        </v-layout>
        <v-alert v-else="selectedWorkout" error>Could not load the desired workout to edit</v-alert>
    </div>
</template>

<script>

import { userAuth, baseURLLocal } from '../auth/auth'
import axios from 'axios'
import moment from 'moment'
import updateExercise from './edit-exercise.vue'








export default {
    name: 'workout-detail',
  data () {
    return {
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


    }
  },

  computed: {

  },

  watch: {
  },
  methods: {
      save: function (e) {
        this.updateTitle = false;

      },
      saveEdits: function () {
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
                    self.context = 'success';
                    self.snackbar = true;
                    self.snackbarText = "Successfully updated workout to ";

                    self.loading = false;

                    console.log('Success')
            }).catch(function (err) {
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarText = "Could not update workout "+"error " + err;

                    self.loading = false;

                    console.log(err)
            })
        },

  },

  mounted: function () {

      this.tmp.date_for_completion = moment(this.tmp.date_for_completion).format('YYYY-MM-DD');
  },
  components: {
      updateExercise
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
