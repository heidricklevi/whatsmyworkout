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

        <tr :active="props.selected" @click="props.selected = !props.selected">
            <td >
            <v-btn icon v-model="props.selected" @click="props.selected = !props.selected" @click.native.stop="editDialog = !editDialog">
                 <v-icon class="blue--text">edit</v-icon>
             </v-btn>

            </td>
            <td class="pt-3">{{ props.item.title }}</td>
            <td class="text-xs-center pt-3"><router-link to="/workout-detail/" >{{ props.item.training_type }}</router-link></td>
            <td class="text-xs-center pt-3">{{ props.item.target_muscle }}</td>
            <td class="text-xs-center pt-3">{{ props.item.date_for_completion }}</td>
        </tr>

          <v-layout>
              <v-dialog v-model="editDialog" persistent width="50%">
                <template v-if="props.selected">
                <v-card v-for="(item, index) in selected" :key="item.id">
                    <v-avatar class="ma-2">
                        <img :src="userAuth.user.avatar">
                    </v-avatar>
                    <v-card-title style="position: absolute; margin-left: 10%">
                        <v-edit-dialog lazy
                        @open="tmp_workout.tmp_title = item.title"
                        @save="item.title = tmp_workout.tmp_title || item.title"
                        >
                            <div class="title ml-2 pt-0">{{ item.title }}</div>
                            <v-text-field
                                    counter
                                    slot="input"
                                    v-model="tmp_workout.tmp_title"
                                    :rules="[max50chars]">
                            </v-text-field>
                        </v-edit-dialog>
                    </v-card-title>
                    <v-layout>
                        <v-flex md4>
                            <v-menu lazy :close-on-content-click="false" v-model="dateMenu" transition="scale-transition"
                                                offset-y full-width :nudge-left="40" max-width="290px">
                                <v-text-field class="ma-2" slot="activator" label="Completion Date" v-model="item.date_for_completion" prepend-icon="event" readonly></v-text-field>
                                <v-date-picker v-model="item.date_for_completion" no-title scrollable actions>
                                   <template scope="{ save, cancel }">
                                         <v-card-actions>
                                              <v-btn flat primary @click.native="cancel()">Cancel</v-btn>
                                              <v-btn flat primary @click.native="save()">Save</v-btn>
                                         </v-card-actions>
                                  </template>
                                </v-date-picker>
                            </v-menu>
                          </v-flex>
                        </v-layout>
                    <v-layout>
                        <v-flex md4>
                            <v-select class="ml-2" title="Target Muscle" id="id_target_muscle" name="target_muscle"
                                              v-model="item.target_muscle" :items="target_muscles" label="Target Muscles"
                                              segmented></v-select>
                        </v-flex>
                    </v-layout>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn class="white--text darken-1" error @click.native="onClose">Close</v-btn>
                        <v-btn class="white--text darken-1" primary @click.native="savedEdit">Save</v-btn>
                    </v-card-actions>
                </v-card>
                </template>
              </v-dialog>
          </v-layout>
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
        selected: function () {
            this.$bus.$emit('selected-workout', this.selected);
        }
  },
  computed: {
    selectedWorkout: function () {
        return this.selected;
    }
  },
  methods: {
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