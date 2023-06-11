<template>
    <div class="d-flex justify-content-between p-3" style="background: lightblue">
        <div class="d-flex">
            <div v-if="namespaces.items !== undefined">
                <div v-if="namespaces.items.length !== 0">
                    <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false" style="margin-right: 20px;"
                            @click="showNamespaces()">
                        Пространства страниц
                    </button>
                    <ul class="dropdown-menu">
                        <router-link to="/notes" v-for="namespace in namespaces.items" :key="namespace.id"
                                     @click="getNamespace(namespace)"
                                     style="text-decoration: none; color: black"
                        >
                            <li style="border-bottom: 1px solid grey;" class="p-2"
                            >
                                {{ namespace.name }}
                            </li>
                        </router-link>
                    </ul>
                </div>
            </div>
            <div class="text-center">
                <MyButton class="blue-buttons" @click="createNamespace">
                    Создать пространство страниц
                </MyButton>
            </div>
        </div>
        <div>
            <MyButton class="blue-buttons" @click="   this.$router.push('/profile')">
                Профиль
            </MyButton>
        </div>
        <div>
            <MyButton class="blue-buttons" @click="exit">
                Выйти
            </MyButton>
        </div>
    </div>

    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="closeModal"
    >
        <div>
            <input class="form-control" id="inputNamespaceName"
                   placeholder="Введите название пространства страниц"
                   v-model="name"
            >
        </div>
    </MyModal>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";

export default {
    name: "NamespacesNavBar",
    data() {
        return {
            name: '',
            modalVisible: false,
            modalButtons: [],
            modalMessage: '',
            needUpdate: false
        }
    },
    computed: {
        ...mapGetters(['namespaces']),
    },
    methods: {
        ...mapActions(['get_namespaces', "get_namespace", 'get_users_me']),
        ...mapMutations(['post_namespaces']),
        createNamespace() {
            this.modalVisible = true
            this.modalButtons = [
                {value: "Создать", status: true},
                {value: "Закрыть", status: false}
            ]
            this.needUpdate = true
        },
        closeModal(status) {
            this.modalVisible = false
            if (status === true) {
                this.post_namespaces({
                    name: this.name
                })
                this.name = ''
            }
            this.get_namespaces()
            this.get_users_me()
        },
        showNamespaces(){
            this.get_namespaces()
            this.get_users_me()
        },
        exit() {
            this.$router.push('/')
        },
        getNamespace(namespace) {
            this.get_namespace({
                namespace: namespace
            })
            this.$router.push('/notes')
        },
    },
    watch: {
        namespaces: {
            handler() {
                if (this.needUpdate) {
                    console.log('get namespaces')
                    this.get_namespaces()
                    this.get_users_me()

                }
                console.log(this.namespaces)
                this.needUpdate = false
            },
            immediate: true
        }
    },
    created() {
        this.get_namespaces()
    }
}
</script>

<style scoped>

</style>