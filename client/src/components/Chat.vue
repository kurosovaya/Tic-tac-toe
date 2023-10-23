<script setup>
import { onMounted, ref } from "vue";
import store from "@/views/store";
import socket from "@/socket.io"
import { useRoute } from 'vue-router'

const socketInstance = socket
const messageInput = ref("")
const messagesArray = ref([])
const route = useRoute()

socketInstance.on("get_message", (message) => getMessage(message))
socketInstance.on("send_system_message", (text) => sendSystemMessage(text));

onMounted(() => {
     socketInstance.emit("get_chat_history", { "game_id": route.params.id }, (messages) => { 
          messages.forEach(message => getMessage(message)); 
     })
})

function sendSystemMessage(message) {
     let localTime = new Date()
     socketInstance.emit("send_system_message", {
               "game_id": store.gameId,
               "message": message,
               "time": localTime.toISOString(),
               "message_type": 'system_message'
          })
}

function sendMessage() {
     if (messageInput.value) {
          let localTime = new Date()          
          socketInstance.emit("send_message", {
               "game_id": store.gameId,
               "message": messageInput.value,
               "time": localTime.toISOString(),
               "player_id": store.playerId,
               "message_type": 'user_message'
          })
          messageInput.value = ""
     }
}

function convertTime(time) {
     let local_time = new Date(time)
     return `${("0" + local_time.getHours()).slice(-2)}:${("0" + local_time.getMinutes()).slice(-2)}`
}


function getMessage(message) {
     messagesArray.value.push({ "player_name": message.player_name, "message": message.message, "time": convertTime(message.time), "message_type": message.message_type })
}
</script>

<template>
     <div class="chat">
          <div class="messages">
               <div v-for="message in messagesArray" class="message">
                    <span v-if="message.time" class="time">{{ `${message.time} ` }}</span>
                    <span v-if="message.player_name" class="player_name">{{ message.player_name + ": " }}</span>
                    <span v-if="message.message" :class="{message_text: message.message_type==='user_message', message_system_text: message.message_type==='system_message'}"> {{ message.message }}</span>
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

.message_system_text {
     color: rgba(255, 255, 255, 0.253);
     font-style: italic;
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