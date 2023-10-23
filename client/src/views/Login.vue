<script setup>
import axios from "axios"
import store from "./store"
import { ref } from "vue"
import router from "@/router";


const login = ref("")

function loginUser() {
    if (login.value) {
        let body = { "login": login.value }
        axios.post("/login", body)
            .then(response => (response.data)).then(
                data => {
                    store.playerId = data.player_id
                    $cookies.set("playerId", data.player_id)
                    router.push({ name: "Menu" })
                }
            )
    }
}
</script>

<template>
    <div class="login">
        <input @keydown.enter="loginUser" v-model="login">
        <button @click="loginUser">Log in</button>
    </div>
</template>