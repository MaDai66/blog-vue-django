import { defineStore } from "pinia";
import { ref } from "vue";

export const articleStore = defineStore("article", () => {
  const articleData = ref([]);

  // 改变文章列表内容
  const changeArticleData = (e) => {
    articleData.value = e;
  };

  return {
    articleData,
    changeArticleData,
  };
});
