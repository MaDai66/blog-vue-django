<script lang="ts" setup>
import { QuillEditor } from "@vueup/vue-quill";
import { ref, watch } from "vue";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const props = defineProps<{
  modelValue?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();

const toolbar = ref([
  ["bold", "italic", "underline", "strike"],
  ["image", "blockquote", "code-block"],

  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }],
  [{ indent: "-1" }, { indent: "+1" }],

  [{ header: [1, 2, 3, 4, 5, 6, false] }],

  ["clean"],
]);

const localContent = ref(props.modelValue || "");

watch(() => props.modelValue, (newVal) => {
  localContent.value = newVal || "";
});

const emitUpdate = () => {
  emit("update:modelValue", localContent.value);
};

defineExpose({
  getContent: () => localContent.value,
});
</script>

<template>
  <QuillEditor 
    v-model="localContent" 
    contentType="html" 
    theme="snow" 
    :toolbar="toolbar"
    @update:modelValue="emitUpdate"
  />
</template>
