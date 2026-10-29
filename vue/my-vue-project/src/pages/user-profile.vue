<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import Header from '../components/Header.vue';
import axios from 'axios';
import defaultAvatar from '../img/b_0a3207ca7c96aaf9febca517bdbf61f4.jpg';
import dayjs from 'dayjs';

const route = useRoute();

// 当前访问的用户ID（从URL参数获取）
const targetUserId = ref('');

// 用户信息
const userInfo = ref({
  username: '用户名',
  avatar: defaultAvatar,
  bio: '暂无简介',
  location: '未知',
  joinDate: '2026-01-01'
});

// 用户统计信息
const userStats = ref({
  articles: 0,
  followers: 0,
  following: 0
});

// 用户文章列表
const userArticles = ref([]);

// 关注列表
const followingList = ref([]);

// 粉丝列表
const followerList = ref([]);

// 激活的标签页
const activeTab = ref('recent');

// 加载所有数据
const loadAllData = () => {
  loadUserInfo();
  loadUserStats();
  loadUserArticles();
  loadFollowingList();
  loadFollowerList();
};

// 加载用户信息
const loadUserInfo = async () => {
  try {
    console.log('开始调用 getUserProfile', targetUserId.value);
    const res = await axios.get(`http://127.0.0.1:8000/user/profile/${targetUserId.value}`);
    console.log('getUserProfile 返回结果:', res);
    if (res.data && res.data.code === 200 && res.data.data) {
      const data = res.data.data;
      userInfo.value = {
        username: data.username || '用户名',
        avatar: data.avatar || 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=user%20avatar%20portrait%20professional&image_size=square',
        bio: data.bio || data.first_name || '暂无简介',
        location: data.location || '未知',
        joinDate: data.date_joined || '2026-01-01'
      };
    }
  } catch (error) {
    console.error('加载用户信息失败:', error);
  }
};

// 加载用户统计信息
const loadUserStats = async () => {
  try {
    console.log('开始调用 getUserStats', targetUserId.value);
    const res = await axios.get(`http://127.0.0.1:8000/user/stats/${targetUserId.value}`);
    console.log('getUserStats 返回结果:', res);
    if (res.data && res.data.code === 200 && res.data.data) {
      const data = res.data.data;
      userStats.value = {
        articles: data.articles || 0,
        followers: data.followers || 0,
        following: data.following || 0
      };
    }
  } catch (error) {
    console.error('加载用户统计信息失败:', error);
  }
};

// 加载用户文章列表
const loadUserArticles = async () => {
  try {
    console.log('开始调用 getUserArticles', targetUserId.value);
    const res = await axios.get(`http://127.0.0.1:8000/article/user/${targetUserId.value}`);
    console.log('getUserArticles 返回结果:', res);
    if (res.data && res.data.code === 200 && res.data.data) {
      userArticles.value = res.data.data.map(article => ({
        ...article,
        create_time: dayjs(article.publish_time).format('YYYY-MM-DD HH:mm'),
        view_count: article.view_count || 0,
        comment_count: article.comment_count || 0
      })) || [];
    }
  } catch (error) {
    console.error('加载用户文章列表失败:', error);
  }
};

// 加载关注列表
const loadFollowingList = async () => {
  try {
    console.log('开始调用 getFollowingList', targetUserId.value);
    const res = await axios.get(`http://127.0.0.1:8000/user/follow/list/${targetUserId.value}`);
    console.log('getFollowingList 返回结果:', res);
    if (res.data && res.data.code === 200 && res.data.data) {
      followingList.value = res.data.data.map(item => ({
        id: item.followed.id,
        username: item.followed.username
      })) || [];
    }
  } catch (error) {
    console.error('加载关注列表失败:', error);
  }
};

// 加载粉丝列表
const loadFollowerList = async () => {
  try {
    console.log('开始调用 getFollowerList', targetUserId.value);
    const res = await axios.get(`http://127.0.0.1:8000/user/follower/list/${targetUserId.value}`);
    console.log('getFollowerList 返回结果:', res);
    if (res.data && res.data.code === 200 && res.data.data) {
      followerList.value = res.data.data.map(item => ({
        id: item.follower.id,
        username: item.follower.username
      })) || [];
    }
  } catch (error) {
    console.error('加载粉丝列表失败:', error);
  }
};

// 页面加载时获取数据
onMounted(() => {
  // 从URL参数中获取目标用户ID
  targetUserId.value = route.query.userId || '1';
  loadAllData();
});

// 监听路由参数变化
watch(() => route.query.userId, (newUserId) => {
  if (newUserId) {
    targetUserId.value = newUserId;
    loadAllData();
  }
});
</script>

<template>
  <Header />
  <main>
    <div class="main-box">
      <!-- 顶部用户信息 -->
      <div class="user-header">
        <div class="user-info-top">
          <div class="user-avatar">
            <img :src="userInfo.avatar" alt="用户头像" />
          </div>
          <div class="user-info">
            <div class="user-name-section">
              <h1 class="username">{{ userInfo.username }}</h1>
              <div class="user-tags">
                <span class="tag">LV1</span>
                <span class="tag">新手</span>
              </div>
            </div>
            <p class="bio">{{ userInfo.bio }}</p>
            <div class="user-meta">
              <span class="meta-item">{{ userInfo.location }}</span>
              <span class="meta-item">加入于 {{ userInfo.joinDate }}</span>
            </div>
            <div class="user-stats-top">
              <span class="stat-item-top">{{ userStats.articles }} 篇文章</span>
              <span class="stat-item-top">{{ userStats.followers }} 位粉丝</span>
              <span class="stat-item-top">{{ userStats.following }} 关注</span>
            </div>
          </div>
          <div class="user-actions">
            <el-button type="primary" size="large">关注</el-button>
            <el-button size="large">私信</el-button>
            <el-dropdown placement="bottom-end">
              <el-button size="large">更多</el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>编辑资料</el-dropdown-item>
                  <el-dropdown-item>账号设置</el-dropdown-item>
                  <el-dropdown-item>管理博文</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
      
      <!-- 内容区域 -->
      <div class="content-area">
        <!-- 左侧边栏 -->
        <div class="sidebar-left">
          <!-- 个人成就 -->
          <div class="achievement-section">
            <h3 class="section-title">个人成就</h3>
            <div class="achievement-items">
              <div class="achievement-item">
                <span class="achievement-icon">🏆</span>
                <span class="achievement-text">获得 2 次赞赏</span>
              </div>
              <div class="achievement-item">
                <span class="achievement-icon">💬</span>
                <span class="achievement-text">获得 22 次评论</span>
              </div>
              <div class="achievement-item">
                <span class="achievement-icon">👁️</span>
                <span class="achievement-text">博客总访问量 108,787</span>
              </div>
              <div class="achievement-item">
                <span class="achievement-icon">⭐</span>
                <span class="achievement-text">能力等级 Lv1</span>
              </div>
            </div>
            
            <!-- 技术栈 -->
            <div class="tech-stack">
              <h4 class="tech-title">技术栈</h4>
              <div class="tech-tags">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">Django</span>
                <span class="tech-tag">Vue</span>
                <span class="tech-tag">JavaScript</span>
              </div>
            </div>
          </div>
          
          <!-- 专栏 -->
          <div class="column-section">
            <h3 class="section-title">TA的专栏</h3>
            <div class="column-items">
              <div class="column-item">
                <span class="column-name">Web自动化</span>
                <span class="column-count">1篇</span>
              </div>
              <div class="column-item">
                <span class="column-name">大数据</span>
                <span class="column-count">1篇</span>
              </div>
              <div class="column-item">
                <span class="column-name">人工智能</span>
                <span class="column-count">1篇</span>
              </div>
            </div>
          </div>
          
          <!-- 关注列表 -->
          <div class="follow-section">
            <h3 class="section-title">TA关注的人 ({{ followingList.length }})</h3>
            <div class="follow-list">
              <div v-for="user in followingList.slice(0, 5)" :key="user.id" class="follow-item">
                <span class="follow-avatar">👤</span>
                <span class="follow-name">{{ user.username }}</span>
              </div>
              <div v-if="followingList.length === 0" class="empty-follow">
                暂无关注
              </div>
            </div>
          </div>
          
          <!-- 粉丝列表 -->
          <div class="follower-section">
            <h3 class="section-title">TA的粉丝 ({{ followerList.length }})</h3>
            <div class="follow-list">
              <div v-for="user in followerList.slice(0, 5)" :key="user.id" class="follow-item">
                <span class="follow-avatar">👤</span>
                <span class="follow-name">{{ user.username }}</span>
              </div>
              <div v-if="followerList.length === 0" class="empty-follow">
                暂无粉丝
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧文章列表 -->
        <div class="content-right">
          <!-- 文章标签页 -->
          <div class="article-tabs">
            <el-tabs v-model="activeTab">
              <el-tab-pane label="最近" name="recent"></el-tab-pane>
              <el-tab-pane label="文章" name="articles"></el-tab-pane>
              <el-tab-pane label="专栏" name="columns"></el-tab-pane>
              <el-tab-pane label="代码" name="code"></el-tab-pane>
              <el-tab-pane label="资源" name="resources"></el-tab-pane>
              <el-tab-pane label="收藏" name="favorites"></el-tab-pane>
              <el-tab-pane label="关注/互动" name="interactions"></el-tab-pane>
              <el-tab-pane label="更多" name="more"></el-tab-pane>
            </el-tabs>
            <div class="search-box">
              <el-input placeholder="搜索" size="small"></el-input>
            </div>
          </div>
          
          <!-- 文章列表 -->
          <div class="articles-section">
            <div class="article-list">
              <div v-for="article in userArticles" :key="article.id" class="article-item">
                <div class="article-content-wrapper">
                  <h3 class="article-title">{{ article.title }}</h3>
                  <p class="article-summary">{{ article.content }}</p>
                  <div class="article-meta">
                    <span class="meta-item">{{ article.create_time }}</span>
                    <span class="meta-item">{{ article.view_count }} 阅读</span>
                    <span class="meta-item">{{ article.comment_count }} 评论</span>
                    <span class="meta-item">{{ article.up }} 点赞</span>
                  </div>
                </div>
              </div>
              <div v-if="userArticles.length === 0" class="empty-articles">
                <p>暂无发布的文章</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style lang="less" scoped>
main {
  background-color: hsla(0, 0%, 98%, 0.8);
  overflow: hidden;
  padding: 30px 0;

  .main-box {
    width: 1200px;
    margin: 0 auto;
  }
  
  // 顶部用户信息
  .user-header {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 30px;
    
    .user-info-top {
      display: flex;
      align-items: flex-start;
      
      .user-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        overflow: hidden;
        margin-right: 30px;
        
        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }
      
      .user-info {
        flex: 1;
        
        .user-name-section {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          
          .username {
            font-size: 24px;
            font-weight: 600;
            margin: 0 15px 0 0;
          }
          
          .user-tags {
            display: flex;
            gap: 8px;
            
            .tag {
              font-size: 12px;
              padding: 2px 8px;
              border-radius: 10px;
              background-color: #f0f0f0;
              color: #666;
            }
          }
        }
        
        .bio {
          font-size: 14px;
          color: #666;
          margin: 0 0 15px 0;
          line-height: 1.5;
        }
        
        .user-meta {
          font-size: 12px;
          color: #999;
          margin-bottom: 10px;
          
          .meta-item {
            margin-right: 20px;
          }
        }
        
        .user-stats-top {
          display: flex;
          gap: 20px;
          
          .stat-item-top {
            font-size: 14px;
            color: #666;
          }
        }
      }
      
      .user-actions {
        display: flex;
        gap: 10px;
        
        button {
          width: 100px;
        }
      }
    }
  }
  
  // 内容区域
  .content-area {
    display: flex;
    gap: 30px;
    
    // 左侧边栏
    .sidebar-left {
      width: 300px;
      
      .achievement-section,
      .column-section,
      .follow-section {
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        
        .section-title {
          font-size: 16px;
          font-weight: 600;
          margin: 0 0 15px 0;
          padding-bottom: 10px;
          border-bottom: 1px solid #eee;
        }
      }
      
      .achievement-section {
        .achievement-items {
          .achievement-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            
            .achievement-icon {
              font-size: 16px;
              margin-right: 10px;
            }
            
            .achievement-text {
              font-size: 14px;
              color: #666;
            }
          }
        }
        
        .tech-stack {
          margin-top: 20px;
          
          .tech-title {
            font-size: 14px;
            font-weight: 600;
            margin: 0 0 10px 0;
          }
          
          .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            
            .tech-tag {
              font-size: 12px;
              padding: 4px 12px;
              border-radius: 12px;
              background-color: #f0f0f0;
              color: #666;
            }
          }
        }
      }
      
      .column-section {
        .column-items {
          .column-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            
            &:last-child {
              border-bottom: none;
            }
            
            .column-name {
              font-size: 14px;
              color: #333;
            }
            
            .column-count {
              font-size: 12px;
              color: #999;
            }
          }
        }
      }
      
      .follow-section,
      .follower-section {
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        
        .section-title {
          font-size: 16px;
          font-weight: 600;
          margin: 0 0 15px 0;
          padding-bottom: 10px;
          border-bottom: 1px solid #eee;
        }
        
        .follow-list {
          .follow-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            
            &:last-child {
              border-bottom: none;
            }
            
            .follow-avatar {
              font-size: 20px;
              margin-right: 10px;
            }
            
            .follow-name {
              font-size: 14px;
              color: #333;
            }
          }
          
          .empty-follow {
            text-align: center;
            color: #999;
            padding: 10px 0;
          }
        }
      }
    }
    
    // 右侧内容
    .content-right {
      flex: 1;
      
      // 文章标签页
      .article-tabs {
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        padding: 15px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .search-box {
          width: 200px;
        }
      }
      
      // 文章列表
      .articles-section {
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        padding: 20px;
        
        .article-list {
          .article-item {
            padding: 20px 0;
            border-bottom: 1px solid #eee;
            
            &:last-child {
              border-bottom: none;
            }
            
            .article-content-wrapper {
              .article-title {
                font-size: 18px;
                font-weight: 600;
                margin: 0 0 10px 0;
                color: #333;
                
                &:hover {
                  color: #409eff;
                  cursor: pointer;
                }
              }
              
              .article-summary {
                font-size: 14px;
                color: #666;
                margin: 0 0 15px 0;
                line-height: 1.5;
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
              }
              
              .article-meta {
                font-size: 12px;
                color: #999;
                
                .meta-item {
                  margin-right: 20px;
                }
              }
            }
          }
          
          .empty-articles {
            text-align: center;
            padding: 40px 0;
            color: #999;
          }
        }
      }
    }
  }
}
</style>