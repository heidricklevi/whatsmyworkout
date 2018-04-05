'use strict';

var _vue = require('vue');

var _vue2 = _interopRequireDefault(_vue);

var _App = require('./App.vue');

var _App2 = _interopRequireDefault(_App);

var _router = require('./router');

var _router2 = _interopRequireDefault(_router);

var _vuetify = require('vuetify');

var _vuetify2 = _interopRequireDefault(_vuetify);

require('vue-event-calendar/dist/style.css');

var _vueEventCalendar = require('vue-event-calendar');

var _vueEventCalendar2 = _interopRequireDefault(_vueEventCalendar);

var _vuex = require('vuex');

var _vuex2 = _interopRequireDefault(_vuex);

var _store = require('./store');

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_vue2.default.use(_vueEventCalendar2.default, { locale: 'en' }); //^1.1.10, CSS has been extracted as one file, so you can easily update it.

_vue2.default.use(_vuetify2.default, {
  theme: {
    primary: '#607D8B',
    secondary: '#455A64',
    accent: '#00BCD4',
    success: '#0288D1'
  }
});
_vue2.default.use(_vuex2.default);

new _vue2.default({
  el: '#app',
  store: _store2.default,
  router: _router2.default,
  render: function render(h) {
    return h(_App2.default);
  }
});
//# sourceMappingURL=main.js.map