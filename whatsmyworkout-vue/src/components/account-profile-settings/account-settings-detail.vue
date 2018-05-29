<template>
    <v-layout row wrap>
        <v-flex xs12 offset-md1 md10>
            <v-layout>
                    <v-flex md1 text-md-right>
                        <v-avatar size="72"><img :src="userAuth.user.avatar"></v-avatar>
                    </v-flex>
                    <v-flex xs12 md4 class="mt-4 ml-4"  text-xs-center>
                        <h4 class="heading primary--text text--darken-3 text-xs-center">Account Settings</h4>
                        <p class="subheading grey--text text--darken-3 ">Make changes to your account</p>
                    </v-flex>
            </v-layout>
            <v-divider></v-divider>
             <v-snackbar

                      :color="snackAlertColor"
                      :multi-line="'multi-line'"
                      top
                      v-model="snackAlertVal"
                    >
                      {{ snackAlertText }}
                      <v-btn dark flat @click.native="snackAlertVal = false">Close</v-btn>
             </v-snackbar>
            <v-layout row wrap justify-center class="mt-4">
                <v-flex md4 xs11 offset-md1>
                   <v-form v-model="fAndLValid">
                    <v-text-field
                            label="First Name"
                            ref="firstName"
                            return-mask-value
                            hint="Your First Name"
                            :rules="[rules.required, () => firstName.length <= 25 || 'Must be shorter than 25 characters']"
                            v-model="firstName">
                        </v-text-field>


                    <v-text-field
                            label="Last Name"
                            ref="lastName"
                            return-mask-value
                            hint="Your Last Name"
                            :rules="[rules.required, () => lastName.length <= 160 || 'Must be shorter than 160 characters']"
                            v-model="lastName">
                        </v-text-field>

                       </v-form>
                </v-flex>
                <v-flex xs11 md4 offset-md2>
                   <v-form v-model="valid">
                        <v-text-field
                            label="Email"
                            ref="email"
                            return-mask-value
                            hint="Valid email address for notifications, etc. "
                            :rules="[rules.required, rules.email]"
                            v-model="email">
                        </v-text-field>
                        <v-text-field
                            label="Username"
                            ref="username"
                            return-mask-value
                            hint="Alphanumeric, unique and how others see you"
                            :rules="[rules.required, () => username.length >= 8 || 'Must be at least 8 chars.', rules.username]"
                            v-model="username">
                        </v-text-field>

                        <v-text-field
                            label="New Password"
                            type="password"
                            ref="password"
                            hint="Min 8 characters, should contain 1 uppercase, l lowercase, and 1 special character"
                            v-model="newPassword">

                        </v-text-field>

                        <v-text-field
                            label="Confirm Password"
                            ref="password"
                            type="password"
                            v-if="isChangingPassword"
                            hint="Match Your new Password"
                            v-model="confirmNewPassword"
                            :rules="[rules.confirmPassword]"

                        >

                        </v-text-field>

                        <v-btn

                            @click="updateAccount"
                            color="accent"
                            :disabled="updateDisabled">

                            Save changes
                            <v-icon right>check</v-icon>
                        </v-btn>

                    </v-form>
                </v-flex>

            </v-layout>


        </v-flex>
    </v-layout>
</template>

<script>

    import {mask} from 'vue-the-mask'
    import axios from 'axios'
    import { baseURLLocal } from '../../auth/auth-utils'
    import moment from 'moment'

    export default {
        name: "account-settings-detail",
        directives: {mask},
        data () {
            return {
                userAuth: this.$store.state.userAuth,

                fAndLValid: false,
                valid: false,

                rules: {
                    required: (val) => !!val || 'Cannot be blank.',
                    username: (val) => {
                        return !/[^a-zA-Z0-9]/.test(val) || 'Please enter a valid username (alphanumeric, no spaces and case sensitive)';
                    },
                    confirmPassword: (val) => {
                        return this.newPassword === val || 'Passwords Must Match'
                    },

                    email: (value) => {
                        const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                        return pattern.test(value) || 'Invalid e-mail.'
                    },
                },
                isChangingPassword: false,
                isChangingUsername: false,


                newPassword: '',
                confirmNewPassword: '',
                email: this.$store.state.userAuth.user.email,
                username: this.$store.state.userAuth.user.username,
                firstName: this.$store.state.userAuth.user.first_name,
                lastName: this.$store.state.userAuth.user.last_name,

                updateDisabled: false,

                snackAlertVal: false,
                snackAlertColor: '',
                snackAlertText: '',



            }
        },
        watch: {

            fAndLValid() {
                this.updateDisabled = !this.fAndLValid;
            },

            valid () {
              this.updateDisabled = !this.valid;
            },

            newPassword() {
                this.isChangingPassword = !!this.newPassword
            }

        },
        computed: {

        },
        methods: {

            updateAccount() {

                let payload = {
                    first_name: this.firstName,
                    last_name: this.lastName,
                    email: this.email,
                    username: this.username,
                    password: this.newPassword,
                    gender: this.$store.state.userAuth.user.gender,
                    about: this.$store.state.userAuth.user.about,
                };

                if (!payload.password) delete payload.password;
                this.updateDisabled = true;


                this.isChangingUsername = this.$store.state.userAuth.user.username !== this.username;
                console.log(this.isChangingUsername);
                axios.put(baseURLLocal+'v1/users/'+this.$store.state.userAuth.user.username+'/', payload).then(response => {
                    console.log(response);

                    this.snackAlertColor = 'success';
                    this.snackAlertText = 'Successfully updated your account.';
                    this.snackAlertVal = true;


                    this.updateDisabled = false;
                    this.$store.commit('storeUserData', response.data);

                    if (this.isChangingUsername || this.isChangingPassword)
                    {
                        this.$router.push('/login/');
                    }


                }).catch(err => {

                    this.snackAlertColor = 'error';
                    this.snackAlertText = 'There was an error updating your account: '+err.message;
                    this.snackAlertVal = true;

                    this.updateDisabled = false;
                    console.log(err)
                })

            },

        },
        mounted() {
            this.$store.commit('setAccountSettingsDialog', false);
        }
    }
</script>

<style scoped>

</style>