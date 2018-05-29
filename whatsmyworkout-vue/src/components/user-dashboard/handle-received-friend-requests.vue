<template>
    <div class="text-xs-center">
        <v-alert
                :color="alertColor"
                :value="alertVal">{{ alertText }}</v-alert>
        <v-progress-circular v-if="loading" indeterminate :size="40" :width="5" color="purple" ></v-progress-circular>
        <div v-if="!loading" class="text-md-left">
            <h5 class="subheading grey--text text--lighten-1 ma-3" v-if="!alertVal && !noResults">Received</h5>
                              <v-chip
                                      v-for="pendingFriend in receivedFriendRequests"
                                      :value="pendingFriend.toggleDisplay"
                                      v-model="pendingFriend.toggleDisplay"
                                      :key="pendingFriend.id"
                                      @input="onRejectRequest(pendingFriend)"
                                      :disabled="disabled"
                                      class="ml-4"
                                      close
                              >

                                  <v-avatar>
                                      <img :src="pendingFriend.from_user.avatar">
                                  </v-avatar>
                                  {{ pendingFriend.from_user.username }}

                                  <div class="chip__close green--text" @click="onAcceptRequest(pendingFriend)"><v-icon >check_circle</v-icon></div>
                              </v-chip>
            </div>
    </div>
</template>
<script>
    import axios from 'axios'
    import { baseURLLocal } from "../../auth/auth-utils";

    export default {
        name: "handle-receive-friend-requests",
        data () {
            return {
                disabled: false,
                receivedFriendRequests: [],
                loading: false,
                noResults: false,

                alertVal: false,
                alertText: '',
                alertColor: 'success',

                accept: false,
            }
        },
        computed: {

        },
        methods: {

            getFriends() {
                this.loading = true;

                axios.get(baseURLLocal +'v1/friends/').then(response => {
                    this.$store.commit('setFriends', response.data.results);
                    this.loading = false;
                }).catch(err => {
                    console.log(err);
                })

            },
            onRejectRequest(pendingFriend) {
                pendingFriend.accept = false;
                this.submitResponse(pendingFriend);
            },

            onAcceptRequest(pendingFriend) {
                pendingFriend.accept = true;
                console.log('accepted', pendingFriend);

                this.submitResponse(pendingFriend)
            },

            submitResponse(pendingFriend) {
                this.loading = true;
                this.disabled = true;
                axios.post(baseURLLocal+ 'v1/friends/', pendingFriend).then(response => {
                    this.loading = false;


                    this.alertVal = true;
                    this.alertText = pendingFriend.accept === false? 'Successfully rejected request': 'Successfully added friend ' +pendingFriend.from_user.username;
                    this.alertColor = 'success';
                    console.log(response);

                    pendingFriend.toggleDisplay = false;

                    if (pendingFriend.accept) { this.getFriends(); }
                }).catch(err => {
                    this.loading = false;
                    console.log(err)
                })
            },

            getReceivedRequests() {

                this.loading = true;
                axios.get(baseURLLocal+ 'v1/friends/?received_requests=true').then(response => {
                    this.receivedFriendRequests = response.data.results;
                    this.$store.commit('setReceivedFriendRequests', this.receivedFriendRequests);

                    this.receivedFriendRequests.map((pr) => {pr.toggleDisplay = true; return pr});

                    this.loading = false;

                    this.noResults = response.data.results.length === 0;

                }).catch(err => {
                    this.loading = false;

                    this.alertVal = true;
                    this.alertText = 'Could not load received requests: '+ err.message;
                    this.alertColor = 'error';
                    console.log(err);
                })


            },
        },
        created() {
            this.getReceivedRequests();
        },
    }
</script>

<style scoped>

</style>