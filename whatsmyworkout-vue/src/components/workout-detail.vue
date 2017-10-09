<template>
  <div >
    {{ selectedWorkout }}
      <span ></span>
  </div>
</template>

<script>
export default {
  name: 'workout-detail',
  data () {
    return {
        message: 'adfasdf'
    }
  },
  props: ['selectedWorkout'],
  created: function () {
      this.$bus.$on('selected-workout', function (data) {
          console.log(data)
      })
  }
}
</script>

<style>

</style>