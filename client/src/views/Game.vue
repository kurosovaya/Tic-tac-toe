<script setup>
import { onMounted, ref } from "vue";
import Board from "../components/Board.vue"
import ModalWindow from "@/components/ModalWindow.vue";
import VueCookies from 'vue-cookies'
import router from "@/router";
import { useRouter, useRoute } from 'vue-router'
import axios from "axios"

let player_id = null
const game_id = ref("")
const route = useRoute()
const modal_window = ref(null)

onMounted(() => {

    player_id = VueCookies.get("player_id")

    if (!player_id) {
        router.push({path: "/"})
    }
    game_id.value = route.params.id
    let socket = new WebSocket("wss://localhost:5000/echo", ["soap", "wamp"])

    // socket.onopen = function(e) {
    //     alert("[open] Соединение установлено");
    //     alert("Отправляем данные на сервер");
    //     socket.send("Меня зовут Джон");
    // };
})

function make_move(x, y, elmn) {
    let body = {"x_axis": x - 1, "y_axis": y - 1, "game_id": game_id}
    axios.post("/move", body)
    elmn.mark()
}

</script>

<template>
    <ModalWindow ref="modal_window"></ModalWindow>
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