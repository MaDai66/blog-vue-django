import axios from "axios";

/**
 * 创建axios实例
 */
const service = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: "3000",
});

/**
 * 请求拦截
 */
service.interceptors.request.use((config) => {
  // 对所有需要认证的 API 添加认证头
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.authorization = token;
  }
  return config;
});

/**
 * 响应拦截
 */
service.interceptors.response.use((res) => {
  return res.data;
});

/**
 * 封装请求函数
 */
const request = (options) => {
  if (options.method === "get" && options.data) {
    options.params = options.data;
  }
  return service(options);
};

export default request;
