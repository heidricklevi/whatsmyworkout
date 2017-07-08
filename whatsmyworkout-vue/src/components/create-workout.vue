<template>
    <div>
       <div class="row row-margin-top">
           <h3>Create Workouts</h3>
         <div class="row">
             <div class="col-md-4 small-12">
                <form v-on:submit.prevent="onSubmit" id="workoutform" method="post" enctype="multipart/form-data">
                     <div class="form-group row">
                         <div class="col-8">
                             <input v-model="title" id="id-title" type="text" name="title" placeholder="Give this workout a name">
                         </div>
                     </div>
                     <div class="form-group row">
                         <div class="col-8">
                             <date-picker  id="id_date_for_completion" name="date_for_completion" :date="date"></date-picker>
                         </div>
                     </div>
                     <div class="form-group row">
                         <div class="col-8">
                             <select title="Target Muscle" id="id_target_muscle" name="target_muscle" v-model="target_muscle">
                                <option disabled value="">Target Muscle</option>

                                <option v-for="target_muscle in target_muscles" v-bind:value="target_muscle.value">
                                    {{ target_muscle.text }}
                                </option>
                             </select>
                         </div>
                     </div>
                     <div class="form-group row">
                         <div class="col-8">
                             <select title="Training Type" id="id_training_type" name="training_type" v-model="training_type" required="">
                                <option disabled value="">Training Type</option>
                                <option value="Endurance">Endurance</option>
                                <option value="Strength Training">Strength Training</option>
                                <option value="Balance Focused">Balance Focused</option>
                                <option value="Flexibility Focused">Flexibility Focused</option>
                             </select>
                         </div>
                     </div>
                    <div class="form-group row">
                        <div class="col-8">
                            <input id="id_slug" name="slug" :value="slug" hidden>
                        </div>
                    </div>
                    <div class="form-group row">
                        <div class="col-8">
                            <input id="id_user" name="user" value="3">
                        </div>
                    </div>

                    <div class="form-group row">
                        <div class="col-8">
                            <input class="btn btn-primary" type="submit" value="add exercises">
                        </div>
                    </div>

                </form>
                <form v-on:submit.prevent="user" id="loginform" method="post">
                    <input v-model="username" type="text" id="id_username">
                    <input v-model="password" type="password" id="id_password">
                    <input type="submit" class="btn btn-primary" value="Login">
                </form>

         </div>
         </div>
       </div>
    </div>
</template>
<script>
 import myDatepicker from 'vue-datepicker'
 import axios from 'axios'
 import { login } from '../auth/auth'



  export default {
    name: 'create-workout',
    data () {
      return {
      date: {
          time: ''
      },
      username: '',
      password: '',
      title: '',
      target_muscle: '',
      training_type: '',
      target_muscles: [
          { text: 'Traps', value: 'Traps'},
          { text: 'Neck', value: "Neck"},
          { text: 'Chest', value: "Chest"},
          { text: 'Biceps', value: "Biceps"},
          { text: 'Forearm', value: "Forearm"},
          { text: 'Abdominal', value: "Abdominal"},
          { text: 'Quads', value: "Quads"},
          { text: 'Calves', value: "Calves"},
          { text: 'Triceps', value: "Triceps"},
          { text: 'Lats', value: "Lats"},
          { text: 'Middle Back', value: "Middle Back"},
          { text: 'Lower Back', value: "Lower Back"},
          { text: 'Glutes', value: "Glutes"},
          { text: 'Hamstrings', value: "Hamstrings"}

      ],


    }

  },
      computed: {
        slug: function getSlug(e) {
            var date;
            if (!this.date.time){ date = Date.now(); }
            else { date = this.date.time; }
            return this.title + '-' + date + '-' + this.target_muscle;
        }
      },
      methods: {
        user: function () {
          console.log(axios.get('http://127.0.0.1:8000/v1/users/ljheidrick/'))
        },
        userLogin: function () {
          login(this.username, this.password);
        },
        onSubmit: function (event) {

            var form = new FormData($('#workoutform').get(0));
            var baseURL = "http://127.0.0.1:8000/";
            var serverURL = "dev.whatsmyworkout.co/";

            $.ajax({
                type: 'POST',
                url: baseURL + "v1/workouts/",
                xhrFields: { withCredentials: true },
                data: form,
                mimeType: "multipart/form-data",
                cache: false,
                processData: false,
                contentType: false,
                success: function () {
                    $('#workoutform').before('<div class="alert alert-success alert-dismissable fade show"' +
                        ' role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                        '<span aria-hidden="true"></span></button> Successfully created workout </div>');

                    $('.alert').fadeTo(2000, 500).slideUp(500, function () { //auto disappear after 2 seconds
                       $('.alert').slideUp(500);
                    });

                    $('#workout-form').hide();

                }
            });
            return false;

        },
          login: function () {

            var username = $('#id_username').val();
            var password = $('#id_password').val();
            var baseURL = "http://127.0.0.1:8000/";

            let data = {
                username: username,
                password: password
            };

            $.ajax({
                type: 'POST',
                url: baseURL + 'v1/login/',
                contentType: 'application/json; charset=utf-8',
                xhrFields: { withCredentials: true },
                crossDomain: true,
                data: JSON.stringify(data),
                dataType: 'json',
                success: function (data) {
                    console.log("Successful Login");
                    localStorage.setItem('JWT', data.token);
                    $.cookie('token', data.token);
                }

            });

            return false;

        }
      },
      components: {
          'date-picker': myDatepicker
        }
}
</script>

<style>
    @media only screen and (max-width: 768px) {

        div > div.row-margin-top {
            margin: 0;
        }

    }

    input, select {
        display: inline-block;
        padding: 6px;
        line-height: 22px;
        font-size: 16px;
        border: 2px solid rgb(255, 255, 255);
        box-shadow: rgba(0, 0, 0, 0.2) 0px 1px 3px 0px;
        border-radius: 2px;
        color: rgb(95, 95, 95);
    }

    div > div.row-margin-top {
        display: inline-block;
        width: 90%;
    }
    div.row > div.row {
        margin-top: 5%;
    }
    h3 {
        letter-spacing: 5px;
        color: dimgrey;
        border-left: 4px solid #270989;
        padding-left: 4px;
    }
</style>