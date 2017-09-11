<template>
    <v-layout row>
        <v-flex md6 xs12>
            <v-card>
                <v-card-title primary-title>
                    <div>
                    <h3 class="headline">September 2017</h3>
                    <div><h4 class="title">Week of 4 - 10</h4></div>
                    </div>
                </v-card-title>
                <v-divider></v-divider>
                <v-layout class="ml-0 mr-0">
                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-right: solid 1px black; border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">4</span>
                    </div>
                </v-flex>

                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-right: solid 1px black; border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">5</span>
                    </div>
                </v-flex>
                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">6</span>
                    </div>
                </v-flex>
                    </v-layout>
                            <v-layout class="ml-0 mr-0">
                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-bottom: 1px solid black; border-right: solid 1px black; height: 100px;">
                        <div>
                            <span style="display: inline-block" class="pa-2">7</span>
                        </div>
                    </div>
                </v-flex>

                <v-flex md4 class="pl-0 pr-0">
                    <div style="border-right: solid 1px black; border-bottom: 1px solid black; height: 100px;">
                        <span style="display: inline-block" class="pa-2">8</span>
                    </div>
                </v-flex>
                <v-flex md4 class="pl-0 pr-0">
                    <div  style="height: 100px; border-bottom: 1px solid black;">
                        <span style="display: inline-block" class="pa-2">9</span>
                        {{ currentWeek }}
                    </div>
                </v-flex>
                    </v-layout>
                <v-layout class="ml-0 mr-0">
                    <v-flex md4 xs4 class="pl-0 pr-0">
                        <div  style="height: 100px;  border-right: 1px solid black;">
                        <span style="display: inline-block" class="pa-2">10</span>
                    </div>
                    </v-flex>
                </v-layout>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
import moment from 'moment'
import calendar from 'calendar-js'



    export default {

        name: 'manage-workouts',
        data () {
            return {

            }
        },
        computed: {
          currentWeek: function () {
              var cal = calendar().of(moment().weekYear(), moment().month());
              var dayOfMonth = moment().date();

              for (var i = 0; i < cal.calendar.length; i++) {
                  for (var j = 0; j < cal.calendar[i].length; j++){
                      if (dayOfMonth === cal.calendar[i][j]){
                            return cal.calendar[i]
                        }
                  }

              }
          },

        },
        methods: {


        },
        components: {

        }
    }

</script>

<style>

</style>