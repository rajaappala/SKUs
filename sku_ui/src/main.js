import "@babel/polyfill";
import "mutationobserver-shim";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Axios from 'axios'

Vue.config.productionTip = false;
Vue.prototype.$http = Axios;
const token = localStorage.getItem('access_token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = `Bearer ${token}`
  Vue.prototype.$http.defaults.headers.common['Content-Type'] = "application/json"
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
