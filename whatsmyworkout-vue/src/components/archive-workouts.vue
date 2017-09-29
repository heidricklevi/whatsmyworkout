<template>
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
        
        class="elevation-1"
      >
        <template slot="headers" scope="props">
      <tr :active="props.selected" @click="props.selected = !props.selected">
        <th>
          <v-checkbox
            primary
            hide-details
            @click.native="toggleAll"
            :input-value="props.all"
            :indeterminate="props.indeterminate"
          ></v-checkbox>
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

        <tr :active="props.selected" @click="props.selected = !props.selected">
            <td>
              <v-checkbox
                primary
                hide-details
                :input-value="props.selected"
              ></v-checkbox>
            </td>
            <td>{{ props.item.title }}</td>
            <td class="text-xs-center">{{ props.item.training_type }}</td>
            <td class="text-xs-center">{{ props.item.target_muscle }}</td>
            <td class="text-xs-center">{{ props.item.date_for_completion }}</td>
        </tr>

      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import axios from 'axios'
import {baseURLLocal} from '../auth/auth'


export default {
    name: 'archive-workouts',
  data () {
    return {
      loading: false,
      dataTableItems: [{}],
      alert: false,

      selected: [],
      headers: [
          { text: 'Workout Name',
            align: 'left',
            value: 'title'
          },
          {text: 'Training Type', value: 'Training Type'},
          {text: 'Target Muscle', value: 'Target Muscle'},
          {text: 'Date', value: 'Date'},
      ],
      search: '',
      pagination: {
          sortBy: 'title'
      },
      tmp: '',
    }

  },
  methods: {
    toggleAll () {
        if (this.selected.length) this.selected = [];
        else this.selected = this.items.slice()
      },
      changeSort (column) {
        if (this.pagination.sortBy === column) {
          this.pagination.descending = !this.pagination.descending
        } else {
          this.pagination.sortBy = column;
          this.pagination.descending = false
        }
      },
  },
  mounted: function () {
      var self = this;

      this.loading = true;
      axios.get(baseURLLocal + 'v1/u/workouts/')
           .then(function (response) {

               self.loading = false;
               self.dataTableItems = response.data;
      }).catch(function (err) {
          self.alert = true;
      })
      
  }
}
</script>

<style scoped>

</style>