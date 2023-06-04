import {reactive} from "vue"

const store = reactive({
    player_id_inner: null,
    get player_id() {
        return this.player_id_inner
    },
    set player_id(value) {
        this.player_id_inner = Number(value)
    },
    game_id: null
})

export default store