<template>
    <v-layout row wrap v-if="!forbidden">
        <v-flex md4 offset-md1 xs12>
                <v-progress-circular indeterminate :size="40" :width="5" color="purple" v-if="loading"></v-progress-circular>
                <user-profile :user-auth="userProfile"></user-profile>
        </v-flex>



    </v-layout>
    <v-container v-else-if="forbidden">
        <v-layout>
            <v-flex md6 offset md-3 xs12>
                <p class="headline">Access to this profile has not been provided.</p>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import { baseURLLocal} from '../auth/auth-utils'

    import UserProfile from './user-profile.vue'

    export default {
        name: "user-public-profile",
        components: { UserProfile, },
        props: [],
        data () {
            return {

                username: this.$route.params.username,
                loading: false,
                forbidden: false,

            }
        },
        computed: {

            userProfile: function () {
                let profileData = {};
                profileData.user = this.$store.state.data;
                return profileData;
            }

        },
        watch: {

            '$route' (to, from) {
                this.fetchProfileData();
            }

        },
        methods: {

            fetchProfileData () {
                this.loading = true;
                axios.get(baseURLLocal+"v1/users/" + this.username +'/').then(response => {

                    this.$store.commit('setData', response.data);
                    this.loading = false;


                }).catch( err => {

                    let status_FORBIDDEN_403 = 403;

                    this.forbidden = status_FORBIDDEN_403 === err.response.status;

                    this.loading = false;
                    console.log(err.status);
                    console.log(err.response.status);
                    console.log(err)
                })
            }
        },

        created () {
            this.fetchProfileData();
        }
    }
</script>

<style scoped>

</style>