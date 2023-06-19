<script setup>
import { onMounted, ref } from "vue";
import store from "@/views/store";
import socket from "@/socket.io"
import { useRoute } from 'vue-router'

const socketInstance = socket
const messageInput = ref("")
const messagesArray = ref([])
const route = useRoute()

socketInstance.on("get_message", (player_name, message, time) => getMessage(player_name, message, time))

onMounted(() => {
     socketInstance.emit("get_chat_history", { "game_id": route.params.id }, (messages) => { 
          messages.forEach(message => {getMessage(message.player_name, message.message, message.time)}); 
     })
})

function sendMessage() {
     if (messageInput.value) {
          let localTime = new Date()          
          socketInstance.emit("send_message", {
               "game_id": store.gameId,
               "message": messageInput.value,
               "time": localTime.toISOString(),
               "player_id": store.playerId
          })
          messageInput.value = ""
     }
}

function convertTime(time) {
     let local_time = new Date(time)
     return `${("0" + local_time.getHours()).slice(-2)}:${("0" + local_time.getMinutes()).slice(-2)}`
}


function getMessage(player_name, message, time) {
     messagesArray.value.push({ "player_name": player_name, "message": message, "time": convertTime(time) })
}
</script>

<template>
     <div class="chat">
          <div class="messages">
               <div v-for="message in messagesArray" class="message">
                    <span class="time">{{ `${message.time} ` }}</span>
                    <span class="player_name">{{ message.player_name + ": " }}</span>
                    <span class="message_text"> {{ message.message }}</span>
               </div>
               <div id="anchor"></div>
          </div>
          <div class="input">
               <input class="input_text" @keydown.enter="sendMessage" v-model="messageInput">
               <button class="input_button" @click="sendMessage">Send</button>
          </div>
     </div>
</template>

<style scoped>
.message {
     color: white;
     overflow-anchor: none;
}

.chat {
     border: thick double #141414;
     background-color: #202020;
     box-sizing: border-box;
     position: absolute;
     width: 420px;
     height: 100%;
     right: 0;
     top: 0;
}

.messages {
     overflow: auto;
     height: 95%;
}

#anchor {
     overflow-anchor: auto;
     height: 1px;
}

.message_text {
     word-wrap: break-word;
}

.input {
     position: absolute;
     bottom: 0;
     width: 100%;
     align-items: center;
}

.input_text {
     width: 75%;
}

.input_button {
     width: 20%;
}

.time {
     color: grey;
}

.player_name {
     color: white;
}
</style>