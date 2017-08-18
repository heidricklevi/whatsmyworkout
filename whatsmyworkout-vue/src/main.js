import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/dist/vuetify.min.css'
import Vuetify from 'vuetify'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.css'

Vue.use(Vuetify);


new Vue({
  el: '#app',
  router,
  render: h => h(App)
});

