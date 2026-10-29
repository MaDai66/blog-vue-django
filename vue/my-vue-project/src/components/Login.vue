<script setup>
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { getLogin } from "../api/user";
import { ref } from "vue";

const pop = popStore();
const user = userStore();
// 账号
const formData = ref({
  username: "",
  password: "",
});

// 从token中解析用户信息
const parseToken = (token) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('解析token失败:', error);
    return null;
  }
};

// 登录按钮
const submitForm = async () => {
  try {
    console.log('开始登录', formData.value);
    const res = await getLogin(formData.value);

    if (res) {
      // JWT登录成功后返回的是 {"access": "...", "refresh": "..."}
      const token = res.access || res.token || res;
      let userId = res.user_id || res.id;
      
      // 从token中解析user_id（JWT默认使用user_id作为claim）
      if (!userId && token) {
        const tokenData = parseToken(token);
        if (tokenData && tokenData.user_id) {
          userId = tokenData.user_id;
        }
      }
      
      localStorage.setItem("token", "Bearer " + token);
      user.getLoginInfo(userId);
      user.changeUsername(formData.value.username);
      pop.changeLoginPop();
    }
  } catch (error) {
    console.error('登录失败:', error);
  }
};
</script>

<template>
  <el-dialog v-model="pop.loginPop" title="登录" width="500">
    <div class="form-out">
      <el-form name="register" @submit.native.prevent="submitForm">
        <!-- 账号 -->
        <el-form-item name="account">
          <el-input placeholder="请输入账号" v-model="formData.username" />
        </el-form-item>
        <!-- 密码 -->
        <el-form-item name="password">
          <el-input
            type="password"
            placeholder="请输入密码"
            v-model="formData.password"
          />
        </el-form-item>
        <!-- 登录 -->
        <el-form-item>
          <el-button type="primary" class="login-button" @click="submitForm">
            <span>立即登录</span>
          </el-button>
        </el-form-item>
        <!-- 跳转注册 -->
        <div class="register-out">
          <span>没有账号?</span>
          <span
            class="register-button"
            @click="
              () => {
                pop.changeLoginPop();
                pop.changeRegisterPop();
              }
            "
            >立即注册</span
          >
        </div>
      </el-form>
    </div>
  </el-dialog>
</template>

<style lang="less" scoped>
::v-deep(.el-form) {
  width: 50%;
}
.register-out {
  margin-left: 50px;
  .register-button:hover {
    color: #409eff;
  }
}
.form-out {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  .login-button {
    color: #fff;
    border-radius: 10px;
    width: 100%;
  }
}
</style>
