<template>
    <v-layout row wrap v-if="!forbidden">
        <v-flex md4 xs12>
            <!--<v-flex md6 xs12>
                <v-card class="mb-2">
                    <router-link to="/user/dashboard/"><v-btn icon class="pa-0 ma-0"><v-icon large>chevron_left</v-icon></v-btn><span class=" text-xs-center">Your Dashboard</span></router-link>
                </v-card>
            </v-flex>-->
            <user-friend-profile :user-auth="userProfileProp" :username="username"></user-friend-profile>
        </v-flex>
        <v-flex md8 xs12>
            <v-flex md10 offset-md1 xs12>
                    <v-card class="blue-grey lighten-5" :class="{'mt-4': $vuetify.breakpoint.smAndDown }">
                          <v-layout row wrap >
                            <v-flex xs5 layout justify-start class="pl-2" align-center>
                                <v-avatar :size="36"><img :src="userProfileProp.user.avatar"></v-avatar>
                                 <span class="subheading grey--text text--darken-4 pl-3">{{ userProfileProp.user.username }}</span>
                            </v-flex>
                            <v-flex  xs6 text-xs-center fill-height>
                                <v-avatar icon class="pr-0 mr-0"><v-icon color="primary">access_time</v-icon></v-avatar>
                                <span class="grey--text text--darken-1">{{ userProfileProp.user.date_joined | moment }}</span>
                            </v-flex>
                            <!--<v-flex md4 xs6 text-xs-center>
                                <v-avatar icon class="pr-0 mr-0">
                                    <v-icon color="primary">event</v-icon>
                                </v-avatar>
                                <span class="grey--text text--darken-1">{{ userProfileProp.user.date_joined | moment }}</span>
                            </v-flex>-->
                          </v-layout>
                        </v-card>
            </v-flex>
            <v-flex md11 offset-md1 xs12 >
                <v-container class="mt-4 ">
                    <v-layout row wrap>

                        <v-flex xs12 md11>
                            <h6 class="title grey--text text--darken-3">Max Lift Progression</h6>
                            <h6 class="subheading grey--text text--darken-1">Core Movements Displayed</h6>
                        </v-flex>
                        <v-flex xs12 md11>
                            <max-lift-profile></max-lift-profile>

                         </v-flex>
                    </v-layout>
                </v-container>
            </v-flex>
            <v-flex md10 offset-md1 class="mt-4">
                <v-tabs icons-and-text centered color="grey lighten-3">
                   <v-tabs-slider color="primary"></v-tabs-slider>
                   <v-tab href="#tab-1">
                        Last 5 Workouts
                    </v-tab>

                   <v-tab-item
                      v-for="i in 1"
                      :key="i"
                      :id="'tab-' + i"
                      >
                      <v-container fluid grid-list-md>
                            <v-data-iterator
                              content-tag="v-layout"
                              row
                              wrap
                              :items="items"
                              :rows-per-page-items="rowsPerPageItems"
                              :pagination.sync="pagination"
                            >
                              <v-flex
                                slot="item"
                                slot-scope="props"
                                md6
                                xs12
                              >
                                <v-card>
                                  <v-card-title class="pt-2 pl-2 pb-0">
                                      <v-layout row wrap>
                                          <v-flex xs2>
                                            <v-avatar  ><img :src="userProfileProp.user.avatar"></v-avatar>
                                          </v-flex>
                                          <v-flex xs6>
                                              <span class=" body grey--text text--darken-2" style="padding-left: 3px">{{ username }}</span>

                                              <p class="caption " style="padding-left: 3px" ><v-icon small color="primary">event </v-icon>
                                              {{ props.item.date_for_completion | moment }}</p>

                                          </v-flex>
                                          <v-flex xs4 text-xs-right class="pt-0">
                                              <span class="d-inline text-xs-right mt-0 pt-0 pr-0 mr-0">
                                                  <v-btn icon class="mt-0 pt-0 pr-0 mr-0" @click="selectedCopy(props.item)">
                                                      <v-icon small>content_copy</v-icon>
                                                  </v-btn>
                                              </span>
                                          </v-flex>



                                      </v-layout>
                                      <v-layout row>
                                          <v-flex text-md-right text-xs-center xs8>
                                              <p class="headline primary--text">{{ props.item.title }}</p>
                                          </v-flex>
                                         <v-flex class="pt-0" xs4 text-xs-right>
                                             <span class="caption grey--text text--darken-1 ">
                                                <img height="16px" width="16px" src="../assets/img/muscle.png">
                                                    {{ props.item.target_muscle }}
                                            </span>
                                         </v-flex>
                                      </v-layout>
                                  </v-card-title>
                                  <v-divider class="mt-0"></v-divider>
                                  <v-list dense>
                                      <template v-for="(exercise, i) in props.item.exercises" v-if="props.item.exercises.length > 0">
                                    <v-list-tile  >

                                      <v-list-tile-content class="grey--text text--darken-4">{{ i+1 }}. {{ exercise.exercise_name }}</v-list-tile-content>
                                      <v-list-tile-content class="align-end grey--text text--darken-1">{{ exercise.sets }} x {{ exercise.reps }}
                                      <v-list-tile-content class="align-end caption grey--text text--lighten-1" v-if="exercise.lifting_weight">
                                          @ {{ exercise.lifting_weight }} lbs.
                                      </v-list-tile-content>
                                      </v-list-tile-content>


                                    </v-list-tile>
                                          <v-divider v-if="i !== props.item.exercises.length -1"></v-divider>
                                          </template>
                                  </v-list>
                                  <v-flex text-xs-center xs12 v-if="props.item.exercises.length <= 0">
                                      <p class="title grey--text text--darken-3">No exercises were created for this workout.</p>
                                  </v-flex>
                                </v-card>
                              </v-flex>
                            </v-data-iterator>

                          </v-container>
                   </v-tab-item>
                </v-tabs>
                <v-dialog
                    v-model="copyDialog"
                    :fullscreen="$vuetify.breakpoint.smAndDown"
                    transition="dialog-bottom-transition"
                    :overlay="false"
                    scrollable
                    max-width="890px"
                  >
                    <v-card tile>
                        <v-snackbar :color="copyAlertColor" v-model="copyAlertVal" top>{{ copyAlertText }}</v-snackbar>
                      <v-toolbar card dark color="primary">
                        <v-btn icon @click.native="closeCopyDialog" :disabled="closeDialogDisabled" dark>
                          <v-icon>close</v-icon>
                        </v-btn>
                        <v-toolbar-title>Copy Workout</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-toolbar-items>
                          <v-btn dark flat @click.native.stop="saveCopy" :disabled="copySaveDisabled">Save</v-btn>
                        </v-toolbar-items>
                      </v-toolbar>

                                <v-card-title>Review & Edit Workout</v-card-title>

                        <v-form ref="copyWorkoutForm">
                              <v-card-text>
                                      <v-layout wrap>
                                          <v-flex xs12 md3 offset-md1 >
                                              <v-text-field
                                                      color="accent"
                                                      label="Workout Title"
                                                      persistent-hint
                                                      hint="What would you like to call this workout?"
                                                      append-icon="edit"
                                                      v-model="title"
                                                      ></v-text-field>
                                          </v-flex>
                                          <v-flex xs12 md3 offset-md1 >
                                               <v-menu
                                                    ref="menu"
                                                    lazy
                                                    :close-on-content-click="false"
                                                    v-model="menu"
                                                    transition="scale-transition"
                                                    offset-y
                                                    full-width
                                                    :nudge-right="40"
                                                    min-width="290px"
                                                    :return-value.sync="date"
                                                  >
                                                    <v-text-field
                                                      slot="activator"
                                                      label="Completion Date"
                                                      v-model="date"
                                                      :value="copiedWorkout.date_for_completion"
                                                      hint="When will you complete this workout?"
                                                      persistent-hint
                                                      prepend-icon="event"
                                                      readonly

                                                    ></v-text-field>
                                                    <v-date-picker v-model="date" no-title scrollable>
                                                      <v-spacer></v-spacer>
                                                      <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                                                      <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                                                    </v-date-picker>
                                                  </v-menu>
                                          </v-flex>
                                          <v-flex xs12 md3 offset-md1 >
                                              <v-select
                                                      v-model="selectedTrainingType"
                                                      label="Training Type"
                                                      :value="copiedWorkout.training_type"
                                                      :items="training_types"
                                                      title="Training Type">

                                              </v-select>
                                          </v-flex>


                                      </v-layout>
                                  <v-divider class="mt-3 mb-3"></v-divider>
                                      <v-layout row wrap fill-height>
                                          <v-layout row class="mt-0">
                                              <v-flex xs5 offset-xs1 class="text-xs-left">
                                                <span class="title grey--text text--darken-3">Exercises</span>
                                              </v-flex>
                                            <v-flex xs5 text-xs-right class="pt-0 mt-0">
                                              <v-btn icon @click="addNewExercise" class="pt-0 mt-0">
                                                  <v-icon v-if="!getAddNewExerciseToggle">add</v-icon>
                                                  <v-icon v-if="getAddNewExerciseToggle" color="error">cancel</v-icon>
                                              </v-btn>
                                            </v-flex>
                                          </v-layout>
                                          <v-flex xs12 class="mt-3">
                                           <!--<v-flex xs12 md1 offset-md1 class="mt-3">

                                           </v-flex>
                                            <v-flex md4 xs12 class="ml-2">
                                                <v-select
                                                    dense
                                                    :disabled="eSearchDisabled"
                                                    :loading="eSelectLoading"
                                                    item-text="exercise_name"
                                                    item-value="exercise_name"
                                                    autocomplete
                                                    :search-input.sync="searchExercises"
                                                    return-object
                                                    :items="target_exercises"
                                                    v-model="selectedExercise"
                                                    label="Exercise"
                                                    >

                                                </v-select>
                                            </v-flex>-->
                                          <v-list dense>
                                              <template v-for="(cExercise, i) in getCopiedExercises">
                                                <div :class="{'mt-4': $vuetify.breakpoint.smAndDown, 'mb-5': $vuetify.breakpoint.smAndDown,}">
                                                    <edit-copied-exercises
                                                        :c-exercise="cExercise"
                                                        :index="i"
                                                        :target-muscle="copiedWorkout.target_muscle"
                                                        :copied-workout="copiedWorkout"
                                                        :edit-exercise="cExercise.editExercise">

                                                    </edit-copied-exercises>
                                                </div>
                                                  <v-flex xs12 md10 offset-md1><v-divider></v-divider></v-flex>
                                              </template>
                                           </v-list>
                                              </v-flex>
                                      </v-layout>
                              </v-card-text>
                        </v-form>
                    </v-card>
                  </v-dialog>
            </v-flex>
        </v-flex>
    </v-layout>
    <v-container v-else-if="forbidden">
        <v-layout>
            <v-flex md6 offset md-3 xs12>
                <p class="headline">You do not have the necessary permissions to view this profile.</p>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import { baseURLLocal} from '../auth/auth-utils'

    import UserFriendProfile from './user-friend-profile.vue'
    import EditCopiedExercises from './edit-copied-exercises.vue'
    import MaxLiftProfile from './max-lift-profile.vue'

    export default {
        name: "user-public-profile",
        components: { UserFriendProfile, EditCopiedExercises, MaxLiftProfile},
        props: [],
        data () {
            return {

                username: this.$route.params.username,
                loading: false,
                forbidden: false,
                userProfileProp: {
                    user: {},
                },
                profile_id: null,
                rowsPerPageItems: [2, 8, 12],
                pagination: {
                    rowsPerPage: 2
                  },

                isOpened: false,
                items: [],
                loadLastFive: false,




                copyDialog: false,
                copiedWorkout: {},
                menu: false,
                date: '',
                training_types: [
                  { text: 'Strength Training', value: 'Strength Training'},
                  { text: 'Flexibility Focused', value: 'Flexibility Focused'},
                  { text: 'Endurance', value: 'Endurance'},
                  { text: 'Balance Focused', value: 'Balance Focused'}
                ],
                selectedTrainingType: '',
                title: '',
                targetMuscle: '',
                copiedWorkoutExercises: [],

                target_exercises: [],
                eSearchDisabled: false,
                eSelectLoading: false,
                selectedExercise: null,
                searchExercises: null,
                exerciseDisabled: false,

                closeDialogDisabled: false,

                copyAlertVal: false,
                copyAlertText: '',
                copyAlertColor: '',
                copySaveDisabled: false,


                newExercise: {},

                userAuth: this.$store.state.userAuth,




            }
        },
        filters: {
            moment(date) {
                return moment(date).format("MMM Do YY");
            }
        },
        computed: {
            getAddNewExerciseToggle (){
                return this.$store.state.friendProfile.addNewExerciseToggle;
            },
            getCopiedWorkout: {
                get: function() {
                    this.copiedWorkout.exercises.map((e) => {e.editExercise = false; return e});
                    return this.copiedWorkout;
                },
                set: function (newExercise) {

                    this.copiedWorkout.exercises.push(newExercise);
                }

            },

            getCopiedExercises: function () {
                return this.copiedWorkout.exercises
            }
        },
        watch: {

            '$route' (to, from) {
                this.fetchProfileData();
            },

            searchExercises(val) {

                val && this.querySelections(val)
            },
            getCopiedExercises(val) {
                console.log('Fired', val);
                this.copiedExerciseEdit(val);
            }


        },
        methods: {
            closeCopyDialog() {
                this.closeDialogDisabled = true;
                this.fetchLastFive();


            },
            addNewExercise() {
                let newExercise = {};
                this.$store.commit('setNewExerciseToggle', !this.$store.state.friendProfile.addNewExerciseToggle);
                //this.addNewExerciseToggle = this.$store.state.friendProfile.addNewExerciseToggle;

                if (!this.getAddNewExerciseToggle) {

                    this.copiedWorkout.exercises.splice(-1, 1); // user cancels addition of new exercise, so we remove last one from list
                    return
                }

                // construct new exercise object with default/stub values

                newExercise.user = this.$store.state.userAuth.user.id;
                newExercise.date_for_completion = '';
                newExercise.lifting_weight = 0;
                newExercise.sets = 0;
                newExercise.reps = 0;
                newExercise.workout_id = null;
                newExercise.editExercise = true;
                newExercise.exercises = [];

                // push onto copied workout exercises property list

                this.getCopiedWorkout = newExercise;


            },
            copiedExerciseEdit(exercise) {

                exercise.editExercise = true;
                console.log('copiedExerciise', exercise)


            },
            selectedCopy (workout){
                this.copyDialog = true;
                workout.isCopiedFromFriend = true;
                this.$store.commit('setToCopyWorkout', workout);
                this.copiedWorkout = this.$store.state.friendProfile.toCopyWorkout;
                this.copiedWorkout.exercises.map((e) => {e.editExercise = false; return e});

                // set fields to original workout values
                this.selectedTrainingType = this.copiedWorkout.training_type;
                this.date = this.copiedWorkout.date_for_completion;
                this.targetMuscle = this.copiedWorkout.target_muscle;
                this.target_exercises = this.getCopiedWorkout.exercises;
                this.title = this.copiedWorkout.title;
            },
            saveCopy () {

                let localCopy = this.copiedWorkout;

                localCopy.user = this.$store.state.userAuth.user.id;
                localCopy.date_for_completion = this.date;
                localCopy.training_type = this.selectedTrainingType;
                localCopy.title = this.title;
                localCopy.workout_image = null;
                localCopy.exercises.map((e) => { e.workout_id = null; delete e.id; e.user = this.userAuth.user.id; delete e.editExercise; e.notes = ''; return e});




                this.copySaveDisabled = true;

                axios.post(baseURLLocal+ 'v1/workouts/', localCopy).then(response => {
                    localCopy.exercises.map((e) => { e.workout_id = response.data.id; e.notes = ''; return e});
                    this.submitExercises(localCopy.exercises);
                    console.log(response)

                }).catch(err => {
                    this.copySaveDisabled = false;
                    this.copyAlertColor = 'error';
                    this.copyAlertVal = true;
                    this.copyAlertText = 'Error copying workout: '+err.message;
                    console.log(err)
                })

            },
            submitExercises(exercises, workout_id) {

                axios.post(baseURLLocal+ 'v1/workout-copy/', exercises).then(response => {
                    this.copyAlertColor = 'success';
                    this.copyAlertVal = true;
                    this.copyAlertText = 'Successfully copied workout!';
                    this.copySaveDisabled = false;
                    this.fetchLastFive();
                    console.log(response)
                }).catch(err => {
                    this.copySaveDisabled = false;
                    this.copyAlertColor = 'error';
                    this.copyAlertVal = true;
                    this.copyAlertText = 'Error copying workout: '+err.message;
                    console.log(err);
                })

            },
            querySelections: _.debounce(function (v) {
                this.eSelectLoading = true;
                //if (!this.target_muscle) { this.errorMessages = "Please choose target muscle before choosing an exercise. "}

                axios.get(baseURLLocal+'v1/exercises/?target_muscle='+this.copiedWorkout.target_muscle).then(response => {

                    this.target_exercises = response.data.results.filter(e => {
                        return (e || '').exercise_name.toLowerCase().indexOf((v || '').toLowerCase()) > -1
                    });

                    this.eSelectLoading = false;
                }).catch(err => {
                    console.log(err);
                    this.eSelectLoading = false;
                })

            },
                500,
            ),
            fetchProfileData () {
                //this.loading = true;
                let accountOwnerURL = `${baseURLLocal}v1/users/${this.username}/`;
                let friendURL = `${baseURLLocal}v1/friend-profile/${this.username}/`;
                let fetchProfileDataURL = this.userAuth.user.username === this.username? accountOwnerURL: friendURL;

                axios.get(fetchProfileDataURL).then(response => {
                    //this.userProfileProp.user.profile_id = response.data.user.profile_id;

                    this.userProfileProp.user = response.data;
                    this.$store.commit('setData', response.data);
                    //this.loading = false;


                }).catch( err => {

                    let status_FORBIDDEN_403 = 403;

                    this.forbidden = status_FORBIDDEN_403 === err.response.status;

                    //this.loading = false;
                    console.log(err.status);
                    console.log(err.response.status);
                    console.log(err)
                })
            },

            fetchLastFive () {
                this.loadLastFive = true;

                axios.get(baseURLLocal+'v1/friend-workouts/?friend='+this.username).then(response => {
                    this.loadLastFive = false;
                    this.items = response.data.results;

                    this.copyDialog = false;
                    this.closeDialogDisabled = false;
                }).catch(err => {
                    this.loadLastFive = false;
                    console.log(err);

                    this.copyDialog = false;
                    this.closeDialogDisabled = false;
                })

            },
        },

        created () {

            axios.all([this.fetchProfileData(), this.fetchLastFive()]).then(axios.spread(function (acct, perms) {
                //this.loading = false;
                console.log(acct, perms);


            }))
        }
    }
</script>

<style scoped>

</style>