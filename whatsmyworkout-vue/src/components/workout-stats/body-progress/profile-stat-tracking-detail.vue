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
                    <v-flex xs4 text-xs-right>
                        <v-btn color="primary"
                               class="text-xs-right"
                               block
                               small
                               outline
                               flat
                               @click="edit = !edit">
                            Change
                            <v-icon right small>edit</v-icon>
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
                                <v-form ref="form" v-model="valid">
                                    <v-layout wrap>
                                        <v-flex xs12 md6>
                                                         <v-text-field

                                                                  suffix="in."
                                                                  label="Height"
                                                                  type="number"
                                                                  v-model="newStats.height"
                                                                  :rules="[rules.required, rules.validHeightInInches]"

                                                          ></v-text-field>
                                        </v-flex>

                                        <v-flex xs12 md6>
                                            <v-text-field
                                                              suffix="lbs."
                                                              label="Weight"
                                                              v-mask="['###.#', '##.#']"
                                                              v-model="newStats.weight"
                                                              return-masked-value
                                                              :rules="[rules.required]"
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
                                                              v-mask="['##.#', '#.#']"
                                                              v-model="newStats.body_fat"
                                                              return-masked-value
                                                              ></v-text-field>
                                        </v-flex>

                                    </v-layout>
                                </v-form>

                            </v-container>
                        </v-card-text>

                          <v-card-actions>
                              <v-btn color="orange" flat outline @click.native="closeDialog">Close</v-btn>
                              <v-btn color="primary" flat @click.native="submitChange" :disabled="disabled">Update</v-btn>
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

        <v-flex offset-md1 md5 xs12 :class="{'mt-4': $vuetify.breakpoint.smAndDown}">
            <v-card class="pa-2">

                <body-progress-chart :graphLabels="getGraphLabels"
                                     :chart-data="getGraphData"
                                     :weight-data="getWeightGraphData">

                </body-progress-chart>

            </v-card>
             <v-flex xs12 class="mt-4">
                <v-data-table
                    :headers="headers"
                    :items="bodyStats"
                    :loading="loadingTable"
                    class="elevation-1"
                  >
                    <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>
                    <template slot="items" slot-scope="props">
                      <td class="text-xs-left">{{ props.item.created }}</td>
                      <td class="text-xs-left">{{ props.item.weight }}</td>
                      <td class="text-xs-left">{{ props.item.body_fat }}</td>
                        <td class="text-xs-center">
                          <v-btn icon @click="removeDialog(props.item)">
                              <v-icon color="error">
                                  remove_circle
                              </v-icon>
                          </v-btn>
                      </td>
                        <v-dialog
                                width="750"
                                v-model="deleteDialog">
                            <v-card>
                                <v-card-title>Remove Body Stat</v-card-title>
                                <v-card-text>Are you sure you wish to remove this body stat?</v-card-text>
                                <v-card-actions>
                                    <v-btn flat @click="deleteDialog = false">Close</v-btn>
                                    <v-btn flat :disabled="deleteDisabled" class="orange--text" @click="removeConfirm">Delete</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </template>
                  </v-data-table>
             </v-flex>

        </v-flex>

    </v-layout>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import { baseURLLocal} from '../../../auth/auth-utils'
    import BodyProgressChart from './body-progress-chart.vue'
    import { mask } from 'vue-the-mask'


    export default {
        name: "profile-stat-tracking-detail",
        directives: {mask},
        data () {

            return {

                rules: {

                    required: (val) => !!val || 'Cannot be blank.',
                    validHeightInFeet: (val) => (val > 1 && val < 8) || 'Enter a valid number between 2-7',
                    validHeightInInches: (val) => (val > 0 && val <= 90) || 'Enter a valid number for Height in inches.',
                },
                valid: false,


                loading: false,
                userAuth: this.$store.state.userAuth,

                currentBodyStats: {},
                bodyStats: [],

                newStats: this.$store.state.data,
                disabled: true,
                edit: false,


                color: 'success',
                alertVal: false,
                alertText: '',


                graphData: [],
                graphLabels: [],
                graphWeightData: [],

                loadingTable: false,
                headers: [

                     {
                        text: 'Date',
                        value: 'created',
                         class: 'pt-4'
                    },

                    {
                        text: 'Weight (lbs.)',
                        value: 'weight',
                        sortable: false,
                        class: 'theader-padding'
                    },
                    {
                        text: 'Body Fat (%)',
                        value: 'body_fat',
                        sortable: false,
                        class: 'theader-padding'
                    },

                    {
                        text: 'Actions',
                        align: 'left',
                        sortable: false,
                        class: 'theader-padding'

                    },
                ],

                deleteDialog: false,
                deleteStat: false,
                deleteDisabled: false,

                statToDelete: null,






            }
        },

        filters: {
            moment(date) {
                return moment(date).format("MMM Do YY");
            },
            heightDisplay: function (hInches) {

                return Math.floor(hInches / 12).toString() + '\'' + ' '+ (hInches%12).toString()+'\'\'';
            }

        },
        watch: {
            valid() {
                this.disabled = !this.valid;
            }
        },
        computed: {
            bodyStatToBeRemoved: {
                get() {
                    return this.statToDelete
                },
                set(stat) {
                    this.statToDelete = stat;
                }
            },
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

            removeDialog(bodyStat) {
                this.bodyStatToBeRemoved = bodyStat;
                this.deleteDialog = true;
            },

            removeConfirm() {
                let item = this.bodyStatToBeRemoved;
                console.log(item);
                this.deleteDisabled = true;
                axios.delete(baseURLLocal+'v1/body-stats/'+item.id+'/', { params: { id: item.id} } ).then(response => {
                        console.log(response);
                        this.deleteDialog = false;
                        this.deleteDisabled = false;
                        this.fetchGraphData();

                    }).catch(err => {
                        this.deleteDisabled = false;
                        console.log(err);

                    });
            },




            closeDialog: function () {
                this.fetchGraphData();
                this.edit = false;
                this.alertVal = false;
                this.$refs.form.reset();


            },
            submitChange: function () {

                this.disabled = true;
                let payload = this.newStats;
                payload.bmi = Object.hasOwnProperty.call(this.newStats, 'bmi')? this.newStats.bmi: 0;
                payload.profile = Object.hasOwnProperty.call(this.newStats, 'profile')? this.newStats.profile: this.userAuth.user.profile_id;

                axios.post(baseURLLocal+ 'v1/body-stats/', payload).then(response => {
                    this.alertVal = true;
                    this.alertText = 'Success! Your changes have been updated';
                    this.color = 'success';
                    this.disabled = false;

                    this.$store.commit('setData', response.data[0]);

                }).catch(err => {

                    this.disabled = false;
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
                this.loadingTable = true;
                axios.get(baseURLLocal+'v1/body-stats/').then(response =>{
                    this.loading = false;
                    this.loadingTable = false;
                    let results = response.data.results;

                    for (let i = 0; i < results.length; i++) {
                        tempLabels[i] = moment(results[i].created).format("MMM Do YY");
                        tempData[i] = results[i].body_fat;
                        tempWeightData[i] = results[i].weight;

                    }


                    this.bodyStats = results;
                    this.bodyStats.map(b => {
                       b.created =  moment(b.created).format("MMM Do YY");
                    });

                    this.currentBodyStats = results[0]; //get most recent stats
                    //this.currentBodyStats.created = moment(results[0].created).format("MMM Do YY, h:m a");

                    this.$store.commit('setData', results[0]);


                    this.graphLabels = tempLabels.reverse();
                    this.graphData = tempData.reverse();
                    this.graphWeightData = tempWeightData.reverse();



                }).catch(err => {
                    this.loadingTable = false;
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

    .theader-padding {
        padding: 24px!important;
    }

</style>