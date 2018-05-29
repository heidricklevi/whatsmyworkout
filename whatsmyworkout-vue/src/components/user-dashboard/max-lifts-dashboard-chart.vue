
<script>
     import VueCharts from 'vue-chartjs'

    export default {
        extends: VueCharts.Line,
        mixins: [VueCharts.mixins.reactiveProp],
        props: ['chartData', 'options', 'graphLabels', 'maxType', 'backData', 'legData'],
        name: "max-lifts-dashboard-chart",

        methods: {

            renderChartWrapper: function () {
                this.renderChart(
                    {
                            labels: this.graphLabels,
                            datasets: [
                                {
                                    label: `Bench Press`,
                                    borderColor: '#90a4ae',
                                    pointBackgroundColor: '#90a4ae',
                                    fill: false,
                                    data: this.data,
                                },
                                {
                                    label: 'Deadlifts',
                                    borderColor: '#f87979',
                                    pointBackgroundColor: '#f87979',
                                    fill: false,
                                    data: this.bData
                                },
                                {
                                    label: 'Squats',
                                    borderColor: '#f87922',
                                    pointBackgroundColor: '#f87922',
                                    fill: false,
                                    data: this.lData
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

            bData: function () {
                return this.backData
            },
            lData: function () {
                return this.legData
            }
        },
        watch: {
            chartData: function () {
                this.$data._chart.destroy();
                this.renderChartWrapper();
            },
            backData: function () {
                this.$data._chart.destroy();
                this.renderChartWrapper();
            },
            legData: function () {
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