<script setup>
import { onMounted, ref } from "vue";
import Board from "../components/Board.vue"
import ModalWindow from "@/components/ModalWindow.vue"
import router from "@/router";
import { useRoute } from 'vue-router'
import socket from "@/socket.io"
import store from "./store"



let player_id = null
const game_id = ref("")
const route = useRoute()
const showDialog = ref(true)
const socketInstance = socket
const emit = defineEmits("make_move")

onMounted(() => {
    if (!$cookies.isKey("player_id") && !store.player_id) {
        router.push({name: "Login"})
    }
    if (!store.player_id) {
        store.player_id = $cookies.get("player_id")
    }

    player_id = store.player_id

    if (!player_id) {
        router.push({name: "Login"})
    }
    game_id.value = route.params.id
    store.game_id = route.params.id
    
    
    socketInstance.emit('connect_to_game', {"game_id": game_id.value, "player_id": player_id}, (response) => {console.log(response)})    
    socketInstance.on('connected_to_game', () => {console.log("player connected")});
    socketInstance.on('game_ready', () => {showDialog.value=false; console.log("game ready")})
    socketInstance.on("end_game", (player_name) => {alert(`END GAME ${player_name} WIN`)})

})


function restart_game(game_id) {
    
}

function new_game() {

}

</script>

<template>
    <ModalWindow :show="showDialog"></ModalWindow>
    <div class="game">
        <Board @make_move="make_move"/>        
        <button @click="restart_game">Restart</button>
        <button @click="new_game">New game</button>
        <div class="copy_link">Pluton-waffen.inc</div>
    </div>
</template>


<style scoped>
.copy_link {
    color: rgb(241, 241, 241);
}
</style>