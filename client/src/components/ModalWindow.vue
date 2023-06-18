<script setup>

import { ref } from "vue";

const inviteUrl = ref(window.location.href)
const isSecure = ref(window.isSecureContext)

const props = defineProps({
    show: false
})


function copyURL() {
    navigator.clipboard.writeText(inviteUrl.value);
}
</script>

<template>
    <div v-if="show" class="modal">
        <div class="modal-content">
            <div class="copy_link">Invite: {{ inviteUrl }}</div>
            <button v-if="isSecure" button @click="copyURL">Copy</button>
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
    background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
    background-color: #181616;
    margin: 20% auto;
    padding: 20px;
    border: 1px solid #f8f8f8f8;
    width: 25%;
    height: 15%;
}

.copy_link {
    color: rgb(241, 241, 241);
}
</style>