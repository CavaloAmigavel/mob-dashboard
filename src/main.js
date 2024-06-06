import { createApp } from "vue";
import "bootstrap/dist/css/bootstrap.css";
import { createPinia } from "pinia";
import DashboardPage from "./components/dashboard-page.vue";

const app = createApp(DashboardPage);
const pinia = createPinia();
app.use(pinia);
app.mount("#app");
