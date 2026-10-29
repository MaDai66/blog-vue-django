<script setup>
import Header from "../components/Header.vue";
import ArticleList from "../components/ArticleList.vue";
import { ref, onMounted } from "vue";
import axios from "axios";

const activeTab = ref("all");
const searchValue = ref("");

// 分类标签 - 从后端获取
const categoryTabs = ref([
  { name: "all", label: "全部" },
  { name: "技术", label: "技术" },
  { name: "生活", label: "生活" },
  { name: "随笔", label: "随笔" },
  { name: "教程", label: "教程" },
  { name: "分享", label: "分享" },
]);

// 加载导航分类
const loadNavigation = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/navigation/get');
    if (res.data && res.data.code === 200 && res.data.data) {
      const navTabs = res.data.data.map(item => ({
        name: item.category,
        label: item.category
      }));
      categoryTabs.value = [{ name: "all", label: "全部" }, ...navTabs];
    }
  } catch (error) {
    console.error("加载导航分类失败:", error);
  }
};

// 页面加载时获取导航数据
onMounted(() => {
  loadNavigation();
});

// 分类点击处理
const handleCategoryClick = (category) => {
  activeTab.value = category;
};

// 左侧导航菜单
const leftMenu = [
  {
    
    items: [
      { name: "首页", icon: "HomeFilled", active: true },
      { name: "博客", icon: "Document" },
      { name: "下载", icon: "Download" },
      { name: "学习", icon: "Reading" },
      { name: "社区", icon: "ChatDotRound" }
    ]
  },
  {
    group: "服务",
    items: [
      { name: "GPU算力", icon: "Cpu", badge: "买1000送1200" },
      { name: "AI搜索", icon: "Search" },
      { name: "AtomGit", icon: "Link" },
      { name: "InsCode", icon: "Code" }
    ]
  },
  {
    group: "其他",
    items: [
      { name: "技术会议", icon: "Microphone" },
      { name: "订阅", icon: "Bell" },
      { name: "关注", icon: "Star" },
      { name: "收藏", icon: "Collection" },
      { name: "历史", icon: "Clock" },
      { name: "会员中心", icon: "Trophy" },
      { name: "创作中心", icon: "EditPen" },
      { name: "我的算力", icon: "Lightning", badge: "买一送一" }
    ]
  }
];
</script>

<template>
  <div class="home-container">
    <!-- 顶部 Header -->
    <Header />
    
    <!-- 主内容区 -->
    <div class="main-layout">
      <!-- 左侧导航栏 -->
      <aside class="left-sidebar">
        <div class="menu-group" v-for="(group, index) in leftMenu" :key="index">
          <div class="menu-list">
            <div 
              v-for="item in group.items" 
              :key="item.name"
              class="menu-item"
              :class="{ active: item.active }"
            >
              <el-icon class="menu-icon">
                <component :is="item.icon" />
              </el-icon>
              <span class="menu-text">{{ item.name }}</span>
              <span v-if="item.badge" class="menu-badge">{{ item.badge }}</span>
            </div>
          </div>
          <div v-if="index < leftMenu.length - 1" class="group-divider"></div>
        </div>
      </aside>
      
      <!-- 右侧内容区 -->
      <div class="right-content">
        <!-- 分类标签 - 固定在顶部 -->
        <div class="category-tabs-wrapper">
          <div class="category-tabs">
            <div 
              v-for="tab in categoryTabs" 
              :key="tab.name"
              class="tab-item"
              :class="{ active: activeTab === tab.name }"
              @click="handleCategoryClick(tab.name)"
            >
              {{ tab.label }}
            </div>
          </div>
        </div>
        
        <!-- 中间内容区 -->
        <main class="content-area">
          <!-- 文章列表 -->
          <div class="article-list-container">
            <ArticleList :category="activeTab" />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-top: 60px; /* 为固定的Header留出空间 */
}

.main-layout {
  display: flex;
  min-height: calc(100vh - 60px); /* 减去Header的高度 */
}

// 左侧导航栏
.left-sidebar {
  width: 270px;
  background-color: #fff;
  border-right: 1px solid #e0e0e0;
  padding: 20px 0;
  height: calc(100vh - 60px); /* 减去Header的高度 */
  position: fixed;
  left: 0;
  top: 60px; /* 距离顶部的距离，Header高度 */
  overflow-y: auto;
  
  .menu-group {
    margin-bottom: 0;
    
    .group-divider {
      height: 1px;
      background-color: #e0e0e0;

      margin: 10px 20px;
    }
    
    .menu-list {
      .menu-item {
        display: flex;
        align-items: center;
        padding: 8px 20px;
        cursor: pointer;
        transition: all 0.3s;
        position: relative;
        
        &:hover {
          background-color: #f5f5f5;
          color: #ff6b6b;
        }
        
        &.active {
          background-color: #fff0f0;
          color: #ff6b6b;
          font-weight: 600;
        }
        
        .menu-icon {
          font-size: 16px;
          margin-right: 10px;
          width: 20px;
          text-align: center;
        }
        
        .menu-text {
          font-size: 14px;
          flex: 1;
        }
        
        .menu-badge {
          font-size: 10px;
          padding: 2px 6px;
          background: #ff6b6b;
          color: #fff;
          border-radius: 10px;
          white-space: nowrap;
        }
      }
    }
  }
}

// 右侧内容区
.right-content {
  flex: 1;
  margin-left: 270px; /* 为左侧导航栏留出空间 */
  display: flex;
  flex-direction: column;
}

// 分类标签容器 - 固定在顶部
.category-tabs-wrapper {
  position: fixed;
  top: 60px;
  left: 270px;
  right: 0;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
  z-index: 999;
}

// 分类标签
.category-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  padding: 10px 20px;
  padding-top: 20px;
  
  .tab-item {
    padding: 6px 12px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
    border-radius: 4px;
    
    &:hover {
      color: #ff6b6b;
    }
    
    &.active {
      background-color: #ff6b6b;
      color: #fff;
    }
  }
}

// 中间内容区
.content-area {
  flex: 1;
  padding: 20px;
  padding-top: 60px; /* 为固定的分类标签留出空间 */
  
  // 文章列表
  .article-list-container {
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;
  }
}

// 响应式
@media (max-width: 1200px) {
  .left-sidebar {
    display: none;
  }
  
  .right-content {
    margin-left: 0;
  }
  
  .category-tabs-wrapper {
    left: 0;
  }
}
</style>
