<template>
    <v-layout row wrap>
        <v-flex md4 offset-md1 xs12>
            <h6 class="headline grey--text ">Body Progress Tracking</h6>
            <v-card >
                <v-card-media height="290px" :src="userAuth.user.avatar">
                </v-card-media>
                <v-card-text>
                    <h6 class="title grey--text text--darken-2">Most Recent Stats</h6>
                    <p class="text-xs-right caption grey--text text--lighten-1">{{ currentBodyStats.created }}</p>
                    <v-flex xs2 offset-xs9>
                        <v-btn color="primary" class="pr-1"
                               block
                               small
                               outline
                               flat
                               @click="edit = !edit">
                            Change
                            <v-icon right small class="pr-2">edit</v-icon>
                        </v-btn>
                    </v-flex>
                </v-card-text>
                <v-dialog v-model="edit" persistent max-width="500px" transition="dialog-bottom-transition" :fullscreen="$vuetify.breakpoint.smAndDown">
                      <v-card>
                          <v-alert :color="color" icon="check_circle" :value="alertVal">
                            {{ alertText }}
                        </v-alert>
                        <v-card-title>
                          <span class="headline">Update Your Profile Stats</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container grid-list-md>
                                <v-form ref="form">
                                    <v-layout wrap>
                                        <v-flex xs12 md6>
                                                         <v-text-field

                                                                  suffix="in."
                                                                  label="Height"
                                                                  type="number"
                                                                  v-model="newStats.height"
                                                          ></v-text-field>
                                        </v-flex>

                                        <v-flex xs12 md6>
                                            <v-text-field
                                                              suffix="lbs."
                                                              label="Weight"
                                                              type="number"
                                                              v-model="newStats.weight"
                                                              ></v-text-field>
                                        </v-flex>

                                        <v-flex xs12 md6>
                                            <v-text-field
                                                              disabled
                                                              label="BMI"
                                                              type="number"
                                                              v-model="newStats.bmi"
                                                              persistent-hint
                                                              hint="Automatically calculated based on profile data"
                                                              ></v-text-field>
                                        </v-flex>

                                        <v-flex xs12 md6>
                                            <v-text-field
                                                              suffix="%"
                                                              label="Body Fat"
                                                              type="number"
                                                              v-model="newStats.body_fat"
                                                              ></v-text-field>
                                        </v-flex>

                                    </v-layout>
                                </v-form>

                            </v-container>
                        </v-card-text>

                          <v-card-actions>
                              <v-btn color="orange" flat outline @click.native="closeDialog">Close</v-btn>
                              <v-btn color="primary" flat @click.native="submitChange">Update</v-btn>
                          </v-card-actions>
                      </v-card>
                </v-dialog>

                 <v-layout v-if="!loading">
                    <v-flex xs6 text-xs-right style="border-right: 1px solid grey" class="pr-3 mr-3">
                        <p class="blue-grey--text text--lighten-2">Height</p>
                        <p class="blue-grey--text text--lighten-2">Weight</p>
                        <p class="blue-grey--text text--lighten-2">BMI</p>
                        <p class="blue-grey--text text--lighten-2">Body Fat</p>
                    </v-flex>
                    <v-flex xs6>
                        <p class="blue-grey--text text--darken-2" >{{ currentBodyStats.height | heightDisplay}}</p>
                        <p class="blue-grey--text text--darken-2" >{{ currentBodyStats.weight }} lbs.</p>
                        <p class="blue-grey--text text--darken-2" >{{ currentBodyStats.bmi }}</p>
                        <p class="blue-grey--text text--darken-2" >{{ currentBodyStats.body_fat }} %</p>
                    </v-flex>
                 </v-layout>
                <v-layout v-if="loading">
                    <v-flex xs12 offset-xs6>
                        <v-progress-circular indeterminate :size="70" :width="7" color="primary"></v-progress-circular>
                    </v-flex>
                </v-layout>
            </v-card>
        </v-flex>

        <v-flex offset-md1 md5 xs12>
            <v-card class="pa-2">

                <body-progress-chart :graphLabels="getGraphLabels"
                                     :chart-data="getGraphData"
                                     :weight-data="getWeightGraphData">

                </body-progress-chart>

            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import { baseURLLocal} from '../auth/auth-utils'
    import BodyProgressChart from '../components/body-progress-chart.vue'


    export default {
        name: "profile-stat-tracking-detail",
        data () {

            return {
                loading: false,
                userAuth: this.$store.state.userAuth,

                currentBodyStats: {},
                bodyStats: [],

                newStats: this.$store.state.data,
                disabled: false,
                edit: false,


                color: 'success',
                alertVal: false,
                alertText: '',


                graphData: [],
                graphLabels: [],
                graphWeightData: [],



            }
        },

        filters: {

            heightDisplay: function (hInches) {

                return Math.floor(hInches / 12).toString() + '\'' + ' '+ (hInches%12).toString()+'\'\'';
            }

        },
        watch: {

        },
        computed: {
            computedClass: function () {

                return this.edit? 'offset-xs6': 'text-xs-left';

            },

            getGraphLabels: function () {
                return this.graphLabels
            },

            getGraphData: function () {
                return this.graphData
            },

            getWeightGraphData: function () {
                return this.graphWeightData
            }





        },
        methods: {

            closeDialog: function () {
                this.fetchGraphData();
                this.edit = false;
                this.alertVal = false;





            },
            submitChange: function () {

                let payload = this.newStats;
                payload.bmi = Object.hasOwnProperty.call(this.newStats, 'bmi')? this.newStats.bmi: 0;
                payload.profile = Object.hasOwnProperty.call(this.newStats, 'profile')? this.newStats.profile: this.userAuth.user.profile_id;

                axios.post(baseURLLocal+ 'v1/body-stats/', payload).then(response => {
                    this.alertVal = true;
                    this.alertText = 'Success! Your changes have been updated';
                    this.color = 'success';

                    this.$store.commit('setData', response.data[0]);

                }).catch(err => {

                    this.alertVal = true;
                    this.alertText = 'Error Submitting Changes: '+err.message;
                    this.color = 'error';

                    console.log(err);

                })


            },

            fetchGraphData () {
                let tempLabels = [];
                let tempData = [];
                let tempWeightData = [];

                axios.get(baseURLLocal+'v1/body-stats/').then(response =>{
                    this.loading = false;
                    let results = response.data.results;

                    for (let i = 0; i < results.length; i++) {
                        tempLabels[i] = moment(results[i].created).format("MMM Do YY");
                        tempData[i] = results[i].body_fat;
                        tempWeightData[i] = results[i].weight;

                    }


                    this.bodyStats = results;

                    this.currentBodyStats = results[0]; //get most recent stats
                    this.currentBodyStats.created = moment(results[0].created).format("MMM Do YY, h:m a");

                    this.$store.commit('setData', results[0]);


                    this.graphLabels = tempLabels.reverse();
                    this.graphData = tempData.reverse();
                    this.graphWeightData = tempWeightData.reverse();



                }).catch(function (err) {

                    this.alertVal = true;
                    this.alertText = 'Error Fetching Data: '+err.message;
                    this.color = 'error';
                    console.log(err);
                })



            },

        },
        mounted: function () {
            this.loading = true;
            this.fetchGraphData();


        },

        components: {BodyProgressChart}

    }
</script>

<style scoped>
    .badge {
        background-color: inherit!important;
    }


</style>