<template><div>
<v-list-tile-content @click="editExercise()">
                                        <v-layout row style="width: 100%">
                                            <v-flex xs12 md12>
                                        <span style="font-weight: 700;" class="mr-3">{{ index+1 }}.</span>
                                        <span>{{exercise.exercise_name}}</span>
                                        <span style="position: absolute; right: 15%">{{ exercise.sets }}x{{ exercise.reps }}</span>
                                            </v-flex>
                                            <v-flex>
                                                <v-list-tile-sub-title>{{ exercise.notes }}</v-list-tile-sub-title>
                                            </v-flex>
                                        </v-layout>
</v-list-tile-content>
        <v-card raised v-if="updateExercise" style="width: 450px; position: absolute; z-index: 9999; border: 1px solid lightslategray; fill-opacity: 100">
            <v-layout style="width: 100%">
                <v-flex md12 style="display: inline-flex" class="pa-2">
                    <v-text-field v-model="exercise.exercise_name" label="Change Exercise" style="width: 50%"></v-text-field>
                    <v-text-field v-model="exercise.sets" label="sets" style="width: 10%; margin-left: 8px" ></v-text-field>
                    <v-text-field v-model="exercise.reps" label="reps" style="width: 10%; margin-left: 8px" ></v-text-field>
                </v-flex>
            </v-layout>
        <v-layout>
                <v-flex class="pa-2">
                    <v-text-field v-model="exercise.notes" label="Edit Notes"></v-text-field>
                </v-flex>
        </v-layout>
            <v-btn @click.native="editExercise" primary style="width: 20%" >Save</v-btn>
    </v-card>
</div>






</template>



<script>









export default {

    data () {

        return {
            updateExercise: false,
        }
    },
    methods: {
      editExercise: function () {
        this.updateExercise = !this.updateExercise;
      },
    },
    props: ['exercise', 'index']
}




</script>