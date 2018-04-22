<template>

    <v-layout justify-center>
        <v-flex xs12 md9>
    <v-card>
        <v-alert :type="deleteAlertType" :value="deleteAlertValue">
            {{ deleteAlertText }}
        </v-alert>

        <v-progress-circular style="position: absolute; left: 50%;" v-if="loading" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
        <v-alert error v-model="alert">There was a problem loading your workout data</v-alert>
    <v-card-text>
        <v-layout row wrap>
            <v-flex xs12>
                <h5 class="headline grey--text text--darken-3 ml-3">Workouts</h5>
            </v-flex>
            <v-flex text-xs-right offset-md6 md5 xs8 offset-xs2>
                   <v-text-field
                    append-icon="search"
                    label="Search Workouts"
                    hide-details
                    single-line
                    selected-key="id"
                    v-model="search"
                  ></v-text-field>
            </v-flex>
            <v-flex xs12 md4 text-xs-left offset-md1>
                <span class="caption">Bulk Actions: <span v-if="selected.length > 1"><v-btn @click="bulkDelete"  flat small class="mx-0" color="warning">Delete Workouts</v-btn></span></span>
            </v-flex>
        </v-layout>
    </v-card-text>
    <v-data-table
        v-model="selected"
        v-bind:headers="headers"
        v-bind:items="dataTableItems"
        v-bind:search="search"
        v-bind:pagination.sync="pagination"
        :loading="loading"
        select-all

        
      >
        <!--<template slot="headers" slot-scope="props">
      <tr :active="props.selected" @click="props.selected = !props.selected">
        <th v-for="header in props.headers" :key="header.text"
          :class="['column sortable', pagination.descending ? 'desc' : 'asc', header.value === pagination.sortBy ? 'active' : '']"
          @click="changeSort(header.value)"
        >
          <v-icon>arrow_upward</v-icon>
          {{ header.text }}
        </th>
      </tr>
        </template>-->
      <template slot="items" slot-scope="props">

        <!--<tr :active="props.selected" @click="props.selected = !props.selected" @click.native.stop="selectedWorkout">-->
            <td>
                <v-checkbox
                    primary
                    hide-details
                    v-model="props.selected"
                ></v-checkbox>
            </td>
            <td class=" pt-3">{{ props.item.title }}</td>
            <td class="text-xs-center pt-3">{{ props.item.training_type }}</td>
            <td class="text-xs-center pt-3">{{ props.item.target_muscle }}</td>
            <td class="text-xs-center pt-3">{{ props.item.date_for_completion }}</td>
            <td class="justify-center layout px-0">
                <v-menu bottom>
                    <v-btn
                            slot="activator"
                            icon>
                        <v-icon color="accent">more_vert</v-icon>
                    </v-btn>
                        <v-list dense>
                            <v-list-tile
                                    @click="selectedWorkout(props.item)">
                                <v-list-tile-content>
                                <v-list-tile-title>
                                   <span class="caption grey--text text--darken-3">Edit</span>
                                    </v-list-tile-title>
                                    </v-list-tile-content>
                                <v-list-tile-action>
                                    <v-icon small class="blue--text">edit</v-icon>
                                </v-list-tile-action>
                                </v-list-tile>
                            <v-divider class="pa-0 ma-0"></v-divider>
                                <v-list-tile @click="initiateRemove(props.item)">
                                    <v-list-tile-content>
                                    <v-list-tile-title>
                                        <span class="caption grey--text text--darken-3">Remove</span>
                                     </v-list-tile-title>
                                        </v-list-tile-content>
                                    <v-list-tile-action>
                                          <v-icon small class="error--text text--lighten-5">delete</v-icon>
                                    </v-list-tile-action>
                                </v-list-tile>
                            <v-divider class="pa-0 ma-0"></v-divider>
                                <v-list-tile @click="onExport(props.item)">
                                    <v-list-tile-content>
                                    <v-list-tile-title>
                                        <span class="caption grey--text text--darken-3">Export xlsx</span>

                                    </v-list-tile-title>
                                        </v-list-tile-content>
                                    <v-list-tile-action>
                                        <v-icon small color="secondary">file_download</v-icon>
                                    </v-list-tile-action>
                                    </v-list-tile>
                            </v-list>
                    </v-menu>
            </td>

        <!--</tr>-->
     </template>
    </v-data-table>
  </v-card>
    <router-view :selected-workout="selectedWorkout"></router-view>

    <v-dialog
                v-model="deleteDialog"
                transition="dialog-bottom-transition"
                :overlay="false"
                max-width="290"
                >
                <v-card>
                    <v-card-title class="title">Do you want to delete this workout?</v-card-title>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn flat :disabled="deleteDisabled" color="warning" @click.native="deleteWorkout">Delete</v-btn>
                        <v-btn flat color="primary" @click.native="cancelRemove">Don't Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-dialog
                    transition="dialog-bottom-transition"
                    :overlay="false"
                    max-width="500"
                    v-model="bulkDeleteDialog">
                <v-card>
                    <v-card-title>
                        <h6 class="grey--text text--darken-2 title">Bulk Delete Workouts</h6>
                    </v-card-title>
                    <v-card-text>
                        <span class="body grey--text text--darken-3">Are you sure you want to delete the selected workouts?</span>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn :disabled="bulkDisabled" color="warning" @click="bulkDeleteConfirm">Delete</v-btn>
                        <v-btn color="primary" @click="cancelRemove">Cancel</v-btn>
                    </v-card-actions>
                </v-card>


            </v-dialog>
            </v-flex>
        </v-layout>
</template>

<script>
import axios from 'axios'
import {baseURLLocal} from '../auth/auth-utils'
import moment from 'moment'

import XLSX from 'xlsx'




export default {
    name: 'archive-workouts',
  data () {
    return {
      deleteDialog: false,
      target_muscle: '',
      dateMenu: false,
      userAuth: this.$store.state.userAuth,
      editDialog: false,
      loading: false,
      dataTableItems: [{}],
      alert: false,
      selected: [],
      deleteDisabled: false,
      showToolTip: false,
      headers: [
          { text: 'Workout Name',
            align: 'left',
            value: 'title'
          },
          {text: 'Training Type', value: 'training_type'},
          {text: 'Target Muscle', value: 'target_muscle'},
          {text: 'Date', value: 'date_for_completion'},
          {text: 'Actions', value: 'title', sortable: false},
      ],
      search: '',
      pagination: {
          sortBy: ''
      },
      tmp_workout: {
          tmp_title: '',
          tmp_date_for_completion: '',
      },
      target_muscles: [
          { text: 'Traps', value: 'Traps'},
          { text: 'Neck', value: "Neck"},
          { text: 'Chest', value: "Chest"},
          { text: 'Biceps', value: "Biceps"},
          { text: 'Forearm', value: "Forearm"},
          { text: 'Abdominal', value: "Abdominal"},
          { text: 'Quads', value: "Quads"},
          { text: 'Calves', value: "Calves"},
          { text: 'Triceps', value: "Triceps"},
          { text: 'Lats', value: "Lats"},
          { text: 'Middle Back', value: "Middle Back"},
          { text: 'Lower Back', value: "Lower Back"},
          { text: 'Glutes', value: "Glutes"},
          { text: 'Hamstrings', value: "Hamstrings"}

      ],


      deleteAlertValue: false,
      deleteAlertText: '',
      deleteAlertType: 'success',


      toExportFieldNames: {
                'Workout Name': 'title',
                'Target Muscle': 'target_muscle',
                'Training Type': 'training_type',
                'Exercise': 'exercise_name',
                'Sets': 'sets',
                'Reps': 'reps',
                'Set Weight': 'lifting_weight',
                'Notes': 'notes'
      },

      propItem: {},

        bulkDeletePromises: [],
        bulkDeleteDialog: false,
        bulkDisabled: false,


    }

  },
  watch: {

  },
  computed: {

  },
  methods: {
        bulkDeleteConfirm() {
            this.bulkDisabled = true;
            axios.all(this.bulkDeletePromises).then(w => {
                this.bulkDisabled = false;
                this.bulkDeleteDialog = false;
                this.deleteAlertValue = true;
                this.deleteAlertText = 'Successfully Removed';
                this.deleteAlertType = 'success';
                this.fetchWorkouts();
            }).catch(err => {
                this.bulkDisabled = false;
                this.bulkDeleteDialog = false;
                this.deleteAlertValue = true;
                this.deleteAlertText = 'There was a problem removing: '+err.msg;
                this.deleteAlertType = 'error';
                console.log(err)
            })
        },
    bulkDelete() {
        this.selected.forEach(w => {
            this.bulkDeletePromises.push(axios.delete(baseURLLocal+'v1/u/workouts/', { params: { id: w.id}}))
        });

        this.bulkDeleteDialog = true;
    },

    cancelRemove() {
      this.selected = [];
      this.deleteDialog = false;
      this.bulkDeleteDialog = false;
    },
    initiateRemove(item){
      this.selected.push(item);
      this.deleteDialog = true;
    },

    onExport(workout) {

       let ColInfo = [
        {wch:40},
        {wch:20},
        {wch:20},
        {wch:20}
    ];

        let newWorkout = this.prepareForExport(workout);
        let wb = XLSX.utils.book_new({cellStyles: true});
        let ws = XLSX.utils.json_to_sheet([newWorkout]);
        let filename = newWorkout.title+ '_'+newWorkout.date_for_completion.replace(/\//g, '')+'.xlsx';

        XLSX.utils.sheet_add_json(ws, newWorkout.exercises, {skipHeader: false, origin: -1});
        ws["!cols"] = ColInfo;
        XLSX.utils.book_append_sheet(wb, ws, "People");
        XLSX.writeFile(wb, filename);


    },
    prepareForExport (workout) {
          let formattedWorkoutObj = {};
          formattedWorkoutObj.exercises = [{}];
          let prop;

          for (prop in workout) {
              console.log(prop);
              if (prop !== 'user' && prop !== 'id' && prop !== 'slug' && prop !== 'workout_image' && prop !== 'exercises') {
                    formattedWorkoutObj[prop] = workout[prop];
              }
          }

          for (let i = 0; i < workout.exercises.length; i++) {
              console.log(i);

              for (prop in workout.exercises[i]) {
                  console.log(prop);
                  if (prop !== 'user' && prop !== 'id' && prop !== 'created' && prop !== 'exercises' && prop !== 'target_muscle') {
                     formattedWorkoutObj.exercises[i][prop] = workout.exercises[i][prop];
                 }
              }
          }
        console.log("formattedWorkoutObj", formattedWorkoutObj);
        return formattedWorkoutObj;
    },
    fetchWorkouts: function () {
          let self = this;
          this.loading = true;
          axios.get(baseURLLocal + 'v1/u/workouts/')
               .then(function (response) {

                   self.loading = false;
                   self.dataTableItems = response.data;
                   for (var i = 0; i < self.dataTableItems.length; i++){
                       self.dataTableItems[i].date_for_completion = moment(self.dataTableItems[i].date_for_completion).format('MM/DD/YYYY');

                   }
          }).catch(function (err) {
              self.alert = true;
              self.loading = "error";
          })

    },
    deleteWorkout: function () {

        let workoutTitle = this.selected[0].title;
        let indexToRemove = this.dataTableItems.indexOf(this.selected[0]);

        this.deleteDisabled = true;
        axios.delete(baseURLLocal+'v1/u/workouts/', { params: { id: this.selected[0].id} } ).then(response => {
            console.log(response);
            this.deleteDialog = false;
            this.selected = [];
            this.deleteDisabled = false;
            this.deleteAlertValue= true;
            this.deleteAlertText =  'You have successfully deleted workout: '+workoutTitle;
            this.deleteAlertType =  'success';

            this.dataTableItems.splice(indexToRemove, 1);

        }).catch(err => {
            console.log(err);

        });



    },
    selectedWorkout: function (item) {
        this.selected.push(item);
        this.$store.commit('setData', [item]);
        this.$router.push('/workout/edit');
    },
    toggleAll () {
        if (this.selected.length) this.selected = [];
        else this.selected = this.items.slice()
      },
    changeSort (column) {

        console.log(column);
        console.log(this.pagination)
        if (this.pagination.sortBy === column) {
          this.pagination.descending = !this.pagination.descending
        } else {
          this.pagination.sortBy = column;
          this.pagination.descending = false
        }
      },
      saveEdit: function () {
          return
      },
      onClose: function () {
        this.editDialog = false;
        this.selected = [];
      }
  },
  mounted: function () {
      this.fetchWorkouts();
  }
}
</script>

<style scoped>

</style>