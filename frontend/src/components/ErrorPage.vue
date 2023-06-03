<template>
    <div class="d-flex flex-column align-items-center justify-content-center h-100 w-100">
        <h1>ОШИБКА</h1>
        <h3>{{ message }}</h3>
        <router-link to="/">
            Вернуться на страницу авторизации
        </router-link>
    </div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
    name: "ErrorPage",
    computed: {
        ...mapGetters(['error']),
    },
    data() {
        return {
            message: ''
        }
    },
    watch: {
        error: {
            handler(error) {
                if (error.status === 401){
                    this.message = 'Ошибка авторизации. Неверно введен логин или пароль.'
                }
                if (error.status === 403){
                    this.message = 'Отсутствует доступ к странице.'
                }
                if (error.status === 422){
                    this.message = 'Ошибка авторизации. Заполните поля логин и пароль.'
                }
            },
            immediate: true
        },
    },

}
</script>

<style scoped>

</style>