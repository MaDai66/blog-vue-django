<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Header from "../components/Header.vue";
import dayjs from "dayjs";
import request from "../utils/request";
import { userStore } from "../store/user";
import { popStore } from "../store/pop";
import { ElMessage } from "element-plus";

const router = useRouter();
const user = userStore();
const pop = popStore();
const articleData = ref({});
const authorName = ref("");
const isLiked = ref(false);
const isDisliked = ref(false);
const isFollowing = ref(false);

const { query } = useRoute();

const getArticleData = async () => {
  articleData.value = JSON.parse(query.data);
  
  // 获取作者信息
  if (articleData.value.author_id) {
    try {
      const res = await request({
        url: `/user/profile/${articleData.value.author_id}`,
        method: 'get'
      });
      if (res && res.code === 200 && res.data) {
        authorName.value = res.data.username;
      }
    } catch (error) {
      console.error('获取作者信息失败:', error);
    }
  }
};

onMounted(() => {
  getArticleData();
});

// 点击作者跳转到作者主页
const goToAuthorProfile = () => {
  if (articleData.value.author_id) {
    router.push({ path: '/user-profile', query: { userId: articleData.value.author_id } });
  }
};

// 点赞（支持切换）
const handleUp = async () => {
  try {
    const res = await request({
      url: '/article/up',
      method: 'post',
      data: {
        article_id: articleData.value.id,
        user_id: user.userId || 'anonymous'
      }
    });
    if (res && res.code === 200) {
      articleData.value.up = res.data;
      isLiked.value = res.liked;
      if (isLiked.value) {
        isDisliked.value = false;
      }
    }
  } catch (error) {
    console.error('点赞失败:', error);
  }
};

// 点踩（支持切换）
const handleDown = async () => {
  try {
    const res = await request({
      url: '/article/down',
      method: 'post',
      data: {
        article_id: articleData.value.id,
        user_id: user.userId || 'anonymous'
      }
    });
    if (res && res.code === 200) {
      articleData.value.down = res.data;
      isDisliked.value = !res.liked;
      if (isDisliked.value) {
        isLiked.value = false;
      }
    }
  } catch (error) {
    console.error('点踩失败:', error);
  }
};

// 关注/取消关注作者
const handleFollow = async () => {
  console.log('handleFollow called');
  console.log('user.isLogin:', user.isLogin);
  console.log('user.userId:', user.userId);
  console.log('user.username:', user.username);
  console.log('articleData.author_id:', articleData.value.author_id);
  
  if (!user.isLogin || !user.userId) {
    ElMessage.error('请先登录');
    pop.changeLoginPop();
    return;
  }
  
  const currentUserId = String(user.userId);
  const authorId = String(articleData.value.author_id);
  
  if (currentUserId === authorId) {
    ElMessage.error('不能关注自己');
    return;
  }
  
  try {
    const res = await request({
      url: '/user/follow',
      method: 'post',
      data: {
        follower_id: currentUserId,
        followed_id: authorId,
        action: isFollowing.value ? 'unfollow' : 'follow'
      }
    });
    console.log('关注操作响应:', res);
    if (res && res.code === 200) {
      isFollowing.value = !isFollowing.value;
      ElMessage.success(isFollowing.value ? '关注成功' : '取消关注成功');
    } else if (res && res.code !== 200) {
      ElMessage.error(res.message || '操作失败');
    }
  } catch (error) {
    console.error('关注操作失败:', error);
    if (error.response && error.response.data && error.response.data.message) {
      ElMessage.error(error.response.data.message);
    } else {
      ElMessage.error('操作失败');
    }
  }
};

</script>

<template>
  <div class="big-box">
    <!-- 头部 -->
    <Header />
    <main>
      <h1>{{ articleData.title }}</h1>
      <div class="illustrate">
        <div class="top">
          <span class="first">原创</span>
          <span class="author-link" @click="goToAuthorProfile">作者: {{ authorName || articleData.author }}</span>
          <span class="follow-btn" :class="{ active: isFollowing }" @click="handleFollow">
            {{ isFollowing ? '已关注' : '+ 关注' }}
          </span>
          <span>
            <el-icon><Clock /></el-icon>
            {{ dayjs(articleData.publish_time).format("YYYY-MM-DD HH:mm:ss") }}
          </span>
          <span class="action-btn" :class="{ active: isLiked }" @click="handleUp">
            <el-icon><ArrowUp /></el-icon>
            {{ isLiked ? '点赞' : '点赞' }} {{ articleData.up }}
          </span>
          <span class="action-btn" :class="{ active: isDisliked }" @click="handleDown">
            <el-icon><ArrowDown /></el-icon>
            {{ isDisliked ? '点踩' : '点踩' }} {{ articleData.down }}
          </span>
        </div>
      </div>
      <div class="content">
        <div v-html="articleData.content" />
      </div>
    </main>
  </div>
</template>

<style lang="less" scoped>
header {
  position: sticky;
  top: 0;
}
.big-box {
  width: 100vw;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: scroll;
}
main {
  background: white;
  width: 1200px;
  min-height: 100vh;
  margin: 8px auto 0;
  box-shadow: 0 0 2px 2px #eee;
  border-radius: 4px;
  padding: 24px;
  h1 {
    font-size: 24px;
    margin: 10px 0;
  }
  .illustrate {
    height: 72px;
    background: #efefef;
    border-radius: 4px;
    padding: 10px;
    box-sizing: border-box;
    span {
      margin-right: 16px;
      &.first {
        display: inline-block;
        height: 50%;
        width: 40px;
        background: #ff5531;
        color: white;
        text-align: center;
      }
      &.last {
        display: inline-block;
        font-size: 12px;
        float: right;
      }
      &.author-link {
        color: #409eff;
        cursor: pointer;
        &:hover {
          text-decoration: underline;
        }
      }
      &.follow-btn {
        color: #ff5531;
        cursor: pointer;
        padding: 4px 12px;
        border-radius: 4px;
        border: 1px solid #ff5531;
        transition: all 0.3s;
        &:hover {
          background-color: #fff0f0;
        }
        &.active {
          background-color: #ff5531;
          color: white;
          &:hover {
            background-color: #e04a2a;
          }
        }
      }
      &.action-btn {
        color: #666;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 4px;
        transition: all 0.3s;
        border: 1px solid transparent;
        &:hover {
          background-color: #ff5531;
          color: white;
        }
        &.active {
          border: 1px solid #ff5531;
          background-color: #ff5531;
          color: white;
        }
      }
      font-size: 14px;
      color: #999aaa;
    }
    .bottom {
      margin-top: 10px;
    }
  }
  .content {
    border-left: 8px solid #dddfe4;
    background: #eef0f4;
    padding: 16px;
    margin-top: 20px;
    p {
      font-size: 16px;
      line-height: 24px;
    }
  }
}
</style>
