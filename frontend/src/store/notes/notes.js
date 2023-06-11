import axios from "axios";
import defaultModule from "@/store/defaultModule";
/*
import router from "../../router/index"*/

const     state = {
    notes: [],
    note: {},
}

const actions = {
    //Получить все заметки для данного пространства страниц
    get_notes: (({commit}, namespaceId) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8080/notes/?namespace_id=' + namespaceId.namespaceId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            }
        };
        axios(config)
            .then(function (response) {
                commit('set_notes', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response)
            });
    }),
    //Получить заметку
    get_note: (({commit}, noteId) => {
        let config = {
            method: 'get',
            url: 'http://localhost:8080/notes/' + noteId.noteId,
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            }
        };
        axios(config)
            .then(function (response) {
                console.log('get_note')
                console.log(response.data)
                commit('set_note', response.data)
            })
            .catch(function (error) {
                console.log(error);
                console.log(error.response.status)
            });
    }),
    //Обновить заметку

    //Удалить заметку
}
const mutations = {
    set_notes: (state, notes) => {
        state.notes = notes
    },
    set_note: (state, note) => {
        state.note = note
    },
    //Создать заметку
    create_note: (state, note) => {
        let config = {
            method: 'post',
            url: 'http://localhost:8080/notes',
            headers: {
                'Authorization': 'Bearer ' + defaultModule.state.token
            },
            data: {
                'title': note.noteTitle,
                'text': note.noteText,
                'namespace_id': note.namespacesId,
                'categories': note.noteCategories
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
    //Удалтиь категорию
    delete_note: (state, noteId) => {
        let config = {
            method: 'delete',
            url: 'http://localhost:8080/notes/' + noteId.noteId,
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
    }
}
const  getters = {
    notes(state) {
        return state.notes
    },
    note(state) {
        return state.note
    }
}


export default {
    state,
    actions,
    mutations,
    getters
}