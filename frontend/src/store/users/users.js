import axios from "axios";
import defaultModule from '@/store/defaultModule';
/*import router from "../../router/index"*/

const state = {
    users: {},
    user: {},
    user_me: {},
    statistics: {}
}

const actions = {
    //Информация о всех пользователях
    get_users: (({commit}) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8030/users/',
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
        };
        axios(config)
            .then(function (response) {
                commit('set_users', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),
    //Информация о пользователе по id
    get_user: (({commit, userId}) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8030/users/' + userId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
        };
        axios(config)
            .then(function (response) {
                commit('set_user', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),
    //Информация о текущем пользователе
    get_users_me: (({commit}) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8080/users/me/',
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
        };
        axios(config)
            .then(function (response) {
                console.log(response.data.is_superuser)
                if (response.data.is_superuser){
                    let config = {
                        method: 'get',
                        url: 'http://localhost:8080/statistics',
                        headers: {
                            'Authorization': 'Bearer ' + defaultModule.state.token
                        },
                    };
                    axios(config)
                        .then(function (response) {
                            console.log(response.data.items.length)
                      /*      if (response.data.items.length === 0){
                                let arr = [
                                    {"service": 'gateway', "description": 'gateway service', "created_time": '02-06-2023 14:59:05',
                                        "id": '7ycbh5d6-3784-48e9-c78d-0cidhr7c8sju'},
                                    {"service": 'identity', "description": 'identity-provider service', "created_time": '02-06-2023 14:59:05',
                                        "id": '9djch5d6-8907-48e9-b33c-8c78dyfhjw67'},
                                    {"service": 'namespaces', "description": 'namespaces service', "created_time": '02-06-2023 14:59:05',
                                        "id": 'eu372yc-1782-48e9-s87d-gyeu7cydjkcl'},
                                    {"service": 'notes', "description": 'notes service', "created_time": '02-06-2023 14:59:05',
                                        "id": 'fj8ud78f-4678-48e9-c67s-8cjsidkfu7xhd6'},
                                    {"service": 'category', "description": 'category service', "created_time": '02-06-2023 14:59:05',
                                        "id": '0djf7e6d-3742-48e9-l35x-o9wdgh56cghdu'},
                                    {"service": 'frontend', "description": 'frontend service', "created_time": '02-06-2023 14:59:05',
                                        "id": '7g67sc56-9856-48e9-o66i-7cgsh46wyduikcl'},
                                    {"service": 'statistic', "description": 'statistics service', "created_time": '02-06-2023 14:59:05',
                                        "id": '9csjudy7-1856-48e9-z78g-9fikjfuchs78fu'}
                                ]
                                commit('set_statistics', arr)
                            }*//*
                            else {*/
                                commit('set_statistics', response.data.items)
                            /*}*/
                        })
                        .catch(function (error){
                            console.log(error);
                            console.log(error.response)
                        })
                }
                commit('set_user_me', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),
}
const mutations = {
    set_users: (state, users) => {
        state.users = users
    },
    set_user: (state, user) => {
        state.user = user
    },
    set_user_me: (state, user_me) => {
        state.user_me = user_me
    },
    set_statistics: (state, statistics) => {
        state.statistics = statistics
    },
    //Обновить информацию о пользователе
    put_user: (state, user) => {
        let config = {
            method: 'put',
            url: 'http://localhost:8030/users/' + user.id,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
            data: {
                'username': user.username,
                'first_name': user.first_name,
                'second_name': user.second_name,
                'email': user.username,
                'is_superuser': user.is_superuser,
                'id': user.id
            }
        };
        axios(config)
            .then(function () {
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    },

    //Удалить пользователя
    delete_user: (state, userId) => {
        let config = {
            method: 'delete',
            url: 'http://localhost:8030/users/' + userId.userId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
        };
        axios(config)
            .then(function () {
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    },

}
const  getters = {
    users(state) {
        return state.users;
    },
    user(state) {
        return state.user;
    },
    user_me(state) {
        return state.user_me;
    },
    statistics(state) {
        return state.statistics
    }
}


export default {
    state,
    actions,
    mutations,
    getters
}