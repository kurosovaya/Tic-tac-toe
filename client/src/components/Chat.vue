<script setup>
import { onMounted, ref } from "vue";
import store from "@/views/store";
import socket from "@/socket.io"
import { useRoute } from 'vue-router'

const socketInstance = socket
const message_input = ref("")
const messages_array = ref([])
const route = useRoute()

socketInstance.on("get_message", (player_name, message, time) => getMessage(player_name, message, time))

onMounted(() => {
     socketInstance.emit("get_chat_history", { "game_id": route.params.id }, (messages) => messages_array.value = messages)
})

function sendMessage() {
     if (message_input.value) {
          let local_time = new Date()
          let local_time_str = `${local_time.getHours()}:${local_time.getMinutes()}`
          socketInstance.emit("send_message", {
               "game_id": store.game_id,
               "message": message_input.value,
               "time": local_time_str,
               "player_id": store.player_id
          })
          message_input.value = ""
     }
}

function getMessage(player_name, message, time) {
     messages_array.value.push({ "player_name": player_name, "message": message, "time": time })
}
</script>

<template>
     <div class="chat">
          <div class="messages">
               <div v-for="message in messages_array" class="message">
                    <span class="time">{{ `${message.time} ` }}</span>
                    <span>{{ message.player_name + ": " }}</span>
                    <span class="message_text"> {{ message.message }}</span>
               </div>
               <div id="anchor"></div>
          </div>
          <div class="input">
               <input class="input_text" @keydown.enter="sendMessage" v-model="message_input">
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
}</style>