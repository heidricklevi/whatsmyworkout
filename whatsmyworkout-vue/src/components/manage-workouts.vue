<template>
    <div>


                <v-alert error v-model="alertError">Could not load calendar error</v-alert>
            <template>
                <vue-event-calendar :events="scheduledEvents" @month-changed="changeMonth">
                    <template scope="props">
                        <v-progress-circular style="" v-if="loading"
                                             indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
                        <div v-for="(event, index) in props.showEvents" class="event-item">
                            <h5 class="mb-0">{{ event.title }}</h5>
                            <div class="subheading mb-2">{{ event.date | moment }}</div>
                            <div v-for="(exercise, index) in event.desc">
                                #{{ index }} <span>{{ exercise.exercise_name }}</span><span style="margin-left: 4%">{{ exercise.sets }}x{{ exercise.reps }}</span>
                                <div style="margin: 0 0 3% 0;"><span style="font-size: small; font-style: italic; color: #1d1e1f">Notes: </span>{{ exercise.notes }}</div>

                                <v-divider></v-divider>
                            </div>
                        </div>
                    </template>
                </vue-event-calendar>
            </template>
        </div>
</template>

<script>
import moment from 'moment'
import {baseURLLocal} from '../auth/auth-utils'


import axios from 'axios'




    export default {

        name: 'manage-workouts',
        data () {
            return {
                scheduledEvents: [{
                    title: 'dafsdf',
                    date: '2017/09/23',
                    desc: 'blah'
                },],
                scheduledWorkouts: [{}],
                alertError: false,
                currenCalWeek: [],
                currentCalFullWeekDate: [],
                currentWeekWorkouts: [],
                loading: false
            }
        },
        filters: {
            moment: function (date) {
                date = date.replace(/\//g, '-');
                return moment(date).format("dddd, MMMM Do YYYY");
            }
        },
        computed: {
          currentWeek: function () {
              var cal = calendar().of(moment().weekYear(), moment().month());
              var dayOfMonth = moment().date();

              for (var i = 0; i < cal.calendar.length; i++) {
                  for (var j = 0; j < cal.calendar[i].length; j++){
                      if (dayOfMonth === cal.calendar[i][j]){
                            this.currentCalWeek = cal.calendar[i];
                            return cal.calendar[i]
                        }
                  }

              }
          },
          currentMonth: function () {
              return moment().get('month') + 1;
          },
          currentCalendar: function () {
              return calendar().of(moment().weekYear(), moment().month())
          },
          scheduledWorkout: function () {
              var weekArr = this.currentCalWeek;
              var newWeekArr = this.getFullWeekDate(weekArr, moment().get('month') + 1 );
              var scheduledWorkouts = this.scheduledWorkouts;

              for (var i = 0; i < scheduledWorkouts.length; i++) {
                  for (var j = 0; j < newWeekArr.length; j++) {
                      if (scheduledWorkouts[i].date_for_completion === newWeekArr[j]) {
                          this.currentWeekWorkouts.push(scheduledWorkouts[i])
                      }
                  }

              }


          }

        },
        methods: {
            getFullWeekDate: function (currentWeekArr, month) {
                var fullWeekDate = [];
                var year = moment().weekYear();

                if (month < 10) {
                    month = '0'+month.toString();
                }

                for (var i = 0; i < currentWeekArr.length; i++){
                    fullWeekDate[i] = year + '-' + month + '-' + currentWeekArr[i];
                }
                this.currentCalFullWeekDate = fullWeekDate;
                return fullWeekDate;
            },
            changeMonth: function (month) {
                var self = this;
                month = month.substring(0, 2);

                this.loading = true;
                axios.get(baseURLLocal + 'v1/workouts/?month=' + month)
                .then(function (response) {
                    self.scheduledWorkouts = response.data.results;
                    for (var i = 0; i < self.scheduledWorkouts.length; i++) {
                        if (!self.scheduledEvents[i]){self.scheduledEvents[i] = {}}
                        self.scheduledEvents[i].id = self.scheduledWorkouts[i].id;
                        self.scheduledEvents[i].desc = self.scheduledWorkouts[i].exercises;
                        self.scheduledEvents[i].title = self.scheduledWorkouts[i].title;
                        self.scheduledEvents[i].date = moment(self.scheduledWorkouts[i].date_for_completion).format('YYYY/MM/DD');
                    }

                    self.loading = false;
                    console.log(self.scheduledEvents);
                    console.log(response.data)
                }).catch(function (error) {

                    self.loading = false;

                  if (error.response) {
                      // The request was made and the server responded with a status code
                      // that falls out of the range of 2xx

                      self.alertError = true;
                      console.log(error.response.data);
                      console.log(error.response.status);
                      console.log(error.response.headers);
                  } else if (error.request) {
                      // The request was made but no response was received
                      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                      // http.ClientRequest in node.js
                      self.alertError = true;
                      console.log(error.request);
                  } else {
                      // Something happened in setting up the request that triggered an Error

                      self.alertError = true;
                      console.log('Error', error.message);
                  }

                  console.log(error.config);
              });
            }

        },
        components: {


        },

        mounted: function () {
            var month = moment().get('month') + 1;
            var self = this;

            self.scheduledEvents = [{
                title: ' ',
                date: ' '
            },];

            this.loading = true;
            axios.get(baseURLLocal + 'v1/workouts/?month=' + month)
                .then(function (response) {
                    self.scheduledWorkouts = response.data.results;
                    for (var i = 0; i < self.scheduledWorkouts.length; i++) {
                        if (!self.scheduledEvents[i]){self.scheduledEvents[i] = {}}
                        self.scheduledEvents[i].id = self.scheduledWorkouts[i].id;
                        self.scheduledEvents[i].desc = self.scheduledWorkouts[i].exercises;
                        self.scheduledEvents[i].title = self.scheduledWorkouts[i].title;
                        self.scheduledEvents[i].date = moment(self.scheduledWorkouts[i].date_for_completion).format('YYYY/MM/DD');
                    }


                    self.loading = false;
                    console.log(self.scheduledEvents);
                    console.log(response.data)
                }).catch(function (error) {

                    self.loading = false;

                  if (error.response) {
                      // The request was made and the server responded with a status code
                      // that falls out of the range of 2xx

                      self.alertError = true;
                      console.log(error.response.data);
                      console.log(error.response.status);
                      console.log(error.response.headers);
                  } else if (error.request) {
                      // The request was made but no response was received
                      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                      // http.ClientRequest in node.js
                      self.alertError = true;
                      console.log(error.request);
                  } else {
                      // Something happened in setting up the request that triggered an Error

                      self.alertError = true;
                      console.log('Error', error.message);
                  }

                  console.log(error.config);
              });

        }
    }

</script>

<style>

</style>