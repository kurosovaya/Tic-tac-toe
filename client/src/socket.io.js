import socketio from 'socket.io-client'

const socket = socketio(import.meta.env.VITE_BASE_URL);

export default socket