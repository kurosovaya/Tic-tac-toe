<script setup>
import router from "@/router";
import axios from "axios"


function createGame() {    

    axios.post("http://localhost:5000/create_game")
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
    <button @click="createGame">Create game</button>
    <button @click="connectToGame">Connect to game</button>
</template>