<template>
    <v-layout row wrap>
        <v-flex xs12 offset-md1 md4>
            <v-card>
                <v-flex xs12>
                    <div class="pt-1 pl-1" style="display: inline-flex">
                        <v-avatar>
                            <img :src="computedAuth.avatar">
                        </v-avatar>
                        <span class="title pl-2 pt-2 card-title grey--text">Next Workout </span>
                    </div>
                    <div style="margin-left: 15%; position:relative; top: -15px;">
                        <v-icon class="mr-1">event</v-icon>
                        <span class="caption">{{ recentWorkouts.date_for_completion | moment }}</span>
                    </div>
                </v-flex>
                <v-divider></v-divider>
                <v-card-title>
                    <h3 class="headline">{{ recentWorkouts.title }}</h3>
                </v-card-title>
                <v-card-media src="src/assets/img/chest-muscle.jpg" height="200px" contain>

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
        </v-flex>
    </v-layout>
</template>
<script>
import axios from 'axios'
import moment from 'moment'

export default {

  name: 'user-dashboard',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      recentWorkouts: {},
      viewExercises: false,
      drawer: true,
    }
  },
    filters: {
        moment: function (date) {
            return moment(date).format("dddd, MMMM Do YYYY");
        }
    },
    props: ["computedAuth"],
    methods: {

    },
    mounted: function () {
            var self = this;
            var baseURL = 'http://127.0.0.1:8000/v1/workouts/';
            axios.get(baseURL).then(function (response) {
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
