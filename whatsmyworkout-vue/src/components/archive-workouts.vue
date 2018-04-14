<template>
<div>
    <v-card>
        <v-alert :type="deleteAlertType" :value="deleteAlertValue">
            {{ deleteAlertText }}
        </v-alert>

        <v-progress-circular style="position: absolute; left: 50%;" v-if="loading" indeterminate v-bind:size="50" class="primary--text"></v-progress-circular>
        <v-alert error v-model="alert">There was a problem loading your workout data</v-alert>
    <v-card-title>
      Workouts
      <v-spacer></v-spacer>
      <v-text-field
        append-icon="search"
        label="Search"
        single-line
        hide-details
        selected-key="id"
        v-model="search"
      ></v-text-field>
    </v-card-title>
    <v-data-table
        v-model="selected"
        v-bind:headers="headers"
        v-bind:items="dataTableItems"
        v-bind:search="search"
        v-bind:pagination.sync="pagination"
        select-all
        :loading="loading"
        class="elevation-1"
      >
        <template slot="headers" slot-scope="props">
      <tr :active="props.selected" @click="props.selected = !props.selected">
        <th>
        </th>
        <th v-for="header in props.headers" :key="header.text"
          :class="['column sortable', pagination.descending ? 'desc' : 'asc', header.value === pagination.sortBy ? 'active' : '']"
          @click="changeSort(header.value)"
        >
          <v-icon>arrow_upward</v-icon>
          {{ header.text }}
        </th>
      </tr>
        </template>
      <template slot="items" slot-scope="props">

        <tr :active="props.selected" @click="props.selected = !props.selected" @click.native.stop="selectedWorkout">
            <td >
            <!--<router-link to="/workout/edit/">-->
                <v-btn icon v-model="props.selected"
                       @click="props.selected = !props.selected"
                       @click.native.stop="selectedWorkout">
                 <v-icon small class="blue--text">edit</v-icon>
            </v-btn>
                <!--</router-link>-->
                <v-btn  icon v-model="props.selected"
                        @click.stop="deleteDialog = true"
                        @click="props.selected = !props.selected" >
                    <v-icon small color="error">delete</v-icon>
                </v-btn>
                <!--<download-excel
                    :data="props.item.exercises"
                    :fields="toExportFieldNames"
                    class="primary btn"
                    name="workout.xls"


                >
                    Download

                </download-excel>-->

                <v-btn

                        flat
                        small
                        @click="onExport(props.item)">
                        Excel
                    <v-icon >file_download</v-icon>
                </v-btn>

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
                        <v-btn flat color="primary" @click.native="deleteDialog = false">Don't Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            </td>

            <td class="text-xs-center pt-3">{{ props.item.title }}</td>
            <td class="text-xs-center pt-3">{{ props.item.training_type }}</td>
            <td class="text-xs-center pt-3">{{ props.item.target_muscle }}</td>
            <td class="text-xs-center pt-3">{{ props.item.date_for_completion }}</td>
        </tr>
     </template>
    </v-data-table>
  </v-card>
    <router-view :selected-workout="selectedWorkout"></router-view>
</div>
</template>

<script>
import axios from 'axios'
import {baseURLLocal} from '../auth/auth-utils'
import moment from 'moment'

import XLSX from 'xlsx'




export default {
    name: 'archive-workouts',
    components: { DownloadExcel, },
  data () {
    return {
      deleteDialog: false,
      target_muscle: '',
      msg: 'dafsfasdfasdfsdaf',
      max50chars: (v) => v.length <= 50 || 'Input too long!',
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
          {text: 'Training Type', value: 'Training Type'},
          {text: 'Target Muscle', value: 'Target Muscle'},
          {text: 'Date', value: 'date'},
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

      propItem: {}


    }

  },
  watch: {

  },
  computed: {

  },
  methods: {

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

        this.deleteDisabled = true;
        axios.delete(baseURLLocal+'v1/u/workouts/', { params: { id: this.selected[0].id} } ).then(response => {
            console.log(response);
            this.deleteDialog = false;
            this.selected = [];
            this.deleteDisabled = false;
            this.deleteAlertValue= true;
            this.deleteAlertText =  'You have successfully deleted workout: '+workoutTitle;
            this.deleteAlertType =  'success';
            this.fetchWorkouts();

        }).catch(err => {
            console.log(err);

        });
        console.log(this.selected);



    },
    selectedWorkout: function () {

        this.$store.commit('setData', this.selected);
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