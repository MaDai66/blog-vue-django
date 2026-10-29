<script setup>
import { popStore } from "../store/pop";
import { getRegister } from "../api/user";
import { ref } from "vue";

const pop = popStore();
// 账号
const formData = ref({
  username: "",
  password: "",
});

// 错误信息
const errorMessage = ref("");
const errorList = ref([]);

// 注册按钮
const submitForm = async () => {
  // 重置错误信息
  errorMessage.value = "";
  errorList.value = [];
  
  try {
    const res = await getRegister(formData.value);
    if (res === "注册成功") {
      pop.changeRegisterPop();
      pop.changeLoginPop();
    } else {
      // 处理错误信息
      if (res.code === 400) {
        errorMessage.value = res.message;
        errorList.value = res.errors || [];
      } else {
        console.log(res);
      }
    }
  } catch (error) {
    // 处理 axios 错误
    if (error.response && error.response.data) {
      const res = error.response.data;
      if (res.code === 400) {
        errorMessage.value = res.message;
        errorList.value = res.errors || [];
      } else {
        console.log(res);
      }
    } else {
      console.log(error);
    }
  }
};
</script>

<template>
  <el-dialog v-model="pop.registerPop" title="注册" width="500">
    <div class="form-out">
      <!-- 错误信息展示 -->
      <div v-if="errorMessage || errorList.length > 0" class="error-message">
        <div class="error-title">{{ errorMessage }}</div>
        <ul v-if="errorList.length > 0" class="error-list">
          <li v-for="(error, index) in errorList" :key="index">{{ error }}</li>
        </ul>
      </div>
      
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
        <!-- 注册 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm" class="login-button">
            <span>立即注册</span>
          </el-button>
        </el-form-item>
        <!-- 跳转登录 -->
        <div class="register-out">
          <span>已有账号?</span>
          <span
            class="register-button"
            @click="
              () => {
                pop.changeRegisterPop();
                pop.changeLoginPop();
              }
            "
            >立即登录</span
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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  .login-button {
    color: #fff;
    border-radius: 10px;
    width: 100%;
  }
}
.error-message {
  width: 50%;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fef0f0;
  border: 1px solid #fbc4c4;
  border-radius: 4px;
  color: #f56c6c;
  .error-title {
    font-weight: bold;
    margin-bottom: 5px;
  }
  .error-list {
    margin: 0;
    padding-left: 20px;
    li {
      margin-top: 3px;
    }
  }
}
</style>
