<template>
    <div class="w-100 h-100 d-flex flex-column justify-content-center align-items-center">
        <form class="row g-3" style="max-width: 80%;"
              @submit.prevent="loginUser"
        >
            <div>
                <label for="inputLogin" class="form-label">Логин</label>
                <input class="form-control" id="inputLogin"
                       placeholder="Введите логин"
                       v-model="username"
                >
            </div>
            <div>
                <label for="inputPassword" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="inputPassword"
                       placeholder="Введите пароль"
                       v-model="password"
                >
            </div>
            <div class="d-flex justify-content-center">
                <MyButton style="width: 250px" class="blue-buttons">
                    Войти
                </MyButton>
            </div>
            <div class="d-flex justify-content-center">
                <router-link to="/registration">
                       Регистрация
                </router-link>
            </div>
        </form>
    </div>

    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="closeModal"
    >
        {{this.modalMessage}}
    </MyModal>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
export default {
    name: "AuthPage",
    data() {
        return {
            username: '',
            password: '',
            modalVisible: false,
            modalButtons: [],
            modalMessage: ''
        }
    },
    computed: {
        ...mapGetters(['error']),
    },
    methods: {
        ...mapActions(['push_login']),
        loginUser() {
            this.push_login({
                username: this.username,
                password: this.password
            })
        },
        closeModal() {
            this.modalVisible = false
        }
    },
    watch: {
        error: {
            handler(error) {
                if (error.status !== undefined){
                    this.modalVisible = true
                    this.modalButtons = [
                        {value: "Закрыть", status: true}
                    ]
                    if (error.status === 401){
                        this.modalMessage = 'Ошибка авторизации. Неверно введен логин или пароль.'
                    }
                    else if (error.status === 403){
                        this.modalMessage = 'Отсутствует доступ к странице.'
                    }
                    else if (error.status === 422){
                        this.modalMessage = 'Ошибка авторизации. Заполните поля логин и пароль.'
                    }
                    else this.modalMessage = 'Ошибка!'
                }
            },
            immediate: true
        },
    },
}
</script>

<style scoped>
</style>