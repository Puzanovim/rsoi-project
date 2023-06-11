import axios from "axios";
import router from "../router"

const state = {
    token: '',
    error: {},
}

const actions = {
    //Вход
    push_login: (({commit}, auth) => {
        console.log(auth)
        let data = new FormData();
        data.append('username', auth.username);
        data.append('password', auth.password);
        let config = {
            method: 'post',
            url: 'http://localhost:8080/login',
            headers: {},
            data: data
        };
        axios(config)
            .then(function (response) {
                commit('set_token', response.data.access_token)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),
    //Регистрация \ создание новго пользователя
    push_registration: (({commit}, registration) => {
    /*    let data = new FormData();
        data.append('first_name', registration.firstName);
        data.append('second_name', registration.secondName);
        data.append('username', registration.username);
        data.append('email', registration.email);
        data.append('password', registration.password);*/

        let config = {
            method: 'post',
            url: 'http://localhost:8080/users/',
            headers: {},
            data: {
                first_name: registration.firstName,
                second_name: registration.secondName,
                username: registration.username,
                email: registration.email,
                password: registration.password
            }
        };
        axios(config)
            .then(function () {
                router.push('/')
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
                commit('set_error', error.response)
            });
    }),
}
const mutations = {
    set_token: (state, token) => {
        state.token = token
        router.push('/profile')
    },
    set_error: (state, error) => {
        state.error = error
    },
}
const  getters = {
    token(state){
        return state.token;
    },
    error(state){
        return state.error;
    },
}


export default {
    state,
    actions,
    mutations,
    getters
}