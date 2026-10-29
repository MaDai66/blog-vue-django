<script setup>
import Login from "./Login.vue";
import Register from "./Register.vue";
import { popStore } from "../store/pop";
import { userStore } from "../store/user";
import { useRoute } from "vue-router";
import router from "../router";
import { ref } from "vue";

const user = userStore();
const pop = popStore();
const location = useRoute();
const searchValue = ref("");

const nav_list = [
  { name: "博客", url: "#" },
  { name: "下载", url: "#" },
  { name: "学习", url: "#" },
  { name: "社区", url: "#" },
  { name: "知道", url: "#" },
  { name: "GitCode", url: "#" },
  { name: "InsCode", url: "#" },
  { name: "会议", url: "#" },
  { name: "学习", url: "#" },
];
</script>

<template>
  <div class="main-header">
    <div class="header-left">
      <a class="header-icon" href="#/home">
        <img src="../assets/20240829093757.png" alt="" />
      </a>
    </div>
    
    <!-- 搜索框 -->
    <div class="header-search" v-if="!(location.path === '/publish')">
      <el-input
        v-model="searchValue"
        placeholder="扣子工作流"
        class="search-input"
        size="large"
      >
        <template #append>
          <el-button type="danger" class="search-btn">搜索</el-button>
        </template>
      </el-input>
      <el-button type="primary" class="ai-search-btn">AI 搜索</el-button>
    </div>
    
    <div class="header-user">
      <!-- 已登录 -->
      <el-dropdown placement="bottom-end" v-if="user.isLogin">
        <span class="user-name">{{ user.username }}</span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="() => router.push('/profile')">
              个人主页
            </el-dropdown-item>
            <el-dropdown-item style="color: red" @click="() => user.logout()">
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <!-- 未登录 -->
      <el-button plain @click="() => pop.changeLoginPop()" v-else>
        登录
      </el-button>

      <el-button
        class="plus-btn"
        @click="() => router.push('/publish')"
        v-if="!(location.path === '/publish')"
      >
        <el-icon>
          <Plus />
        </el-icon>
        <span>发布</span>
      </el-button>
    </div>
    <Login />
    <Register />
  </div>
</template>

<style scoped lang="less">
::v-deep(.el-dialog__header) {
  display: flex;
  justify-content: center;
}

.main-header {
  width: 100vw;
  height: 60px;
  padding: 0 24px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  z-index: 1000;
  
  .header-left {
    display: flex;
    align-items: center;
    .back {
      margin-left: 30px;
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    .back :hover {
      color: #409eff;
    }
    .header-icon {
      float: left;
      height: 100%;
      overflow: hidden;
      width: 130px;
      height: 60px;
      img {
        height: 100%;
      }
    }
  }
  
  .header-search {
    display: flex;
    gap: 10px;
    flex: 1;
    max-width: 600px;
    margin: 0 20px;
    
    .search-input {
      flex: 1;
      
      :deep(.el-input__wrapper) {
        border-radius: 4px 0 0 4px;
        border: 1px solid #e0e0e0;
      }
      
      :deep(.el-input-group__append) {
        border-radius: 0 4px 4px 0;
        background-color: #ff6b6b;
        border-color: #ff6b6b;
        
        .search-btn {
          color: #fff;
          border: none;
          background: transparent;
        }
      }
    }
    
    .ai-search-btn {
      border-radius: 4px;
      background: #6c757d;
      border: none;
      color: #fff;
    }
  }
  
  .header-user {
    float: right;
    height: 100%;
    display: flex;
    align-items: center;
    span.user-name {
      display: block;
      width: 32px;
      height: 32px;
      border: 1px solid #ccc;
      border-radius: 50%;
      line-height: 32px;
      text-align: center;
      font-size: 14px;
    }
    .plus-btn {
      background-color: #ff6b6b;
      width: 80px;
      height: 32px;
      color: white;
      margin-left: 16px;
      &:hover {
        color: white;
      }
      border-radius: 4px;
    }
  }
}
</style>
../store/user
