<template>
    <NamespacesNavBar/>
    <div class="m-3">
        <input class="form-control" id="inputLogin"
               placeholder="Введите название заметки"
               v-model="noteTitle"
        >
        <textarea type="text" class="form-control mt-3" id="inputPassword"
                  placeholder="Введите текст заметки"
                  v-model="noteText"
        >

            </textarea>
        <div class="card m-4" v-for="category in noteCategories" :key="category.id">
            <div class="card-body d-flex align-items-center px-4">
                <p>{{category.name}}</p>
                <p class="close-button" style="margin-right: 10px; font-size: 24px;"
                   @click="deleteNoteCategory(category)">
                    &times;
                </p>
            </div>
        </div>
        <div>
            <MyButton class="blue-buttons mt-3" @click="showAllCategories">
                Добавить категорию
            </MyButton>
        </div>
        <div class="d-flex mt-3">
            <div>
                <MyButton class="blue-buttons" @click="createNote">
                    Сохранить
                </MyButton>
            </div>
            <div>
                <MyButton class="blue-buttons mx-3" @click="this.$router.push('/notes')">
                    На страницу заметок
                </MyButton>
            </div>
        </div>
    </div>


    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="closeModal"
    >
        <div>
            <div>Список доступных категорий:</div>
            <div v-if="categories.items !== undefined" class="d-flex m-2">
                <div class="card mx-2" v-for="category in categories.items" :key="category.id">
                    <div class="card-body" @click="addNoteCategory(category)">
                        <p>{{category.name}}</p>
                    </div>
                </div>
            </div>
        </div>
    </MyModal>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";
import NamespacesNavBar from "@/components/NamespacesNavBar.vue";

export default {
    name: "CreateNotePage",
    components: {NamespacesNavBar},
    data() {
        return {
            noteTitle: '',
            noteText: '',
            noteCategories: [],
            modalVisible: false,
            modalButtons: [],
            modalMessage: '',
            needUpdate: false
        }
    },
    computed: {
        ...mapGetters(['notes', 'namespace', 'categories']),
    },
    methods: {
        ...mapActions(['get_notes', 'get_categories']),
        ...mapMutations(['create_note']),
        createNote(){
            let noteCategories = []
            this.noteCategories.forEach( el => {
                noteCategories.push(el.id)
            })
            this.create_note({
                noteTitle: this.noteTitle,
                noteText: this.noteText,
                namespacesId: this.namespace.id,
                noteCategories: noteCategories
            })
            this.needUpdate = true
            this.get_notes({
                namespaceId: this.namespace.id
            })
        },
        showAllCategories() {
            this.get_categories({
                namespaceId: this.namespace.id
            })

            this.modalVisible = true
            this.modalButtons = [
                {value: "Создать новую категорию", status: 'toCategories'},
                {value: "Сохранить", status: true},
                {value: "Закрыть", status: false}
            ]
        },
        addNoteCategory(category) {
            if (this.noteCategories.indexOf(category) === -1){
                this.noteCategories.push(category)
            }
        },
        deleteNoteCategory(category) {
            this.noteCategories.splice(this.noteCategories.indexOf(category))
        },
        closeModal(status) {
            this.modalVisible = false
            if (status === 'toCategories') {
                this.$router.push('/categories')
            }
        },
    },
    watch: {
        notes: {
            handler() {
                if (this.needUpdate) {
                    this.get_notes({
                        namespaceId: this.namespace.id
                    })
                    this.needUpdate = false
                    this.$router.push('/notes')
                }
            },
            immediate: true
        }
    },
}
</script>

<style scoped>

</style>