<template>
    <NamespacesNavBar/>
    <div class="d-flex flex-column justify-content-center align-items-center">
        <div class="card" style="width: 80%; margin: 50px">
            <div class="card-body m-2">
                <div class="d-flex justify-content-between">
                    <h1>{{note.title}}</h1>
<!--                    <div>
                        <MyButton class="blue-buttons" @click="editNote">
                            Редактировать
                        </MyButton>
                    </div>-->
                </div>
                <p> {{ note.text }}</p>
                <div class="d-flex">
                    <div v-for="category in note.categories" :key="category.id" class=" m-2 border p-2">
                        {{  category.name }}
                    </div>
                </div>
            </div>
        </div>
        <div class="d-flex">
            <div>
                <MyButton style="background: red; border: red"  @click="deleteNote">
                    Удалить заметку
                </MyButton>
            </div>
            <div>
                <MyButton class="blue-buttons" @click="this.$router.push('/notes')">
                    На страницу заметок
                </MyButton>
            </div>
        </div>
    </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";
import NamespacesNavBar from "@/components/NamespacesNavBar.vue";

export default {
    name: "NotePage",
    components: {NamespacesNavBar},
    data(){
        return {
            needUpdate: false
        }
    },
    computed: {
        ...mapGetters(['note', 'notes', 'namespaces', 'namespace']),
    },
    methods:{
        ...mapActions(['get_note', 'get_namespaces', 'get_notes', 'get_note_categories']),
        ...mapMutations(['delete_note']),
        exit() {
            this.$router.push('/')
        },
        editNote() {
            this.$router.push('/edit-note')
        },
        getNamespaceNotes(namespaceId) {
            this.get_notes({
                namespaceId: namespaceId
            })
            this.$router.push('/notes')
        },
        deleteNote() {
            this.delete_note({
                noteId: this.note.id
            })
            this.needUpdate = true
            this.get_notes({
                namespaceId: this.namespace.id
            })
        }
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