import request from "../utils/request";

/**
 * 导航栏获取接口
 */
export const getNavigation = () => {
  return request({ method: "get", url: "/navigation/get" });
};
