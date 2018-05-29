<template>
    <v-layout row wrap v-if="isMaxData">
        <v-flex xs12 offset-md1>
            <v-card  raised tile>
                <v-card-title>
                    <h6 class="subheading widget-title">Max Lift</h6>
                </v-card-title>



                <max-lifts-dashboard-widget-chart class="pa-4" :chart-data="getGraphData" :back-data="bData" :leg-data="lData" :graph-labels="getGraphLabels" :options="chartOptions"></max-lifts-dashboard-widget-chart>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import axios from 'axios'
    import { baseURLLocal } from "../../auth/auth-utils";
    import MaxLiftsDashboardWidgetChart from './max-lifts-dashboard-chart.vue'
    import moment from 'moment'

    export default {
        name: "max-lifts-dashboard-widget",
        components: {MaxLiftsDashboardWidgetChart, },
        data () {
            return {

                isMaxData: false,

                loading: false,
                labels: [],
                chartData: [],
                chartOptions: {

                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {

                    },
                    title: {
                        text: '3 Rep Max (all time)',
                        display: true,
                        fontSize: 24,
                        fontStyle: 'normal',
                        fontColor: '#424242',
                    },
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {
                                unit: 'month',
                                displayFormats: {
                                    quarter: 'MMM YYYY'
                                }
                            },
                            gridLines: {
                                display: false
                            }
                        }],
                        yAxes: [{
                            gridLines: {
                                display: false
                            }
                        }]
                    },

                },
                bData: [],
                lData: [],
            }
        },
        computed: {
            getGraphData: {
                get() {
                    return this.chartData
                },

                set(val) {
                   this.chartData = val;
                }


            },

            getGraphLabels: {
                get() {
                    return this.labels
                },
                set(val) {
                    this.labels = val;
                }
            },
        },
        methods: {
            fetchMaxBenchPress () {
                return axios.get(baseURLLocal+ 'v1/max-lifts/?exercise_name='+'Bench Press'+
                    '&max_type=3&max=max')
            },
            fetchMaxSquat () {
                return axios.get(baseURLLocal+ 'v1/max-lifts/?exercise_name='+'Squats'+
                    '&max_type=3&max=max')
            },
            fetchMaxDeadlift () {
                return axios.get(baseURLLocal+ 'v1/max-lifts/?exercise_name='+'Deadlifts'+
                    '&max_type=3&max=max')
            },

            async fetchAll () {

                const [chest, legs, back] = await axios.all([this.fetchMaxBenchPress(), this.fetchMaxSquat(), this.fetchMaxDeadlift()]);
                console.log('chest', chest);

                let cWeight = chest.data.results.length > 0? chest.data.results[0].weight: null;
                let cLegs = legs.data.results.length > 0? legs.data.results[0].weight: null;
                let cBack = back.data.results.length > 0? back.data.results[0].weight: null;

                let cDate = chest.data.results.length > 0? moment(chest.data.results[0].created).format("MM/DD/YYYY"): null;
                let lDate = legs.data.results.length > 0? moment(legs.data.results[0].created).format("MM/DD/YYYY"): null;
                let bDate = back.data.results.length > 0? moment(back.data.results[0].created).format("MM/DD/YYYY"): null;



                this.isMaxData = cWeight || cLegs || cBack;

                if (cDate) this.labels.push(cDate);
                if (lDate) this.labels.push(lDate);
                if (bDate) this.labels.push(bDate);

                let obChest = {
                    x: cDate,
                    y: cWeight
                };
                let obBack = {
                    x: bDate,
                    y: cBack
                };

                let obLegs = {
                    x: lDate,
                    y: cLegs
                };

                this.chartData.push(obChest);
                this.bData.push(obBack);
                this.lData.push(obLegs);
                /*this.chartData.push(cWeight);
                this.lData.push(cLegs);
                this.bData.push(cBack);*/

            },
        },
        mounted () {
            this.fetchAll();
        }

    }
</script>

<style scoped>

</style>