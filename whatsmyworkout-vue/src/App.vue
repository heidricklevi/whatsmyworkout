<template>
<div class="row row-margin-top">
    <div class="col-md-4 col-sm-10 col-xs-12">
                        <div class="card text-center">
                            <h4 class="card-header">Next Workout</h4>
                            <div class="card-block">
                                <div class="text-center">
                                    <div>
                                        <p class="card-text display-inline workout-text">3 March 2017</p>
                                    <br/><p class="card-text float-left clear">Type: <span>Strength Training</span></p>
                                    </div>
                                    <div class="clear image">
                                        <p class="img-overlay">Target muscles: <span>Triceps</span></p>
                                        <img src="../src/assets/img/250px-Triceps_brachii.png">
                                    </div>
                                </div>
                            </div>
                               <div>
                                   <table class="table">
                                        <thead>
                                             <tr>
                                                 <th>#</th>
                                                 <th>Exercise</th>
                                                 <th>Sets</th>
                                                 <th>Reps</th>
                                             </tr>
                                        </thead>
                                       <tbody>
                                            <tr>
                                                <th scope="row">1</th>
                                                <td>Straight Arm pull downs</td>
                                                <td>4</td>
                                                <td>12</td>
                                            </tr>
                                            <tr>
                                                <th scope="row">2</th>
                                                <td>Hammer Curls</td>
                                                <td>4</td>
                                                <td>12</td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td>Overhead Extensions</td>
                                                <td>4</td>
                                                <td>12</td>
                                            </tr>
                                            <tr>
                                                <th scope="row">4</th>
                                                <td>Overhead press</td>
                                                <td>4</td>
                                                <td>12</td>
                                            </tr>
                                       </tbody>
                                   </table>
                               </div>

                        </div>
                    </div>
</div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

