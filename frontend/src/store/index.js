import Vuex from 'vuex';
import defaultModule from '@/store/defaultModule';
import users from '@/store/users/users';
import namespaces from "@/store/namespaces/namespaces";
import notes from "@/store/notes/notes";
import categories from "@/store/categories/categories";

export default new Vuex.Store({
    namespaced: true,
    modules: {
        defaultModule: defaultModule,
        users: users,
        namespaces: namespaces,
        notes: notes,
        categories: categories
    }
})

