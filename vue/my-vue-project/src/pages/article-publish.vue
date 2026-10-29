<script lang="ts" setup>
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import Header from "../components/Header.vue";
import { publishArticle } from "../api/article";
import { userStore } from "../store/user";
import router from "../router.js";
import { ref } from "vue";
import { ElMessage } from "element-plus";

const content = ref("");
const titleData = ref("");
const user = userStore();

const toolbar = [
  ["bold", "italic", "underline", "strike"],
  ["image", "blockquote", "code-block"],
  [{ list: "ordered" }, { list: "bullet" }],
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  ["clean"],
];

const handlePublish = async () => {
  if (!user.isLogin) {
    ElMessage.warning({
      message: "请先登录",
      type: "warning",
    });
    router.push("/login");
    return;
  }
  
  const title = titleData.value || "";
  const articleContent = content.value || "";
  
  if (!title.trim()) {
    ElMessage.warning({
      message: "请输入文章标题",
      type: "warning",
    });
    return;
  }
  
  if (!articleContent.trim()) {
    ElMessage.warning({
      message: "请输入文章内容",
      type: "warning",
    });
    return;
  }
  
  try {
    const res = await publishArticle({
      title: title,
      content: articleContent,
      author_id: user.userId || '1',
      up: 0,
      down: 0,
      category: '技术',
    });
    
    if (res && res.code === 200) {
      ElMessage.success({
        message: "发布成功",
        type: "success",
      });
      router.push("/home");
    } else {
      ElMessage.error({
        message: res?.message || "发布失败",
        type: "error",
      });
    }
  } catch (error) {
    ElMessage.error({
      message: error.response?.data?.message || "发布失败",
      type: "error",
    });
  }
};
</script>

<template>
  <div class="editor-out">
    <Header />
    <div class="editor">
      <div class="title">
        <div class="titl">文章标题</div>
        <el-input v-model="titleData"></el-input>
      </div>
      <div class="editor-com">
        <QuillEditor 
          v-model:content="content" 
          contentType="html" 
          theme="snow" 
          :toolbar="toolbar"
        />
      </div>
      <div class="publish" @click="handlePublish">
        <el-button class="plus-btn">
          <span>发布</span>
        </el-button>
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.publish {
  margin-top: 50px;
  .plus-btn {
    background-color: #fc5531;
    width: 80px;
    height: 32px;
    color: white;
    margin-left: 16px;
    &:hover {
      color: white;
    }
    border-radius: 14px;
  }
}
.editor-out {
  .editor {
    padding: 50px 0;
    width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-content: center;
    justify-content: center;
    align-items: center;
    .title {
      margin-bottom: 50px;
      display: flex;
      align-items: center;
      width: 500px;
      height: 40px;
      .titl {
        width: 100px;
      }
    }
    .editor-com {
      height: 600px;
    }
  }
}
</style>
