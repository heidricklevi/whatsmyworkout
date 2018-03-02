<template>
    <div class="text-xs-center">
        <v-alert
                :color="alertColor"
                :value="alertVal">{{ alertText }}</v-alert>
        <v-progress-circular v-if="loading" indeterminate :size="40" :width="5" color="purple" ></v-progress-circular>
        <div v-if="!loading" class="text-md-left">
            <h5 class="subheading grey--text text--lighten-1 ma-3" v-if="!alertVal">Sent</h5>
                              <v-chip
                                      v-for="pendingFriend in sentFriendRequests"
                                      :value="pendingFriend.toggleDisplay"
                                      v-model="pendingFriend.toggleDisplay"
                                      :key="pendingFriend.id"
                                      @input="onCancelRequest(pendingFriend)"
                                      :disabled="disabled"
                                      class="ml-4"
                                      close
                              >
                                  <v-avatar>
                                      <img :src="pendingFriend.to_user.avatar">
                                  </v-avatar>
                                  {{ pendingFriend.to_user.username }}
                              </v-chip>
            </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import { baseURLLocal } from "../auth/auth-utils";

    export default {
        name: "handle-friend-requests",
        props: [],
        data () {
            return {
                disabled: false,
                sentFriendRequests: [],
                loading: false,

                alertVal: false,
                alertText: '',
                alertColor: 'success',



            }

        },
        methods: {
            getPendingRequests() {

                this.loading = true;
                axios.get(baseURLLocal+ 'v1/friends/?sent_requests=true').then(response => {
                    this.sentFriendRequests = response.data.results;
                    this.$store.commit('setSentFriendRequests', this.sentFriendRequests);

                    this.sentFriendRequests.map((pr) => {pr.toggleDisplay = true; return pr});

                    this.loading = false;

                }).catch(err => {
                    this.loading = false;

                    this.alertVal = true;
                    this.alertText = 'Could not load sent requests: '+ err.message;
                    this.alertColor = 'error';
                    console.log(err);
                })


            },

            onCancelRequest(pendingFriend) {

                this.disabled = true;

                axios.delete(baseURLLocal+ 'v1/friends/'+pendingFriend.id+'/', { params: { id: pendingFriend.id }}).then(response => {

                    console.log('removed', pendingFriend);
                    pendingFriend.toggleDisplay = false;
                    this.getPendingRequests();


                }).catch(err => {

                    console.log(err)

                });


            },
        },
        computed: {

            requestData: function () {
                return this.sentFriendRequests;
            }

        },

        watch: {

        },

        created() {
            this.getPendingRequests();
        }

    }
</script>

<style scoped>

</style>