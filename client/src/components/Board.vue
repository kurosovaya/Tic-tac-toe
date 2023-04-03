<script setup>
import BoardCell from "./BoardCell.vue"
const emit = defineEmits("make_move")

function make_move(x, y, elmn) {
    emit("make_move", x, y, elmn)
}

</script>

<template>
    <div class="board">
        <template v-for="y in 3">
            <BoardCell v-for="x in 3" :x="x" :y="y" @make_move="make_move"></BoardCell>
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