import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import axios from "@/axios";
import Video from '@/components/VideoPlayer.vue';



Vue.config.productionTip = false
Vue.prototype.$http = axios


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
