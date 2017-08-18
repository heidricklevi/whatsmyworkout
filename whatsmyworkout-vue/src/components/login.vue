<template>
    <div>
        <v-layout class="ma-5" row>
            <v-flex xs12 sm12 md4 class="margin">
                    <v-card >
                        <v-card-text>
                            <v-container fluid>
                                <v-layout row wrap>
                                    <v-flex xs12 md12>
                                        <v-subheader display-4>Login below to access your Dashboard</v-subheader>
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
                                            <v-text-field v-model="password" label="password"
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
    import { login } from '../auth/auth'



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
                login(this.username, this.password);
            }
        },
    }

</script>

<style>
    #hero {
        display: none;
    }
    .margin {
        margin: 5% 0 0 35%;
    }

@media only screen and (max-width: 768px) {

      .margin {
          margin: 15% 0 0 0 ;
      }

    }
</style>