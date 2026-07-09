<script setup>
import { ref, reactive } from "vue"
import router from "@/router"
import BoardCell from "@/components/BoardCell.vue"

const HUMAN = "X"
const COMPUTER = "O"

const difficulty = ref("hard")
const board = reactive([["", "", ""], ["", "", ""], ["", "", ""]])
const statusMessage = ref("Your move")
const gameOver = ref(false)
const thinking = ref(false)

const WIN_LINES = [
    [[0, 0], [0, 1], [0, 2]],
    [[1, 0], [1, 1], [1, 2]],
    [[2, 0], [2, 1], [2, 2]],
    [[0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [2, 1]],
    [[0, 2], [1, 2], [2, 2]],
    [[0, 0], [1, 1], [2, 2]],
    [[0, 2], [1, 1], [2, 0]],
]

function checkWinner(b) {
    for (const line of WIN_LINES) {
        const [[ax, ay], [bx, by], [cx, cy]] = line
        if (b[ax][ay] && b[ax][ay] === b[bx][by] && b[bx][by] === b[cx][cy]) {
            return b[ax][ay]
        }
    }
    return null
}

function isBoardFull(b) {
    return b.every(row => row.every(cell => cell !== ""))
}

function minimax(b, isMaximizing, depth) {
    const winner = checkWinner(b)
    if (winner === COMPUTER) return 10 - depth
    if (winner === HUMAN) return depth - 10
    if (isBoardFull(b)) return 0

    let best = isMaximizing ? -Infinity : Infinity
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            if (b[x][y] !== "") continue
            b[x][y] = isMaximizing ? COMPUTER : HUMAN
            const score = minimax(b, !isMaximizing, depth + 1)
            b[x][y] = ""
            best = isMaximizing ? Math.max(best, score) : Math.min(best, score)
        }
    }
    return best
}

function bestComputerMove() {
    let bestScore = -Infinity
    let move = null
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            if (board[x][y] !== "") continue
            board[x][y] = COMPUTER
            const score = minimax(board, false, 1)
            board[x][y] = ""
            if (score > bestScore) {
                bestScore = score
                move = { x, y }
            }
        }
    }
    return move
}

function randomComputerMove() {
    const empty = []
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            if (board[x][y] === "") empty.push({ x, y })
        }
    }
    return empty[Math.floor(Math.random() * empty.length)]
}

function finishIfOver() {
    const winner = checkWinner(board)
    if (winner) {
        gameOver.value = true
        statusMessage.value = winner === HUMAN ? "You win!" : "Computer wins!"
        return true
    }
    if (isBoardFull(board)) {
        gameOver.value = true
        statusMessage.value = "Draw"
        return true
    }
    return false
}

function handleMove(x, y) {
    if (gameOver.value || thinking.value || board[x][y] !== "") return

    board[x][y] = HUMAN
    if (finishIfOver()) return

    thinking.value = true
    statusMessage.value = "Computer's move"
    setTimeout(() => {
        const move = difficulty.value === "hard" ? bestComputerMove() : randomComputerMove()
        if (move) board[move.x][move.y] = COMPUTER
        thinking.value = false
        if (!finishIfOver()) statusMessage.value = "Your move"
    }, 300)
}

function resetBoard() {
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            board[x][y] = ""
        }
    }
    gameOver.value = false
    thinking.value = false
    statusMessage.value = "Your move"
}

function setDifficulty(value) {
    difficulty.value = value
    resetBoard()
}

function backToMenu() {
    router.push({ name: "Menu" })
}
</script>

<template>
    <div class="single-player">
        <div class="controls">
            <button :class="{ active: difficulty === 'easy' }" @click="setDifficulty('easy')">Easy</button>
            <button :class="{ active: difficulty === 'hard' }" @click="setDifficulty('hard')">Hard</button>
        </div>
        <div class="status">{{ statusMessage }}</div>
        <div class="board">
            <template v-for="(row, x) in board">
                <BoardCell v-for="(cell_value, y) in row" :key="`cell_${x}_${y}`" :x="x" :y="y" :value="cell_value"
                    @makeMove="handleMove"></BoardCell>
            </template>
        </div>
        <div class="game">
            <button @click="resetBoard">Restart</button>
            <button @click="backToMenu">Back to menu</button>
        </div>
    </div>
</template>

<style scoped>
.single-player {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.board {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr;
}

.controls, .game {
    display: flex;
    gap: 8px;
}

.controls button.active {
    font-weight: bold;
    text-decoration: underline;
}

.status {
    color: rgb(241, 241, 241);
    font-size: 20px;
}
</style>
