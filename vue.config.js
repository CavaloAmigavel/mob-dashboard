const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/acme": {
        target: process.env.VUE_APP_ACME_URL,
        changeOrigin: true,
        pathRewrite: { "^/acme": "" },
      },
    },
  },
});
