<script>
import axios from "axios"

// 
// const router = useRouter()
export default {
data() {
    return {
        login: "",
        user_id: null
    }
},
methods: {
    login_post()
    {       
        let body = {"login": this.login}
        axios.post("http://localhost:5000/login", body)
        .then(response => (response.data)).then(
            data => {                
                this.user_id = data.player_id,
                this.$cookies.set("player_id", this.user_id)
                this.$router.push({name: "Menu"})
            }
        )
    }
}
}
</script>

<template>
    <div class="login">
        <input v-model="login">
        <button @click="login_post">Log in</button>
    </div>
</template>