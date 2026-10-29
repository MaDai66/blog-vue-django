import { defineStore } from "pinia";
import { ref } from "vue";

export const userStore = defineStore(
  "user",
  () => {
    // 账号名
    const username = ref("");

    // 用户ID
    const userId = ref("");

    // 是否登录
    const isLogin = ref(false);

    // 登录
    const getLoginInfo = (id) => {
      isLogin.value = true;
      if (id) {
        userId.value = id;
      }
    };

    const changeUsername = (u) => {
      username.value = u;
    };

    const changeUserId = (id) => {
      userId.value = id;
    };

    // 退出登录
    const logout = () => {
      isLogin.value = false;
      username.value = "";
      userId.value = "";
      localStorage.removeItem("token");
    };

    return { username, userId, isLogin, changeUsername, changeUserId, getLoginInfo, logout };
  },
  {
    persist: true, //Store中数据持久化生效
  }
);
