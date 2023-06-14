<script setup>

const props = defineProps({
    x: Number,
    y: Number,
    value: String
})

const emit = defineEmits(["makeMove"])

function makeMove() {
    emit("makeMove", props.x, props.y)
}
</script>

<template>
    <button @click="makeMove" class="cell_button">{{ value }}</button>
</template>

<style scoped>
.cell_button {
    width: 200px;
    height: 200px;
    font-size: 90px;
}
</style>