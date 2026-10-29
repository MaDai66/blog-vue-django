import request from "../utils/request";

/**
 * 注册接口
 */
export const getRegister = (data) => {
  return request({ method: "post", url: "/user/register", data });
};

/**
 * 登录接口
 */
export const getLogin = (data) => {
  return request({ method: "post", url: "/user/login", data });
};

/**
 * 获取用户个人信息
 */
export const getUserProfile = (userId) => {
  return request({ method: "get", url: `/user/profile/${userId}` });
};

/**
 * 获取用户统计信息
 */
export const getUserStats = (userId) => {
  return request({ method: "get", url: `/user/stats/${userId}` });
};

/**
 * 获取用户文章列表
 */
export const getUserArticles = (userId) => {
  return request({ method: "get", url: `/article/user/${userId}` });
};
