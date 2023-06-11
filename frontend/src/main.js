import { createApp } from 'vue'
import store from "./store"
import router from "./router"
import App from './App.vue'
import components from '@/components/UI'
import "bootstrap/dist/js/bootstrap.bundle.min"
import "bootstrap/dist/css/bootstrap.css"

const app = createApp(App)
components.forEach( component => {
    app.component(component.name, component)
})

app.use(store)
app.use(router)

app.mount('#app')
