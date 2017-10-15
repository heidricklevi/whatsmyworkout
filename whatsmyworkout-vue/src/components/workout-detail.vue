<template>
    <div>
        <v-layout v-if="selectedWorkout">
            <v-flex md5 offset-md1>
                <v-card>
                    <div>
                        <v-avatar class="ma-3" style="display: inline-flex;">
                            <img :src="userAuth.user.avatar">
                        </v-avatar>
                    </div>
                     <span class="subheading mt-0" style="position: absolute; top: 5px; left: 65px">{{ userAuth.user.username }}</span>
                    <v-menu lazy :close-on-content-click="false"
                            v-model="updateDate"
                            transition="scale-transition"
                            offsetY
                            fullWidth
                            :nudge-right="40"
                            maxWidth="295px"
                            style="top: -25px">
                        <div slot="activator"
                         v-model="tmp.date_for_completion"
                         label="edit date"
                         style="position: absolute; left: 60px; top: 20%;"
                         @click="updateDate = !updateDate">
                        <v-icon class="pr-1">event</v-icon>
                        {{ tmp.date_for_completion }}</div>
                        <v-date-picker v-model="tmp.date_for_completion" no-title  actions>
                            <template scope="{ save, cancel }">
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn primary @click.native="updateDate = !updateDate">Cancel</v-btn>
                                    <v-btn primary @click.native="updateDate = !updateDate">Save</v-btn>
                                </v-card-actions>
                            </template>
                        </v-date-picker>
                    </v-menu>
                    <v-card-title primary-title>
                        <h3 class="headline mb-0" @click="updateTitle = !updateTitle">{{ tmp.title }}</h3>
                    </v-card-title>
                    <v-card raised v-if="updateTitle" style="position:absolute; width: 100%; bottom: -15px">
                         <v-flex xs12>
                            <v-text-field
                                v-model="tmp.title"
                                name="input-1"
                                label="Update Title"
                                id="title"
                            ></v-text-field>
                            <v-btn primary @click="save">save</v-btn>
                        </v-flex>
                    </v-card>

                </v-card>
            </v-flex>
        </v-layout>
        <v-alert v-else="selectedWorkout" error>Could not load the desired workout to edit</v-alert>
    </div>
</template>

<script>

import { userAuth } from '../auth/auth'
import axios from 'axios'
import moment from 'moment'






export default {

    name: 'workout-detail',
  data () {
    return {
        selectedWorkout: this.$store.state.data[0],
        userAuth: userAuth,
        newWorkout: {},
        updateTitle: false,
        tmp: this.$store.state.data[0],
        updateDate: false,

    }
  },

  computed: {

  },

  watch: {
      updateTitle: function () {

      }
  },
  methods: {
      save: function (e) {
        this.updateTitle = false;

      },
  },

  mounted: function () {
      this.tmp.date_for_completion = moment(this.tmp.date_for_completion).format('YYYY-MM-DD');
  }
}
</script>

<style>

</style>