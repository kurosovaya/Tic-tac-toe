<script setup>
import { onMounted, ref } from "vue";
import Board from "../components/Board.vue"
import Chat from "@/components/Chat.vue"
import ModalWindow from "@/components/ModalWindow.vue"
import router from "@/router";
import { useRoute } from 'vue-router'
import socket from "@/socket.io"
import store from "./store"


let playerId = null
const gameId = ref("")
const route = useRoute()
const showDialog = ref(true)
const socketInstance = socket

onMounted(() => {
    if (!$cookies.isKey("playerId") && !store.playerId) {
        router.push({ name: "Login" })
    }
    if (!store.playerId) {
        store.playerId = $cookies.get("playerId")
    }

    playerId = store.playerId

    if (!playerId) {
        router.push({ name: "Login" })
    }
    gameId.value = route.params.id
    store.gameId = route.params.id


    socketInstance.emit('connect_to_game', { "game_id": gameId.value, "player_id": playerId }, (response) => { console.log(response) })
    socketInstance.on('connected_to_game', () => { console.log("player connected") });
    socketInstance.on('game_ready', () => { showDialog.value = false; console.log("game ready") })
    socketInstance.on("end_game", (player_name) => { alert(`END GAME ${player_name} WIN`) })
    socketInstance.on("draw", () => { alert("Draw") })

})

function restartGame() {
    socketInstance.emit("restart_game", { "game_id": gameId.value, "player_id": playerId })
}

function newGame() {

}

</script>

<template>
    <ModalWindow :show="showDialog"></ModalWindow>
    <div class="main">
        <div class="game">
            <Board/>
            <button @click="restartGame">Restart</button>
            <!-- <button @click="newGame">New game</button> -->
            <div class="logo">Pluton-waffen.inc</div>
        </div>
        <Chat></Chat>
    </div>
</template>


<style scoped>
.main {
    display: flex;
}

.logo {
    color: rgb(241, 241, 241);
    position: absolute;
    bottom: 1%;
    left: 1%;
}
</style>