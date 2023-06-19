<script setup>

import router from "@/router";
import { ref } from "vue";

const emit = defineEmits(["closeDialog"])

const gameId = ref(null)

const props = defineProps({
    show: Boolean
})

function connectToGame() {
    router.push({name: 'game', params: { id: gameId.value }})
}

function close() {
    emit("closeDialog")
}
</script>

<template>
    <div v-if=show class="modal">
        <div class="modal-content">
            <button class="close_btn" @click="close"></button>
            <div class="copy_link">Enter game ID {{gameId}}</div>
            <input v-model="gameId">
            <button @click="connectToGame">Connect</button>
        </div>        
    </div>
</template>

<style scoped>
.modal {
    display: block;
    position: fixed;
    z-index: 1;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #181616;
  margin: 20% auto;
  padding: 5px;
  border: 1px solid #f8f8f8f8;
  width: 25%;
  height: 15%;
}

.copy_link {
    color: rgb(241, 241, 241);
}

.close_btn {
    float: right;
    width: 15px;
    height: 15px;
}
</style>