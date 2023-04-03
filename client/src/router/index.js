import { createRouter, createWebHistory} from 'vue-router'

import Home from "@/views/Login.vue"
import Game from "@/views/Game.vue"
import Menu from "@/views/Menu.vue"


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: "/", name: "Login", component: Home},
        {path: "/game/:id", name: "game", component: Game},
        {path: "/menu", name: "Menu", component: Menu}
    ]
})

export default router
