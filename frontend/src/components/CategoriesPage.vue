<template>
    <NamespacesNavBar/>
    <div class="m-3">
        <div v-if="categories.items !== undefined" class="d-flex">
            <div class="card m-4" v-for="category in categories.items" :key="category.id">
                <div class="card-body d-flex align-items-center px-4">
                    <p>{{category.name}}</p>
                    <p class="close-button" style="margin-right: 10px; font-size: 24px;"
                       @click="deleteNoteCategory(category)">
                        &times;
                    </p>
                </div>
            </div>
        </div>
        <div>
            <MyButton class="blue-buttons" @click="addCategory">
                Создать категорию
            </MyButton>
        </div>
        <div class="mt-3">
            <MyButton class="blue-buttons" @click="this.$router.push('/notes')">
                На страницу заметок
            </MyButton>
        </div>
    </div>
    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="closeModal"
    >
        <input class="form-control" id="inputLogin"
               placeholder="Введите название категории"
               v-model="categoryName"
        >
    </MyModal>

</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";
import NamespacesNavBar from "@/components/NamespacesNavBar.vue";

export default {
    name: "CategoriesPage",
    components: {NamespacesNavBar},
    data() {
        return {
            modalVisible: false,
            modalButtons: [],
            modalMessage: '',
            categoryName: '',
            needUpdate: false
        }
    },
    computed: {
        ...mapGetters(['categories', 'namespace']),
    },
    methods: {
        ...mapActions(['get_notes', 'get_categories']),
        ...mapMutations(['post_category', 'delete_category']),
        exit() {
            this.$router.push('/')
        },
        deleteNoteCategory(category){
            this.delete_category({
                categoryId: category.id
            })
            this.get_categories({
                namespaceId: this.namespace.id
            })
            this.needUpdate = true
        },
        addCategory() {
            this.modalVisible = true
            this.modalButtons = [
                {value: "Сохранить", status: true},
                {value: "Отмена", status: false}
            ]
            this.needUpdate = true
        },
        closeModal(status) {
            this.modalVisible = false
            if (status === true) {
                this.post_category({
                    namespaceId: this.namespace.id,
                    categoryName: this.categoryName
                })
                this.get_categories({
                    namespaceId: this.namespace.id
                })
                this.categoryName = ''
            }
        }
    },
    watch: {
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
        }
    },
}
</script>

<style scoped>

</style>