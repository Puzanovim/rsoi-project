<template>
    <div class="w-100 h-100 d-flex flex-column justify-content-center align-items-center">
        <form class="row g-3" style="max-width: 80%;"
              @submit.prevent="registrationUser"
        >
            <div>
                <label for="inputFirstName" class="form-label">Имя</label>
                <input class="form-control" id="inputFirstName"
                       placeholder="Введите Имя"
                       v-model="firstName"
                >
            </div>
            <div>
                <label for="inputSecondName" class="form-label">Фамилия</label>
                <input class="form-control" id="inputSecondName"
                       placeholder="Введите Фамилию"
                       v-model="secondName"
                >
            </div>
            <div>
                <label for="inputLogin" class="form-label">Логин</label>
                <input class="form-control" id="inputLogin"
                       placeholder="Введите логин"
                       v-model="username"
                >
            </div>
            <div>
                <label for="inputEmail" class="form-label">Почта</label>
                <input class="form-control" id="inputEmail"
                       placeholder="Введите почту"
                       v-model="email"
                >
            </div>
            <div>
                <label for="inputPassword" class="form-label">Пароль</label>
                <input type="password" class="form-control" id="inputPassword"
                       placeholder="Введите пароль"
                       v-model="password"
                >
            </div>
            <div class="col-12 d-flex justify-content-center">
                <MyButton style="width: 250px" class="blue-buttons">
                    Зарегистрироваться
                </MyButton>
            </div>
            <div class="col-12 d-flex justify-content-center">
                <router-link to="/">
                    Войти
                </router-link>
            </div>
        </form>
    </div>

    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="checkAnswer"
    >
        {{this.modalMessage}}
    </MyModal>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
    name: "RegistrationPage",
    data() {
        return {
            firstName: '',
            secondName: '',
            username: '',
            email: '',
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
        ...mapActions(['push_registration']),
        registrationUser(){
            this.push_registration({
                firstName: this.firstName,
                secondName: this.secondName,
                username: this.username,
                email: this.email,
                password: this.password
            })
        },
        checkAnswer(){
            this.modalVisible = false
        }
    }
}
</script>

<style scoped>
</style>