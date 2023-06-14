<script setup>
import BoardCell from "./BoardCell.vue"
import { ref } from "vue"
import socket from "@/socket.io"
import store from "@/views/store"
import { useRoute } from 'vue-router'

const cellsList = ref([])
const socketInstance = socket
const route = useRoute()

socketInstance.on('make_move', (x_axis, y_axis, sight) => { cellsList.value[x_axis][y_axis].cell_value = sight })
socketInstance.on("restart_game", () => (reset_field()))
socketInstance.emit("get_field", { "game_id": route.params.id }, (response) => { set_field(response) })


function set_field(field) {
    for (let x = 0; x < 3; x++) {
        let temp_array = []
        for (let y = 0; y < 3; y++) {
            temp_array.push({ x: x, y: y, cell_value: field[x][y] == 0 ? "" : field[x][y] })
        }
        cellsList.value.push(temp_array)
    }
}

function reset_field() {
    for (let x = 0; x < 3; x++) {
        let temp_array = []
        for (let y = 0; y < 3; y++) {
            temp_array.push({ x: x, y: y, cell_value: "" })
        }
        cellsList.value[x] = temp_array
    }
}

function make_move(x, y) {
    let body = { "x_axis": x, "y_axis": y, "game_id": store.game_id, "player_id": store.player_id }
    socketInstance.emit("check_move", body)
}

</script>

<template>
    <div class="board">
        <template v-for="rowList in cellsList">
            <BoardCell v-for="(cell_data, index) in rowList" :key="`cell_${index}`" :x="cell_data.x" :y="cell_data.y"
                :value="cell_data.cell_value" @make_move="make_move"></BoardCell>
        </template>
    </div>
</template>

<style scoper>
.board {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
}
</style>