<script setup>
import { ref, onMounted } from "vue";
import router from "@/router";
import axios from "axios"
import store from "./store"
import ConnectGameModalWindow from "@/components/ConnectGameModalWindow.vue";


const showModal = ref(false)

onMounted(() => {
    if (!$cookies.isKey("playerId") && !store.playerId) {
        router.push({ name: "Login" })
    }
    if (!store.playerId) {
        store.playerId = $cookies.get("playerId")
    }
})

function createGame() {
    let body = { player_creator: store.playerId }
    axios.post("/create_game", body)
        .then(response => (response.data)).then(
            data => {
                let gameId = data.game_id
                connectToGame(gameId)
            }
        )
}

function connectToGame(gameId) {
    router.push({ name: 'game', params: { id: gameId } })
}
</script>

<template>
    <ConnectGameModalWindow :show="showModal"></ConnectGameModalWindow>
    <button @click="createGame">Create game</button>
    <button @click="showModal = true">Connect to game</button>
</template>