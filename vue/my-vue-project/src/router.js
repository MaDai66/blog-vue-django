import { createRouter, createWebHashHistory } from "vue-router";
import Home from "./pages/home.vue";
import ArticleDetail from "./pages/article-detail.vue";
import Publish from "./pages/article-publish.vue";
import UserProfile from "./pages/user-profile.vue";
import { ElMessage } from "element-plus";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: Home },
  { path: "/detail", component: ArticleDetail },
  { path: "/publish", component: Publish, meta: { isAuth: true } },
  { path: "/profile", component: UserProfile, meta: { isAuth: true } },
  { path: "/user-profile", component: UserProfile },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 路由拦截守卫
router.beforeEach((to, from, next) => {
  //判断是否需要登录权限
  if (to.meta.isAuth) {
    if (localStorage.getItem("token")) {
      next();
    } else {
      ElMessage.error({
        message: "请先登录",
        type: "error",
      });
      router.push("/home");
    }
  } else {
    next();
  }
});

export default router;
