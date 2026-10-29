import request from "../utils/request";

/**
 * 文章搜索接口
 */
export const searchArticle = (data) => {
  return request({ method: "post", url: "/article/search", data });
};

/**
 * 文章获取接口
 */
export const getArticle = (data = {}) => {
  return request({ method: "get", url: "/article/get", data });
};

/**
 * 文章发布接口
 */
export const publishArticle = (data) => {
  return request({ method: "post", url: "/article/publish", data });
};
