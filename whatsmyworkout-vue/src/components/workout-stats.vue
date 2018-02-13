<template>
    <v-layout row wrap>
        <v-flex xs12 md4 :class="{'mb-4': $vuetify.breakpoint.smAndDown, 'ml-3': $vuetify.breakpoint.mdAndUp}">
            <v-card>
                <v-card-title primary-title>
                    <h3 class="headline mb-0">Max Lift Tracking</h3>
                    <div class="mb-3" style="float: right">
                        <v-btn icon @click="dialogSet()">
                            <v-icon>add</v-icon>
                        </v-btn>
                        <add-max-lift-tracking v-if="dialog"></add-max-lift-tracking>

                    </div>
                </v-card-title>
                <span class="ml-4 grey--text">Core Muscle Groups Tracked</span>
                <span class="caption grey--text text--lighten-1 mr-3 mt-3" style="font-style: italic; float: right;"></span>


                <v-divider></v-divider>
                <v-layout>
                    <v-flex md4 offset-1 xs10>
                            <v-select class="mt-0 blue-grey--text text--darken-2"
                                      v-bind:items="target_muscles" v-model="selectedMuscle" label="Choose Muscle"></v-select>
                    </v-flex>
                </v-layout>
                <v-layout class="ma-4" v-if="isLoading">
                        <v-flex offset-4 xs9>
                             <v-progress-circular indeterminate v-bind:size="60" v-bind:width="5" color="primary"></v-progress-circular>
                        </v-flex>
                </v-layout>

                    <render-max-data :isLoading="getLoadingStatus" :max-lifts="getMaxLiftsObjects"></render-max-data>
            </v-card>
        </v-flex>
        <v-flex xs12 md6 offset-md1>
            <v-card class="pa-2">
                <v-alert outline color="error" icon="warning" :value="noResults">
                        Chart Data not loaded. Please ensure you have recorded a Max for this target muscle.
                </v-alert>
                <lift-progress-chart ref="liftProgressChart" :graphLabels="getGraphLabels" v-if="!isLoading" :css-classes="cssClasses"
                                     :chart-data="getGraphData" :options="{responsive: true, maintainAspectRatio: false}"></lift-progress-chart>

            </v-card>
        </v-flex>

    </v-layout>
</template>

<script>

    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'
    import LiftProgressChart from '../components/lift-progress-chart.vue'
    import RenderMaxData from '../components/render-max-data.vue'
    import AddMaxLiftTracking from '../components/add-max-lift-tracking.vue'

    export default {
        name: "workout-stats",
        data () {
            return {
                target_muscles: [

                              { text: 'Chest', value: "Chest"},
                              { text: 'Arms', value: "Arms"},
                              { text: 'Legs', value: "Legs"},
                              { text: 'Back', value: "Back"}
                          ],
                chestMax: [],
                selectedMuscle: null,
                dialog: this.$store.state.dialog,
                isLoading: false,
                graphLabels: this.$store.state.muscleHistoryGraphLabels,
                graphData: this.$store.state.muscleHistoryGraphData,
                max_type: '3',
                noResults: false,
                cssClasses: "",
            }
        },
        watch: {

            selectedMuscle: function (queryVal) {
                this.isLoading = true;
                console.log(this.isLoading);
                this.setAndFetchMaxData(queryVal);

            },

            dialog: function () {
              this.dialog = this.$store.state.dialog;
            },

        },
        computed: {
            computeDialog () {

                this.dialog = this.$store.state.dialog;

            },
            getMaxLiftsObjects: function () {

                if (this.$store.state.recentTargetedMuscleExercises) {
                    this.cssClasses = '';
                    this.noResults = false;
                    return this.$store.state.recentTargetedMuscleExercises[0]
                }

                this.cssClasses = 'opacity';
                this.noResults = true;

            },
            getGraphLabels: function () {
                return this.$store.state.muscleHistoryGraphLabels;
            },
            getGraphData: function ()  {
                return this.$store.state.muscleHistoryGraphData
            },
            getLoadingStatus: function () {
                return this.isLoading;
            }
        },
        methods: {
            dialogSet () {
              this.$store.commit('setDialog', !this.dialog);
              this.dialog = this.$store.state.dialog;
            },
            setAndFetchMaxData: function (queryVal) {

                this.selectedMuscle = queryVal;

                this.$store.dispatch('fetchGraphData', queryVal)
                    .then(() => {
                        this.graphLabels = this.$store.state.muscleHistoryGraphLabels;
                        this.graphData = this.$store.state.muscleHistoryGraphData;
                        this.isLoading = false;

                    }).catch((err) => {
                        this.isLoading = false;
                        console.log("Workout-stats.vue setAndFetch: fetchGraphData error:", err);
                    });

            },

        },
        mounted: function () {
            this.isLoading = true;
            this.selectedMuscle = this.target_muscles[0].text;

            this.setAndFetchMaxData(this.target_muscles[0].text);




        },
        components: { LiftProgressChart, RenderMaxData, AddMaxLiftTracking },
    }
</script>

<style  scoped>

    .opacity {
        opacity: 0.4;
    }

</style>