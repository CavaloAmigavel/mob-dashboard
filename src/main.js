import { createApp } from "vue";
import "bootstrap/dist/css/bootstrap.css";
import DashboardPage from "./components/dashboard-page.vue";
import { createPinia } from "pinia";

const pinia = createPinia();
const app = createApp(DashboardPage);

app.use(pinia);
app.mount("#app");
