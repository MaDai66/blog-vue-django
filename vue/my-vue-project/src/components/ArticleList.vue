<script setup>
import { onMounted, watch, ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const props = defineProps({
  category: {
    type: String,
    default: 'all'
  }
});

const router = useRouter();
const articles = ref([]);

// 获取文章接口逻辑
const getArticleData = async (cat = 'all') => {
  try {
    const url = cat === 'all' 
      ? 'http://127.0.0.1:8000/article/get' 
      : `http://127.0.0.1:8000/article/get?category=${encodeURIComponent(cat)}`;
    const res = await axios.get(url);
    if (res.data && res.data.code === 200) {
      articles.value = res.data.data;
    }
  } catch (error) {
    console.error('获取文章失败:', error);
  }
};

// 获取文章接口调用
onMounted(() => {
  getArticleData(props.category);
});

// 监听分类变化
watch(() => props.category, (newCategory) => {
  getArticleData(newCategory);
});

// 跳转详情页
const goDetail = (data) => {
  router.push({
    path: "/detail",
    query: { data: JSON.stringify(data) },
  });
};

// 获取默认图片
const getDefaultImage = () => {
  return 'https://picsum.photos/200/150?random=' + Math.floor(Math.random() * 1000);
};

// 去除HTML标签
const stripHtml = (html) => {
  if (!html) return '';
  const temp = document.createElement('div');
  temp.innerHTML = html;
  return temp.textContent || temp.innerText || '';
};
</script>

<template>
  <div class="article-list">
    <div v-if="articles.length === 0" class="empty-state">
      <p>暂无文章</p>
    </div>
    <div
      v-for="item in articles"
      :key="item.id"
      class="article-item"
      @click="goDetail(item)"
    >
      <!-- 左侧图片 -->
      <div class="article-image">
        <img :src="item.cover || getDefaultImage()" alt="文章封面" />
      </div>
      
      <!-- 中间分隔线 -->
      <div class="divider"></div>
      
      <!-- 右侧内容 -->
      <div class="article-content">
        <h3 class="article-title">{{ item.title }}</h3>
        <p class="article-summary" v-html="stripHtml(item.content).substring(0, 150) + '...'"></p>
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><View /></el-icon>
            {{ item.view_count || 0 }} 阅读
          </span>
          <span class="meta-item">
            <el-icon><Pointer /></el-icon>
            {{ item.up || 0 }} 赞
          </span>
          <span class="meta-item">
            <el-icon><Star /></el-icon>
            {{ item.collect_count || 0 }} 收藏
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.article-list {
  width: 100%;
  
  .article-item {
    display: flex;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid #e8e8e8;
    cursor: pointer;
    transition: background-color 0.3s;
    
    &:hover {
      background-color: #f5f5f5;
    }
    
    &:last-child {
      border-bottom: none;
    }
    
    // 左侧图片 - 固定大小
    .article-image {
      width: 180px;
      height: 120px;
      flex-shrink: 0;
      border-radius: 8px;
      overflow: hidden;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }
    
    // 中间分隔线
    .divider {
      width: 1px;
      height: 100px;
      background-color: #e8e8e8;
      margin: 0 20px;
      flex-shrink: 0;
    }
    
    // 右侧内容
    .article-content {
      flex: 1;
      min-width: 0;
      
      .article-title {
        font-size: 18px;
        font-weight: 600;
        color: #222226;
        margin: 0 0 10px 0;
        line-height: 1.4;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
      }
      
      .article-summary {
        font-size: 14px;
        color: #555666;
        margin: 0 0 12px 0;
        line-height: 1.5;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }
      
      .article-meta {
        display: flex;
        gap: 20px;
        
        .meta-item {
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 13px;
          color: #999;
          
          .el-icon {
            font-size: 14px;
          }
        }
      }
    }
  }
}

// 响应式
@media (max-width: 768px) {
  .article-list {
    .article-item {
      flex-direction: column;
      align-items: flex-start;
      
      .article-image {
        width: 100%;
        height: 180px;
        margin-bottom: 15px;
      }
      
      .divider {
        display: none;
      }
      
      .article-content {
        width: 100%;
      }
    }
  }
}
</style>