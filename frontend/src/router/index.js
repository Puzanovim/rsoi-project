import { createWebHistory, createRouter } from "vue-router";
import AuthPage from "@/components/AuthPage.vue";
import UserProfile from "@/components/UserProfile.vue";
import NotesPage from "@/components/NotesPage.vue";
import RegistrationPage from "@/components/RegistrationPage.vue";
import store from '../store'
import ErrorPage from "@/components/ErrorPage.vue";
import NotePage from "@/components/NotePage.vue";
import EditNotePage from "@/components/EditNotePage.vue";
import CategoriesPage from "@/components/CategoriesPage.vue";
import CreateNotePage from "@/components/CreateNotePage.vue";


const routes = [
    {
        path: "/",
        name: "AuthPage",
        component: AuthPage,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: "/registration",
        name: "RegistrationPage",
        component: RegistrationPage,
        meta: {
            requiresAuth: false
        }
    },
    {
        path: "/profile",
        name: "UserProfile",
        component: UserProfile,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/notes",
        name: "NotesPage",
        component: NotesPage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/note",
        name: "NotePage",
        component: NotePage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/edit-note",
        name: "EditNotePage",
        component: EditNotePage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/create-note",
        name: "CreateNotePage",
        component: CreateNotePage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/categories",
        name: "CategoriesPage",
        component: CategoriesPage,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/error",
        name: "ErrorPage",
        component: ErrorPage,
        meta: {
            requiresAuth: false
        }
    },



];

const router = createRouter({
    history: createWebHistory(),
    routes,
});


router.beforeEach((to, from, next) => {
    if (to.matched.some(r => r.meta.requiresAuth)) {// Определить, требует ли маршрут разрешения входа в систему
        if (store.getters.token) {// через vuex, если в данный момент есть логин
            next();
        } else {
            next({
                path: '/',
                query: {redirect: to.fullPath}
            })
        }
    } else {
        next();
    }
});


export default router;