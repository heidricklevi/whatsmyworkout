<script>
    import VueCharts from 'vue-chartjs'

    export default {
        extends: VueCharts.Line,
        mixins: [VueCharts.mixins.reactiveProp],
        props: ['chartData', 'graphLabels', 'exerciseName', 'options'],
        name: "max-lift-profile-chart",

         data() {
            return {

            }
        },


        methods: {

            renderChartWrapper: function () {
                this.renderChart(
                    {
                            labels: this.labels,
                            datasets: [
                                {
                                  label: '3 Rep Max (lbs.)',
                                  backgroundColor: '#00BCD4',

                                  data: this.data
                                }, /*{
                                  label: 'Data One',
                                  backgroundColor: '#f87979',
                                  data: [this.getRandomInt(), this.getRandomInt()]
                                }*/
                          ],


                    },
                    this.options
                )
            },
        },
        computed: {
            data: function () {
               return this.chartData;
            },

            labels: function () {
                return this.graphLabels
            }
        },
        watch: {
            chartData: function () {
                this.$data._chart.destroy();
                this.renderChartWrapper();
            },
            'options': function () {
                this.$data._chart.destroy();
                this.renderChartWrapper();
            }
        },
        mounted() {
            this.renderChartWrapper();
        }
    }
</script>

<style scoped>

</style>