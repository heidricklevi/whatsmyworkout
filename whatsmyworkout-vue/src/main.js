import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuetify from 'vuetify'
import 'vue-event-calendar/dist/style.css' //^1.1.10, CSS has been extracted as one file, so you can easily update it.
import vueEventCalendar from 'vue-event-calendar'


Vue.use(vueEventCalendar, {locale: 'en'});
Vue.use(Vuetify);

Object.defineProperty(Vue.prototype, '$bus', {
    get() {
        return this.$root.bus;
    }
});

var bus = new Vue({});

new Vue({
  el: '#app',
  data: {
      bus:bus
  },
  router,
  render: h => h(App)
});

