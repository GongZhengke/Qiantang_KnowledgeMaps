import { createApp } from 'vue'
import ArcoVue from '@arco-design/web-vue'
import ViewUIPlus from 'view-ui-plus'
import App from './App.vue'
import router from './router'
import '@arco-design/web-vue/dist/arco.css'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import axios from './axios'
const app = createApp(App)
app.use(router).use(ArcoVue).use(ViewUIPlus).mount('#app')
app.config.globalProperties.$axios=axios