import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/dist/vuetify.min.css'
import Vuetify from 'vuetify'



Vue.use(Vuetify);


new Vue({
  el: '#app',
  router,
  render: h => h(App)
});

