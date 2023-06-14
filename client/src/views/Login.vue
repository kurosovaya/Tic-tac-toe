<script setup>
import axios from "axios"
import store from "./store"
import { ref } from "vue"
import router from "@/router";


const login = ref("")

function loginUser() {
    let body = { "login": login.value }
    axios.post("http://localhost:5000/login", body)
        .then(response => (response.data)).then(
            data => {
                store.player_id = data.player_id
                $cookies.set("player_id", data.player_id)
                router.push({ name: "Menu" })
            }
        )
}
</script>

<template>
    <div class="login">
        <input v-model="login">
        <button @click="loginUser">Log in</button>
    </div>
</template>