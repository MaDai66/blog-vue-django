import { defineStore } from "pinia";
import { ref } from "vue";

export const popStore = defineStore("pop", () => {
  const loginPop = ref(false);
  const registerPop = ref(false);

  // 改变登录弹窗状态
  const changeLoginPop = () => {
    loginPop.value = !loginPop.value;
  };

  // 改变注册弹窗状态
  const changeRegisterPop = () => {
    registerPop.value = !registerPop.value;
  };

  return {
    loginPop,
    registerPop,
    changeLoginPop,
    changeRegisterPop,
  };
});
