<template>
<div>
    <v-card>
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
        <template slot="headers" scope="props">
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
      <template slot="items" scope="props">

        <tr :active="props.selected" @click="props.selected = !props.selected" @click.native.stop="selectedWorkout">
            <td >
            <router-link to="/workout-detail/" ><v-btn icon v-model="props.selected" @click="props.selected = !props.selected" @click.native.stop="selectedWorkout">
                 <v-icon class="blue--text">edit</v-icon>
            </v-btn></router-link>

            </td>
            <td class="pt-3">{{ props.item.title }}</td>
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
import {baseURLLocal, userAuth} from '../auth/auth'
import moment from 'moment'



export default {
    name: 'archive-workouts',
  data () {
    return {
      target_muscle: '',
      msg: 'dafsfasdfasdfsdaf',
      max50chars: (v) => v.length <= 50 || 'Input too long!',
      dateMenu: false,
      userAuth: userAuth,
      editDialog: false,
      loading: false,
      dataTableItems: [{}],
      alert: false,
      selected: [],
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
    }

  },
  watch: {

  },
  computed: {

  },
  methods: {

    selectedWorkout: function () {

          this.$store.commit('setData', this.selected);
          console.log("commited selected workout to store")
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
      var self = this;

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
      
  }
}
</script>

<style scoped>

</style>