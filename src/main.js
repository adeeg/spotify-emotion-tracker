import Vue from "vue";
import VueRouter from "vue-router";
import BootstrapVue from "bootstrap-vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import App from "./App.vue";
import Login from "./components/Login.vue";
import User from "./components/User.vue";

Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(BootstrapVue);

const routes = [
  { path: "/", component: Login, props: true },
  { path: "/user", component: User }
];

const router = new VueRouter({
  routes
});

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
