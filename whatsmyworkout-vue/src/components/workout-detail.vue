<template>
    <div>
        <v-layout v-if="selectedWorkout">
            <v-flex md5 offset-md1>
                <v-card>
                    <div>
                        <v-avatar class="ma-3" style="display: inline-flex;">
                            <img :src="userAuth.user.avatar" >
                        </v-avatar>
                        <span class="subheading">{{ userAuth.user.username }}</span>

                    </div>
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




export default {


    name: 'workout-detail',
  data () {
    return {
        selectedWorkout: this.$store.state.data[0],
        userAuth: userAuth,
        newWorkout: {},
        updateTitle: false,
        tmp: this.$store.state.data[0],
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

  }
}
</script>

<style>

</style>