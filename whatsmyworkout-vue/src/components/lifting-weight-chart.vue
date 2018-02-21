<script>
    import VueCharts from 'vue-chartjs'

    export default {
        extends: VueCharts.Line,
        mixins: [VueCharts.mixins.reactiveProp],
        props: ['chartData', 'options', 'graphLabels', 'repData', 'exerciseData'],
        name: "lifting-weight-chart",

        methods: {

            renderChartWrapper: function () {
                this.renderChart(
                    {
                            labels: this.graphLabels,
                            datasets: [
                                {
                                  label: 'Lifting Weight (lbs.)',
                                  backgroundColor: '#90a4ae',
                                  data: this.data
                                }, {
                                  label: 'Reps',
                                  backgroundColor: '#f87979',
                                  data: this.reps
                                }
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
            reps: function () {
                return this.repData;
            }
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