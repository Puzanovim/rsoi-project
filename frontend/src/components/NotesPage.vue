<template>
    <NamespacesNavBar/>
    <div class="m-3">
        <div>
            <p>
                Список заметок:
            </p>
        </div>
        <div v-if="notes.items !== undefined" class="d-flex">
            <div class="card m-3" v-for="note in notes.items" :key="note.id" @click="openNote(note.id)">
                <div class="card-body">
                    <h1>{{note.title}}</h1>
                    <p> {{ note.text.length > 100 ? note.text.substring(0, 100) + '...' : note.text }}</p>
                </div>
            </div>
        </div>
        <div v-else>
            <p>
                Заметок пока нет.
            </p>
        </div>
        <div>
            <MyButton class="blue-buttons" @click="addNote">
                Создать заметку
            </MyButton>
        </div>
        <div class="mt-3">
            <p>Список категорий пространства:</p>
            <div v-if="categories.items !== undefined" class="d-flex">
                <div class="card m-4" v-for="category in categories.items" :key="category.id">
                    <div class="card-body">
                        <p>{{category.name}}</p>
                    </div>
                </div>
            </div>
            <div>
                <MyButton class="blue-buttons" @click="this.$router.push('/categories')">
                    Редактировать категории
                </MyButton>
            </div>
        </div>

<!--        <div class="mt-3">
            <p>Список пользователей в пространстве страниц:</p>
            <div>

            </div>
            <div class="mt-3">
                <MyButton class="blue-buttons" @click="addUserToNamespace">
                    Добавить пользователя в пространство страниц
                </MyButton>
            </div>
        </div>-->

        <div class="mt-3">
            <MyButton style="background: red; border: red" @click="deleteNamespace">
                Удалить пространство страниц
            </MyButton>
        </div>
    </div>

    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="closeModal"
    >
        {{this.modalMessage}}
    </MyModal>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";
import NamespacesNavBar from "@/components/NamespacesNavBar.vue";

export default {
    name: "NotesPage",
    components: {NamespacesNavBar},
    data() {
        return {
            modalButtons: [],
            modalMessage: '',
            modalVisible: false,
            needUpdate: false
        }
    },
    computed: {
        ...mapGetters(['notes', 'namespace', 'categories']),
    },
    methods: {
        ...mapActions(['get_notes', 'get_categories', 'get_note']),
        ...mapMutations(['post_category', 'delete_namespace']),
        deleteNamespace(){
            this.modalVisible = true
            this.modalButtons = [
                {value: "Да", status: true},
                {value: "Нет", status: false}
            ]
            this.modalMessage = 'Вы действительно хотите удалить это пространство станиц?'
        },
        closeModal(status){
            this.modalVisible = false

            if (status === true) {
                this.delete_namespace({
                    namespaceId: this.namespace.id
                })
                this.$router.push('/profile')
            }
        },
        addNote() {
            this.$router.push('/create-note')
            this.needUpdate = true
        },
        exit() {
            this.$router.push('/')
        },
        openNote(noteId) {
            this.get_note({
                noteId: noteId
            })
            this.$router.push('/note')
            console.log('Замтека')
        },
        addUserToNamespace(){

        }
    },
    watch: {
        namespace: {
            handler(namespace) {
                if (namespace.id !== undefined){
                    this.get_notes({
                        namespaceId: this.namespace.id
                    })
                    this.get_categories({
                        namespaceId: this.namespace.id
                    })
                }
            },
            immediate: true
        },
        categories: {
            handler() {
               if (this.needUpdate) {
                   this.get_categories({
                       namespaceId: this.namespace.id
                   })
                   this.needUpdate = false
               }
            },
            immediate: true
        },
        notes: {
            handler() {
                if (this.needUpdate) {
                    this.get_categories({
                        namespaceId: this.namespace.id
                    })
                    this.needUpdate = false
                }
            },
            immediate: true
        },
    },
}
</script>

<style scoped>

</style>