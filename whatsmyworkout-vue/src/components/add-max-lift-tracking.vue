<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="500px" transition="dialog-bottom-transition" :fullscreen="$vuetify.breakpoint.smAndDown">
      <v-card>
          <v-alert :color="color" icon="check_circle" :value="alertVal">
            {{ alertText }}
        </v-alert>
        <v-card-title>
          <span class="headline">Add Your Max Lift</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
              <v-form ref="form">
                    <v-layout wrap>

                      <v-flex  xs12 sm6 md6 >
                          <v-select
                                  label="Max Type"
                                  hint="Number of reps for the max"
                                  persistent-hint
                                  v-model="max_type"
                                  :items="['1', '3']"
                                  required></v-select>
                      </v-flex>

                      <v-flex  xs12 sm6 md6>
                        <v-text-field v-model="weight" label="Weight" hint="The amount lifted" suffix="lbs." type="number" required></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6>
                        <v-select
                          label="Target Muscle"
                          required
                          v-model="target_muscle"
                          :items="['Arms', 'Chest', 'Back', 'Legs']"
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm6>
                        <v-select
                          label="Exercise"
                          required

                          dense
                          :loading="loading"
                          cache-items
                          autocomplete
                          :search-input.sync="search"
                          v-model="select"
                          :items="items"
                          item-text="exercise_name"
                          return-object
                        ></v-select>
                      </v-flex>
                    </v-layout>
              </v-form>

          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="clearForm()">Close</v-btn>
          <v-btn color="blue darken-1" flat @click.native="submitMax">Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>

    import {baseURLLocal} from '../auth/auth-utils'
    import axios from 'axios'
    import moment from 'moment'

    export default {

        name: "add-max-lift-tracking",
        props: [],
        data () {
            return {

                userAuth: this.$store.state.userAuth,
                weight: '',
                max_type: '',
                target_muscle: '',
                loading: false,
                items: [],
                search: null,
                select: [],
                exercises: [],
                errorMessages: [],
                loadSubmission: false,
                dialog: this.$store.state.dialog,


                alertText: '',
                color: 'success',
                alertVal: false,

            }
        },
        methods: {
            querySelections (v) {
                this.loading = true;
                if (!this.target_muscle) { this.errorMessages = "Please choose target muscle before choosing an exercise. "}

                axios.get(baseURLLocal+'v1/exercises/?target_muscle='+this.target_muscle).then(response => {

                    this.items = response.data.results.filter(e => {
                        return (e || '').exercise_name.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.loading = false;
                }).catch(err => {
                    console.log(err);
                })

            },
            changeDialog() {

                this.dialog = !this.dialog;
                this.$store.commit('setDialog', this.dialog);

            },

            submitMax () {

                let maxObj = {};

                maxObj.target_muscle = this.target_muscle;
                maxObj.max_type = this.max_type;
                maxObj.weight = this.weight;
                maxObj.exercise = this.select;
                maxObj.profile = this.userAuth.user.profile_id;
                this.loadSubmission = true;

                axios.post(baseURLLocal+'v1/max-lifts/', maxObj).then(response => {
                    this.alertVal = true;
                    this.color = 'success';
                    this.alertText = 'Success! The stat was posted';

                    console.log(response);

                }).catch(err => {
                    this.alertVal = true;
                    this.color = 'error';
                    this.alertText = 'There was a problem submitting the request.';


                    console.log(err.status);
                })

            },

            clearForm() {

                this.$refs.form.reset();
                this.changeDialog();


            },
        },
        computed: {



        },
        watch: {
            search (val) {
              val && this.querySelections(val)
            },

        },
        mounted () {

        },
        created () {

        },
    }
</script>

<style scoped>

</style>