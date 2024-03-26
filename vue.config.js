const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/acme": {
        target: "http://m2m.boxdev.site/",
        changeOrigin: true,
        pathRewrite: { "^/acme": "" },
      },
    },
  },
});
