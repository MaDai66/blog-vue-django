
import { createApp } from "vue";
import App from "./App.vue";
//路由
import router from "./router.js";
//pinia
import { createPinia } from "pinia";
import ElementPlus from "element-plus";

import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
//配置pinia
const pinia = createPinia();
const app = createApp(App);
// 配置数据持久化
pinia.use(piniaPluginPersistedstate);
// ⾃动引⼊图标
Object.keys(ElementPlusIconsVue).forEach((key) => {
app.component(key, ElementPlusIconsVue[key]);
});
app.use(pinia).use(router).use(ElementPlus).mount("#app");