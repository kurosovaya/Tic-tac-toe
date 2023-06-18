import {reactive} from "vue"

const store = reactive({
    playerIdInner: null,
    get playerId() {
        return this.playerIdInner
    },
    set playerId(value) {
        this.playerIdInner = Number(value)
    },
    gameId: null
})

export default store