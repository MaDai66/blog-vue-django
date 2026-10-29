<script setup>
import { ref } from "vue";
import { getNavigation } from "../api/navigation";
import { onMounted } from "vue";

const navi_data = ref([]);

const arrow = ref(true);

// 鼠标移入展开
const handleEnter = (e) => {
  const target = e.target;
  target.style.transition = "none";
  target.style.height = "auto";
  const height = target.offsetHeight;
  target.style.transition = "height 0.4s ease";
  target.style.height = height + "px";
  target.offsetHeight; // 触发重绘
  arrow.value = false;
};
// 鼠标移除收起
const handleLeave = (e) => {
  const target = e.target;
  target.style.height = "74px";
  arrow.value = true;
};

onMounted(async () => {
  const res = await getNavigation();
  if (res && res.code === 200 && res.data) {
    navi_data.value = res.data;
  }
});
</script>

<template>
  <div class="navi" @mouseenter="handleEnter" @mouseleave="handleLeave">
    <span>
      <el-icon v-if="!arrow"><ArrowUp /></el-icon>
      <el-icon v-else><ArrowDown /></el-icon>
    </span>
    <a href="" v-for="item in navi_data" :key="item.name">
      {{ item.category }}
    </a>
  </div>
</template>

<style lang="less" scoped>
.navi {
  background: #fff;
  box-shadow: 0 0 2px #ccc;
  height: 74px;
  border-radius: 4px;
  overflow: hidden;
  padding: 24px 24px 0;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  box-sizing: border-box;
  position: relative;

  a {
    color: black;
    display: block;
    width: fit-content;
    font-size: 16px;
    margin: 10px auto;
    padding-right: 24px;
    &:hover {
      color: #fc5531;
    }
  }
  span {
    display: block;
    width: 32px;
    height: 12px;
    background: #eee;
    position: absolute;
    left: 0;
    right: 0;
    margin: auto;
    bottom: 0;
    border-radius: 4px 4px 0 0;
    text-align: center;
    line-height: 12px;
    color: #999;
  }
}
</style>
