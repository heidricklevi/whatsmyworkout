<template>
    <v-layout row>
        <v-flex md6 xs12>
            <v-card>
                <v-alert error v-model="alertError">Could not load calendar error</v-alert>
                <v-card-title primary-title>
                    <div>
                    <h3 class="headline">{{ currentCalendar.month }} {{ currentCalendar.year }}</h3>
                   <h4 class="title">Week of {{ currentMonth }}/{{ currentWeek[0] }} - {{ currentMonth }}/{{ currentWeek[currentWeek.length - 1]  }}</h4></div>

                </v-card-title>
                <v-divider></v-divider>
                <v-layout class="ml-0 mr-0">
                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-right: solid 1px black; border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">{{ currentWeek[0] }}</span><span>{{currentCalendar.weekdaysAbbr[0]}}</span>
                    </div>
                </v-flex>

                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-right: solid 1px black; border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">{{ currentWeek[1] }}</span><span>{{currentCalendar.weekdaysAbbr[1]}}</span>
                    </div>
                </v-flex>
                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">{{ currentWeek[2] }}</span><span>{{currentCalendar.weekdaysAbbr[2]}}</span>
                    </div>
                </v-flex>
                    </v-layout>
                            <v-layout class="ml-0 mr-0">
                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-bottom: 1px solid black; border-right: solid 1px black; height: 100px;">
                        <div>
                            <span style="display: inline-block" class="pa-2">{{ currentWeek[3] }}</span><span>{{currentCalendar.weekdaysAbbr[3]}}</span>
                        </div>
                    </div>
                </v-flex>

                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-right: solid 1px black; border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">{{ currentWeek[4] }}</span><span>{{currentCalendar.weekdaysAbbr[4]}}</span>
                    </div>
                </v-flex>
                <v-flex md4 class="pl-0 pr-0">
                    <div  style="height: 100px; border-bottom: 1px solid black;">
                        <span style="display: inline-block" class="pa-2">{{ currentWeek[5] }}</span><span>{{currentCalendar.weekdaysAbbr[5]}}</span>
                    </div>
                </v-flex>
                    </v-layout>
                <v-layout class="ml-0 mr-0">
                    <v-flex md4 xs4 class="pl-0 pr-0">
                        <div  style="height: 100px;  border-right: 1px solid black;">
                        <span style="display: inline-block" class="pa-2">{{ currentWeek[6] }}</span><span>{{currentCalendar.weekdaysAbbr[6]}}</span>
                         {{ scheduledWorkout }}
                    </div>
                    </v-flex>
                </v-layout>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
import moment from 'moment'
import baseURLLocal from '../auth/auth'
import calendar from 'calendar-js'
import axios from 'axios'




    export default {

        name: 'manage-workouts',
        data () {
            return {
                scheduledWorkouts: {},
                alertError: false,
                currenCalWeek: [],
                currentCalFullWeekDate: [],
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
                          console.log('They match! ' + scheduledWorkouts[i] + ' ' + newWeekArr[j]);
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
            }

        },
        components: {


        },

        mounted: function () {
            var month = moment().get('month') + 1;
            var baseURL = 'http://127.0.0.1:8000/';
            var self = this;

            axios.get(baseURL + 'v1/workouts/?month=' + month)
                .then(function (response) {
                    self.scheduledWorkouts = response.data.results;
                    console.log(response.data)
                }).catch(function (error) {
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