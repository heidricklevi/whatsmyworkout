<template>
<div>
    <v-layout class="ma-4" v-if="maxLiftsObjects && !loading">

        <v-flex md6 xs12 class="pr-2" style="border-right: solid 1px #BDBDBD; text-align: right;">
                                <p class="blue-grey--text text--darken-2">Exercise</p>
                                <p class="blue-grey--text text--darken-2">Max Type</p>
                                <p class="blue-grey--text text--darken-2">Weight</p>
                                <p class="blue-grey--text text--darken-2">Recorded</p>

        </v-flex>
        <v-flex md6 xs12 class="pl-2" style="text-align: left;" >
                                <p class=" blue-grey--text ">{{ maxLiftsObjects.exercise.exercise_name }}</p>
                                <p class=" blue-grey--text">{{ maxLiftsObjects.max_type }}</p>
                                <p class=" blue-grey--text">{{ maxLiftsObjects.weight }} lbs.</p>
                                <p class=" blue-grey--text">{{ maxLiftsObjects.created }}</p>
        </v-flex>

    </v-layout>



</div>
</template>

<script>
    export default {
        name: "render-max-data",
        props: ['maxLifts'],
        data () {
            return {

                loading: this.$store.state.loading,
                maxLiftsObjects: this.maxLiftsData,

            }
        },
        computed: {
          maxLiftsData: function () {

              return this.maxLifts
          },
        },
        watch: {

          maxLifts () {
              this.maxLiftsObjects = this.maxLifts;
              this.$store.commit('setLoading', false);
          },


        },
    }
</script>

<style scoped>

</style>