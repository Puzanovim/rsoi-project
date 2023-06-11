import axios from "axios";
import defaultModule from '@/store/defaultModule';
/*import router from "../../router/index"*/

const state = {
    namespaces: [],
    namespace: {}
}

const actions = {
    //Получить все пространства страниц
    get_namespaces: (({commit}) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8080/namespaces/',
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            }
        };
        axios(config)
            .then(function (response) {
                commit('set_namespaces', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),
    //Получить пространство страниц
    get_namespace: (({commit}, namespace) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8080/namespaces/' + namespace.namespace.id,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            }
        };
        axios(config)
            .then(function (response) {
                commit('set_namespace', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),

    //Обновиьть пространство страниц
    put_namespace: ((namespaceId) => {
        let config = {
            method: 'put',
            url: 'http://localhost:8080/namespaces/' + namespaceId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            }
        };
        axios(config)
            .then(function () {
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),

}
const mutations = {
    set_namespaces: (state, namespaces) => {
        state.namespaces = namespaces
    },
    set_namespace: (state, namespace) => {
        state.namespace = namespace
    },
    //Создать пространство страниц
    post_namespaces: (state, name) => {
        let config = {
            method: 'post',
            url: 'http://localhost:8080/namespaces/',
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
            data: {
                'name': name.name
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
    //Удалить пространство страниц
    delete_namespace: (state, namespaceId) => {
        let config = {
            method: 'delete',
            url: 'http://localhost:8080/namespaces/' + namespaceId.namespaceId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
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

    //Добавить польователя в пространство страниц
    add_user_to_namespace: (state, id) => {
        let config = {
            method: 'post',
            url: 'http://localhost:8080/namespaces/' + id.namespaceId + '/users/' + id.userId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
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
    //Добавить польователя в пространство страниц
    delete_user_from_namespace: (state, namespaceId) => {
        let config = {
            method: 'delete',
            url: 'http://localhost:8080/namespaces/' + namespaceId + '/users',
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
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
}
const  getters = {
    namespaces(state) {
        return state.namespaces;
    },
    namespace(state) {
        return state.namespace;
    },
}


export default {
    state,
    actions,
    mutations,
    getters
}