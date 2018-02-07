

<script>
    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'
    import VueCharts from 'vue-chartjs'


    export default {
        extends: VueCharts.Line,
        mixins: [VueCharts.mixins.reactiveProp],
        props: ['chartData', 'options'],
        name: "lift-progress-chart",
        mounted() {
            this.renderChart(this.chartData, this.options)
        }
    }
</script>

<style scoped>

</style>