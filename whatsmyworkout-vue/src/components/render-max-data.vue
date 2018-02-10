<template>
<div>
    <v-layout class="ma-4" v-if="!isLoading && maxLiftsObjects">
        <v-flex md6 xs12 class="pr-2" style="border-right: solid 1px black; text-align: right;">
                                <p class="blue-grey--text text--lighten-2">Exercise</p>
                                <p class="blue-grey--text text--lighten-2">Max Type</p>
                                <p class="blue-grey--text text--lighten-2">Weight</p>
                                <p class="blue-grey--text text--lighten-2">Recorded</p>

        </v-flex>
        <v-flex md6 xs12 class="pl-2" style="text-align: left;" >
                                <p class=" blue-grey--text">{{ maxLiftsObjects.exercise.exercise_name }}</p>
                                <p class=" blue-grey--text">{{ maxLiftsObjects.max_type }}</p>
                                <p class=" blue-grey--text">{{ maxLiftsObjects.weight }} lbs.</p>
                                <p class=" blue-grey--text">{{ maxLiftsObjects.created }}</p>
        </v-flex>

    </v-layout>
    <v-layout class="ma-4" v-if="!maxLiftsObjects && !isLoading">
                        <v-flex xs12>
                            <v-alert color="info" icon="info" value="true">
                                No data could be retrieved.
                            </v-alert>
                        </v-flex>
    </v-layout>


</div>
</template>

<script>
    export default {
        name: "render-max-data",
        props: ['maxLifts', "isLoading"],
        data () {
            return {
                maxLiftsObjects: this.maxLiftsData,

            }
        },
        computed: {
          maxLiftsData: function () {

              return this.maxLifts;
          },
        },
        watch: {

          maxLifts () {
              this.maxLiftsObjects = this.maxLifts;
          },


        },
    }
</script>

<style scoped>

</style>