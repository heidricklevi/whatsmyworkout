<template>
    <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="secondary">

                <v-toolbar-title>Password Reset</v-toolbar-title>
                <v-spacer></v-spacer>

              </v-toolbar>
              <v-card-text>
                  <v-snackbar :color="snackColor" v-model="snackbar" top >{{ snackText }}</v-snackbar>
                <v-form v-model="valid" ref="form">


                          <v-text-field v-model="username" required prepend-icon="person" :rules="[passRules.passRequired]"
                                        name="username" label="Username" type="text"></v-text-field>
                          <v-text-field v-model="token" required label="Token" type="text" :rules="[passRules.passRequired]"
                                        name="token" hint="Please enter the token you received via email"></v-text-field>
                          <v-text-field v-model="password" required :rules="[passRules.passRequired, passRules.passLength]"
                                        prepend-icon="lock" name="password" label="New Password" type="password" hint="Please enter your new password"></v-text-field>
                          <v-text-field v-model="password2" required :rules="[passRules.passRequired, passRules.passLength, passRules.passMustMatchRule]"
                                        label="Confirm Password" name="password2" type="password" hint="Please confirm the new password"></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" type="submit" @click.prevent="submitPassForm" :disabled="submitDisabled">Submit</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
</template>

<script>
    import axios from 'axios'
    import { baseURLLocal } from "../auth/auth-utils";

    export default {
        name: "password-reset-confirm",
        data () {
            return {
                valid: true,
                username: null,
                token: null,
                password: null,
                password2: null,
                passRules: {
                    passRequired: v => !!v || 'This field is required',
                    passLength: v => v.length > 7 || 'Password length must be greater than 7 characters',
                    passMustMatchRule: v => {
                        return this.password === v || 'Passwords Must Match';
                    },

                },

                submitDisabled: false,
                snackbar: false,
                snackText: null,
                snackColor: null,

            }
        },
        watch: {
            valid() {
                this.submitDisabled = !this.valid;
            }
        },
        methods: {

            submitPassForm() {
                let payload = {
                    username: this.username,
                    token: this.token,
                    password: this.password
                };
                delete axios.defaults.headers.common['Authorization'];

                this.submitDisabled = true;
                axios.post(baseURLLocal+ 'v1/reset-password-confirm/', payload).then(response => {
                    this.snackText = 'You have successfully changed your password';
                    this.snackbar = true;
                    this.snackColor = 'success';
                    this.submitDisabled = false;
                    console.log(response)
                }).catch(err => {
                    this.submitDisabled = false;
                    this.snackText = 'There was an error trying to change your password.\n Please double check your inputs.  ';
                    this.snackbar = true;
                    this.snackColor = 'error';
                    console.log(err.response);
                })

            }
        }

    }
</script>

<style scoped>

</style>