<template>
    <div>
        <v-layout class="ma-5" row wrap justify-center>
            <v-flex xs12 sm12 md4 class="margin">
                    <v-card >
                        <v-card-text>
                            <v-container fluid>
                                <v-layout row wrap>
                                    <v-flex xs12 md12>
                                        <v-subheader display-4>Provide Your Credentials to continue</v-subheader>
                                    </v-flex>
                                </v-layout>
                                <form v-on:submit.prevent="userLogin" method="post">
                                    <v-layout row>
                                        <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="username"
                                                          label="username"
                                                          prepend-icon="account_circle"
                                            ></v-text-field>
                                        </v-flex>
                                    </v-layout>
                                      <v-layout row>
                                        <v-flex xs12 sm12 md8>
                                            <v-text-field v-model="password" label="password" type="password"
                                                            prepend-icon="visibility_off"></v-text-field>
                                        </v-flex>
                                    </v-layout>
                                    <v-layout row>
                                        <v-flex xs12 md8>
                                            <input class="btn primary" type="submit" value="Login">
                                        </v-flex>
                                    </v-layout>
                                </form>
                            </v-container>
                        </v-card-text>
                    </v-card>
            </v-flex>
        </v-layout>

    </div>
</template>

<script>
    import { login } from '../auth/auth-utils'
    import { baseURLLocal } from "../auth/auth-utils";
    import axios from 'axios'

    export default {

        name: 'login',
        data () {
            return {
                username: '',
                password: '',

            }
        },
        methods: {
            userLogin: function () {
                let credentials = {username: this.username, password: this.password};
                axios.post(baseURLLocal+'v1/login/', credentials
                        ).then(response => {
                            let JWT = response.data.token;
                            localStorage.setItem("JWT", JWT);
                            this.$store.commit('setUserAuth', response.data.user);
                            this.$router.push('/user/dashboard')
                        }).catch(err => {
                            console.log(err);

                        })
            }
        },
    }

</script>

<style>

</style>