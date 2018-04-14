import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuetify from 'vuetify'
import 'vue-event-calendar/dist/style.css' //^1.1.10, CSS has been extracted as one file, so you can easily update it.
import vueEventCalendar from 'vue-event-calendar'
import Vuex from 'vuex'
import store from './store'



Vue.use(vueEventCalendar, {locale: 'en'});
Vue.use(Vuetify, {
  theme: {
    primary: '#607D8B',
    secondary: '#455A64',
    accent: '#00BCD4',
    success: '#0288D1'
  }
});
Vue.use(Vuex);




new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
});

