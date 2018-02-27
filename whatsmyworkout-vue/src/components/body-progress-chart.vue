
<script>
    import VueCharts from 'vue-chartjs'

    export default {
        extends: VueCharts.Line,
        mixins: [VueCharts.mixins.reactiveProp],
        props: ['chartData',  'graphLabels', 'weightData'],
        name: "body-progress-chart",

        data() {
            return {
               options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    tooltips: {
                        mode: 'index',

                    },

               }
            }
        },

        methods: {

            renderChartWrapper: function () {
                this.renderChart(
                    {
                            labels: this.graphLabels,
                            datasets: [
                                {
                                  label: 'Body Fat (%) ',
                                  backgroundColor: '#90a4ae',
                                  data: this.data
                                }, {
                                  label: 'Weight (lbs)',
                                  backgroundColor: '#f87979',
                                  data: this.weight
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

            weight: function () {
                return this.weightData;
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