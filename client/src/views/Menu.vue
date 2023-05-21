<script setup>
import { ref, onMounted } from "vue";
import router from "@/router";
import axios from "axios"
import store from "./store"
import ConnectGameModalWindow from "@/components/ConnectGameModalWindow.vue";


const showModal = ref(null)

onMounted(() => {
    if (!$cookies.isKey("player_id") && !store.player_id) {
        router.push({name: "Login"})
    }
    if (!store.player_id) {
        store.player_id = $cookies.get("player_id")
    }
})

function createGame() {    

    let body = {player_creator: store.player_id}    
    axios.post("http://localhost:5000/create_game", body)
    .then(response => (response.data)).then(
        data => {
            let game_id = data.game_id
            connectToGame(game_id)
        }
    )
}

function connectToGame(game_id) {
    router.push({name: 'game', params: { id: game_id }})
}
</script>

<template>
    <ConnectGameModalWindow :show="showModal"></ConnectGameModalWindow>
    <button @click="createGame">Create game</button>
    <button @click="showModal = true">Connect to game</button>
</template>