<script setup>
import { onMounted, ref } from "vue";
import Board from "../components/Board.vue"
import ModalWindow from "@/components/ModalWindow.vue";
import router from "@/router";
import { useRouter, useRoute } from 'vue-router'
import axios from "axios"
import socketio from 'socket.io-client'
import store from "./store";



let player_id = null
const game_id = ref("")
const route = useRoute()
const showDialog = ref(true)

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
    
    const SocketInstance = socketio('http://localhost:5000');
    SocketInstance.emit('connect_to_game', {"game_id": game_id.value, "player_id": player_id}, (response) => {console.log(response)})    
    SocketInstance.on('connected_to_game', () => {console.log("player connected")});
    SocketInstance.on('game_ready', () => {showDialog.value=false; console.log("game ready")})

})

function make_move(x, y, elmn) {
    let body = {"x_axis": x - 1, "y_axis": y - 1, "game_id": game_id}
    axios.post("/move", body)
    elmn.mark()
}

</script>

<template>
    <ModalWindow :show="showDialog"></ModalWindow>
    <div class="game">
        <Board @make_move="make_move"/>        
        <div class="copy_link">Pluton-waffen.inc</div>
    </div>
</template>


<style scoped>
.copy_link {
    color: rgb(241, 241, 241);
}
</style>