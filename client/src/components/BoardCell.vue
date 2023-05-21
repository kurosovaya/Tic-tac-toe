<script>

export default{
    props: {
        x: Number,
        y: Number,
        value: String
    },
    methods: {
        make_move() {
            this.$emit("make_move", this.x, this.y)
        }
    }
}
</script>

<template>
    <button @click="make_move" class="cell_button">{{value}}</button>
</template>

<style scoped>
.cell_button {
    width: 200px;
    height: 200px;
    font-size: 90px;
}
</style>