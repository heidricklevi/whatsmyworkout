

<script>
    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'
    import VueCharts from 'vue-chartjs'


    export default {
        extends: VueCharts.Line,
        mixins: [VueCharts.mixins.reactiveProp],
        props: ['chartData', 'options', 'graphLabels',],
        name: "lift-progress-chart",

        methods: {

            renderChartWrapper: function () {
                this.renderChart(
                    {
                            labels: this.graphLabels,
                            datasets: [
                                {
                                  label: '3 Rep Max (lbs.)',
                                  backgroundColor: '#90a4ae',
                                  data: this.data
                                }, /*{
                                  label: 'Data One',
                                  backgroundColor: '#f87979',
                                  data: [this.getRandomInt(), this.getRandomInt()]
                                }*/
                          ]

                    },
                    this.options
                )
            },
        },
        computed: {
            data: function () {
               return this.chartData;
            },
        },
        watch: {
            chartData: function () {
                this.$data._chart.destroy();
                this.renderChartWrapper();
            },
        },
        mounted() {
            this.renderChartWrapper();
        }
    }
</script>

<style scoped>

</style>