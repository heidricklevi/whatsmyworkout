<template>
    <v-layout row wrap>
        <v-flex xs12 offset-md1 md3>
                     <v-snackbar v-model="snackbar" :color="snackColor" :error="context === 'error'" :success="context === 'success'" :top="y === 'top'">
                            {{ snackbarText }}
                        </v-snackbar>

            <v-card v-if="recentWorkouts">
                <v-snackbar v-model="snackbar1" :error="context1 === 'error'" :success="context1 === 'success'" :top="y === 'top'">
                    {{ snackbarText1 }}
                </v-snackbar>
                <v-flex xs12>
                    <div class="pt-1 pl-1" style="display: inline-flex">
                        <v-avatar>
                            <img :src="userAuth.user.avatar">
                        </v-avatar>
                        <span class="title pl-2 pt-2 card-title grey--text">Next Workout </span>
                        <div style="position: absolute; right: 0; top: 0;">
                            <v-btn icon @click.native="isEmailWorkout = !isEmailWorkout" style="margin-right: 0">
                                <v-icon v-if="!isEmailWorkout">email</v-icon>
                                <v-icon class="red--text" v-if="isEmailWorkout">cancel</v-icon>
                            </v-btn>
                            <router-link to="/workout/edit/">
                                <v-btn icon class="mr-1" @click="commitToStore">
                                    <v-icon>edit</v-icon>
                                </v-btn>
                            </router-link>
                        </div>
                    </div>

                    <div style="margin-left: 15%; position:relative; top: -15px;">
                        <v-icon class="mr-1">event</v-icon>
                        <span class="caption">{{ recentWorkouts.date_for_completion | moment }}</span>
                    </div>
                </v-flex>

                    <v-card raised v-if="isEmailWorkout" style="border-color: lightslategray; border-bottom-width: 5px;
                                                            position: absolute; height: 200px; top: 50px; width: 100%; z-index: 2">

                        <form method="post" v-on:submit.prevent="sendWorkout">
                            <v-card-title>
                                Send this workout to someone else via email
                            </v-card-title>
                        <v-layout row>
                            <v-flex xs8 offset-xs2 md6 offset-md3>
                            <v-text-field v-model="shareEmail" label="@" type="email" :value="shareEmail" required></v-text-field>
                            </v-flex>
                            </v-layout>
                            <v-layout>
                            <v-flex md6 offset-md3>
                                <v-btn primary :loading="loading" type="submit" :disabled="loading" @click.native="loader = 'loading'">
                                    Send
                                    <span slot="loader" class="custom-loader">
                                        <v-icon>cached</v-icon>
                                    </span>
                                </v-btn>

                            </v-flex>
                                </v-layout>



                        </form>
                        </v-card>
                <v-divider></v-divider>
                <v-card-title>
                    <h3 class="headline">{{ recentWorkouts.title }}</h3>
                </v-card-title>
                <v-card-media id="workout-image" :src="recentWorkouts.workout_image" height="200px" contain>

                </v-card-media>
                <v-progress-circular style="position:absolute; top: 50%; right: 50%; "  v-if="loadingWorkout" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                <v-divider></v-divider>
                <v-card-actions>

                    <v-btn flat class="blue--text text--darken-4 pl-0 pt-0" @click.native="viewExercises = !viewExercises">View Exercises</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn icon @click.native="viewExercises = !viewExercises">
                        <v-icon class="blue--text text--darken-4">{{ viewExercises ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
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

                            <template v-for="(exercise, i) in recentWorkouts.exercises">


                                <v-list-tile style="padding: 0">
                                    <v-list-tile-content>
                                        <v-layout style="width: 100%" row wrap :key="exercise.exercise_name">


                                            <v-flex style="display: flex;" xs12>
                                                <v-flex xs1 class="ml-1">
                                                    <div style="text-align: center;">{{ i+1 }}.</div>
                                                </v-flex>
                                                <v-flex xs8 class="body-1" style="word-wrap: break-word">
                                                    {{ exercise.exercise_name }}
                                                </v-flex>
                                                <v-flex xs2 offset-xs1>
                                                    <div>{{ exercise.sets }}/{{ exercise.reps }}</div>
                                                </v-flex>
                                            </v-flex>
                                            <div style="position: relative; margin-left: 5%"><v-icon style="position: absolute; top: 0;" color=" ">fa-sticky-note-o</v-icon></div>
                                            <div class="caption" style="word-wrap: break-word; margin: 2% 0 0 5%;">
                                                {{ exercise.notes }}
                                            </div>
                                        </v-layout>
                                        <v-layout style="text-align: center">
                                            <div style="word-wrap: break-word; font-size: small; font-weight: 500">
                                                Lifting Weight: <span style="font-style: italic" class="caption">{{ exercise.lifting_weight }}</span></div>
                                        </v-layout>

                                    </v-list-tile-content>

                                </v-list-tile>
                                <v-divider></v-divider>
                            </template>
                        </v-list>
                    </v-card-text>
                </v-slide-y-transition>
            </v-card>
         <v-card v-else="recentWorkouts">
                <v-card-text>
                    No workouts have been created. Head on over <router-link to="/create-workout/">here</router-link> to create your workouts and see the recently scheduled one show up here
                </v-card-text>
            </v-card>
        </v-flex>
        <v-flex xs12  offset-md1 md3>
            <v-card>
                <v-card-title primary-title>
                    <div>
                        <h3 class="headline mb-0">Find Friends or Follow Experts</h3>
                    </div>
                </v-card-title>
                <v-container fluid>
                    <v-layout>
                      <v-flex xs12 offset-md1 md10>
                        <v-text-field
                          label="Async items"
                          append-icon="search"
                          :loading="loading"

                          required
                          :items="items"
                          @keyup="search = $event.target.value"
                          v-model="select"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>
                </v-container>
              <v-layout>
                <v-flex xs12 offset md1 md12 v-if="items" >
                    <v-list subheader>
                  <v-subheader>Results</v-subheader>
                 <template v-for="item in items">

                    <v-list-tile avatar  v-bind:key="item.id"  @click="">
                      <v-list-tile-avatar>
                        <img v-bind:src="item.avatar"/>
                      </v-list-tile-avatar>
                      <v-list-tile-content>
                        <v-list-tile-title class="blue-grey--text">{{ item.username }}</v-list-tile-title>
                      </v-list-tile-content>
                      <v-list-tile-action>

                      </v-list-tile-action>

                    </v-list-tile>
                     <v-divider></v-divider>
                     </template>
                    </v-list>

                </v-flex>

              </v-layout>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import axios from 'axios'
import moment from 'moment'
import { devServer, baseURLLocal} from '../auth/auth-utils'


export default {
    name: 'user-dashboard',
  data () {
    return {
      search: null,
      select: [],
      items: [],
      recentWorkouts: {},
      userAuth: this.$store.state.userAuth,
      viewExercises: false,
      drawer: true,
      isEmailWorkout: false,
      isArchiveWorkout: false,
      nextWorkout: false,
      shareEmail: '',
      loader: null,
      loading: false,
      snackbar: false,
      snackbarText: ' ',
      y: 'top',
      context: '',
      context1: '',
      loadingWorkout: true,
      snackbar1: false,
      snackbarText1: '',
      snackColor: '',

    }
  },
    watch: {
      search (val) {
          val && this.resolveSearch(val)
          if (!val){
              this.items = null;
          }
      }
    },
    filters: {
        moment: function (date) {
            return moment(date).format("dddd, MMMM Do YYYY");
        }
    },
    props: ["computedAuth"],
    methods: {
        resolveSearch (queryVal) {

            this.loading = true;
            var that = this;
            axios.get(baseURLLocal+'v1/users/find?search='+queryVal).then(function (response) {

                for (var i = 0; i < response.data.results.length; i++) {
                    that.items[i] = response.data.results[i];

                    console.log(that.items[i]);
                }

                that.loading = false;
            }).catch(function (err) {
                that.loading = false;

            })

        },
        commitToStore: function () {
          this.$store.commit('setData', [this.recentWorkouts]);
          console.log("Commited to store");
        },
        sendWorkout: function () {
            var self = this;
            var payload = this.recentWorkouts;

            for (var i =0; i < payload.exercises.length; i++) {
                payload.exercises[i].workout_id = this.recentWorkouts.id;
            }

            payload.to = this.shareEmail;

            this.loading = true;
            axios.post(baseURLLocal+'v1/workout/send/', payload)
                .then(function () {
                    self.context = 'success';
                    self.snackbar = true;
                    self.snackbarText = "Successfully sent workout to "+payload.to;
                    self.snackColor = 'green';

                    self.loading = false;
                    console.log('Success')
            }).catch(function (err) {
                    self.context = 'error';
                    self.snackbar = true;
                    self.snackbarText = "Could not send workout to "+payload.to +"error " + err;

                    self.loading = false;
                    console.log(err)
            })
        }
    },
    created: function () {
            var self = this;


            this.loadingWorkout = true;

            axios.get(baseURLLocal+'v1/workouts/?recent=5').then(function (response) {
                self.recentWorkouts = response.data.results[0];
                self.loadingWorkout = false;



                console.log(self.recentWorkouts);
            }).catch(function (e) {
                self.loadingWorkout = false;
                self.context1 = 'error';
                self.snackbar1 = true;
                self.snackbarText1 = "error loading workout";
                console.log('There was an error loading recent workouts');
            });


      },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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

    .card > .card__title {
        display: block;
    }

    .card-title {
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0;
    }

</style>
