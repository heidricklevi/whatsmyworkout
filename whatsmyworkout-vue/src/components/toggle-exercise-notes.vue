<template>
    <v-layout justify-end>
          <v-btn @click="opened = true"  small flat class="caption grey--text text--darken-2 mb-0 mt-2 mr-0">
                                               see notes
                                      </v-btn>
                                          <v-card raised v-if="opened" style="position: absolute; width: 300px; margin-top: -160px" class="elevation-5">
                                            <v-btn icon @click="opened = false" right absolute ><v-icon small>close</v-icon></v-btn>
                                              <v-card-title class="mb-0">
                                                  <h4 class="subheading mt-0 mb-0 pb-0 grey--text">Exercise Notes</h4>
                                              </v-card-title>
                                              <v-divider></v-divider>
                                            <v-card-text>
                                                <p class="caption grey--text text--darken-2">{{ exercise.notes }}</p>
                                            </v-card-text>
                                        </v-card>
        </v-layout>
</template>

<script>
    export default {
        name: "toggle-exercise-notes",
        props: ['exercise', 'opened', 'index'],
        data () {
            return {

            }
        },

    }
</script>

<style scoped>

</style>