<template>
    <v-layout row wrap>
        <v-flex xs12 offset-md1 md4>
            <v-card v-if="recentWorkouts">
                <v-flex xs12>
                    <div class="pt-1 pl-1" style="display: inline-flex">
                        <v-avatar>
                            <img :src="computedAuth.avatar">
                        </v-avatar>
                        <span class="title pl-2 pt-2 card-title grey--text">Next Workout </span>
                        <div style="position: absolute; right: 0; top: 0;">
                            <v-btn icon @click.native="isEmailWorkout = !isEmailWorkout" style="margin-right: 0">
                                <v-icon v-if="!isEmailWorkout">email</v-icon>
                                <v-icon class="red--text" v-if="isEmailWorkout">cancel</v-icon>
                            </v-btn>
                            <v-btn icon @click.native="isArchiveWorkout = !isArchiveWorkout" style="margin-right: 0">
                                <v-icon v-if="!isArchiveWorkout">archive</v-icon>
                            </v-btn>
                            <v-btn icon @click.native="nextWorkout = !nextWorkout" style="margin-left: 0">
                                <v-icon v-if="!nextWorkout">forward</v-icon>
                            </v-btn>
                        </div>
                    </div>

                    <div style="margin-left: 15%; position:relative; top: -15px;">
                        <v-icon class="mr-1">event</v-icon>
                        <span class="caption">{{ recentWorkouts.date_for_completion | moment }}</span>
                    </div>
                </v-flex>

                    <v-card raised v-if="isEmailWorkout" style="border-color: lightslategray; border-bottom-width: 5px">
                        <form method="post" v-on:submit.prevent="sendWorkout">
                            <v-card-title>
                                Send this workout to someone else via email
                            </v-card-title>
                        <v-layout row>
                            <v-flex xs8 offset-xs2 md6 offset-md3>
                            <v-text-field v-model="shareEmail" label="@" type="email" :value="shareEmail" required></v-text-field>
                            </v-flex>
                            <v-flex md6 offset-md3>
                                <v-btn primary type="submit">
                                    Send
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
                                    <v-divider></v-divider>
                                    <v-list-tile-content>
                                        <v-layout style="width: 100%" row wrap :key="exercise.exercise_name">

                                            <v-flex style="display: flex;" xs12>
                                                <v-flex xs1 class="ml-1">
                                                    <span class="text-grey text--darken-2" style="font-size: smaller; position: relative; left: -8px;">#{{ i }}</span>
                                                </v-flex>
                                                <v-flex xs8 class="body-1" style="word-wrap: break-word">
                                                    {{ exercise.exercise_name }}
                                                </v-flex>
                                                <v-flex xs2 offset-xs1>
                                                    <div>{{ exercise.sets }}/{{ exercise.reps }}</div>
                                                </v-flex>

                                            </v-flex>
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
         <v-card v-else="recentWorkouts">
                <v-card-text>
                    No workouts have been created. Head on over <router-link to="/create-workout/">here</router-link> to create your workouts and see the recently scheduled one show up here
                </v-card-text>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
import axios from 'axios'
import moment from 'moment'
import { devServer, baseURLLocal} from '../auth/auth'

export default {

  name: 'user-dashboard',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      recentWorkouts: {},
      viewExercises: false,
      drawer: true,
      isEmailWorkout: false,
      isArchiveWorkout: false,
      nextWorkout: false,
      shareEmail: '',

    }
  },
    filters: {
        moment: function (date) {
            return moment(date).format("dddd, MMMM Do YYYY");
        }
    },
    props: ["computedAuth"],
    methods: {
        sendWorkout: function () {
            var payload = this.recentWorkouts;

            for (var i =0; i < payload.exercises.length; i++) {
                payload.exercises[i].workout_id = this.recentWorkouts.id;
            }
            payload.workout_image = null;
            payload.to = this.shareEmail;





            console.log(payload);

            axios.post(baseURLLocal+'v1/workout/send/', payload)
                .then(function () {
                    console.log('Success')
            }).catch(function (err) {
                console.log(err)
            })
        }
    },
    mounted: function () {
            var self = this;

            axios.get(baseURLLocal+'v1/workouts/').then(function (response) {
                self.recentWorkouts = response.data.results[0];
                console.log(self.recentWorkouts);
            }).catch(function (e) {
                console.log('There was an error loading recent workouts');
            })
      },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .card > .card__title {
        display: block;
    }

    .card-title {
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0;
    }

</style>
