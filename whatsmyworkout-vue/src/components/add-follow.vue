<template>
    <v-list-tile avatar>
                      <v-list-tile-avatar>
                        <img v-bind:src="item.avatar"/>
                      </v-list-tile-avatar>
                      <v-list-tile-content>
                        <v-list-tile-title class="blue-grey--text">{{ item.username }}</v-list-tile-title>
                      </v-list-tile-content>
                      <v-list-tile-action>
                          <v-btn icon flat color="blue lighten-2" :disabled="addFollowBtn" @click.native="addFollow">
                              <v-icon v-if="!addFollowBtnSuccess">add_circle_outline</v-icon>
                              <v-icon v-if="addFollowBtnSuccess" color="success">check</v-icon>
                          </v-btn>
                      </v-list-tile-action>

                    </v-list-tile>
</template>

<script>
    import { baseURLLocal } from '../auth/auth-utils'
    import axios from 'axios'

    export default {
        name: "add-follow",
        data () {
            return {
                addFollowBtn: false,
                addFollowBtnSuccess: false,
            }
        },
        methods: {
          addFollow: function () {
              this.addFollowBtn = true;
              let self = this;

              axios.post(baseURLLocal+'v1/follow/', this.item).then(function (response) {
                  self.addFollowBtnSuccess = true;
                  console.log(response)
              }).catch(function (err) {
                  console.log(err)

              })
          }
        },
        props: ['item', 'index']
    }
</script>

<style scoped>

</style>