<script>

export default{
    props: {
        x: Number,
        y: Number,
    },
    data() {
        return {            
            cell_value: null,
        }
    },
    methods: {
        make_move() {
            this.$emit("make_move", this.x, this.y, this)
        },
        mark() {
            this.cell_value = "O"
        }
    }
}
</script>

<template>
    <button @click="make_move" class="cell_button">{{cell_value}}</button>
</template>

<style scoped>
.cell_button {
    width: 200px;
    height: 200px;
    font-size: 90px;
}
</style>