<template>
    <div class="d-flex justify-content-between p-2">
        <div>
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пространства страниц
            </button>
            <ul class="dropdown-menu dropdown-menu-dark">
                <li v-for="namespace in namespaces" :key="namespace.id">
                    <router-link to="/notes" @click="getNamespaceNotes(namespace.id)">
                        {{ namespace.name }}
                    </router-link>
                </li>
            </ul>
        </div>
        <div>
            <MyButton class="blue-buttons" @click="exit">
                Выйти
            </MyButton>
        </div>
    </div>
  <div class="d-flex flex-column justify-content-center align-items-center p-5">
      <div style="width: 80%">
          <input class="form-control" id="inputLogin"
                 placeholder="Введите логин"
                 v-model="note.title"
          >
          <textarea type="text" class="form-control" id="inputPassword"
                    placeholder="Введите пароль"
                    v-model="note.text"
          >

          </textarea>

          <div>
              <div class="d-flex">
                  <div v-for="category in note_categories" :key="category.id" class=" m-2 border p-2">
                      <div class="d-flex">
                          <p> {{  category.name }}</p>
                          <p class="close-button" style="margin-right: 10px; font-size: 24px;"
                             @click="deleteNoteCategory(category)">
                              &times;
                          </p>
                      </div>
                  </div>
                  <div>
                      <MyButton class="blue-buttons" @click="showAllCategories">
                          Добавить категорию
                      </MyButton>
                  </div>
              </div>
          </div>

          <div class="d-flex">
              <div>
                  <MyButton class="blue-buttons" @click="save">
                      Сохранить
                  </MyButton>
              </div>
          </div>
      </div>
  </div>

    <MyModal v-model:show="modalVisible" v-model:buttons="modalButtons"
             @update="closeModal"
    >
        <div>
            <div>Список доступных категорий:</div>
            <div class="d-flex">
                <div v-for="category in categories" :key="category.id" class=" m-2 border p-2"
                     @click="addNoteCategory(category)">
                    {{  category.name }}
                </div>
            </div>
            <MyButton class="blue-buttons" @click="this.$router.push('/categories')">
                Создать новую категорию
            </MyButton>
        </div>
    </MyModal>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
    name: "EditNotePage",
    data() {
        return {
            username: '',
            password: '',
            modalVisible: false,
            modalButtons: [],
            modalMessage: '',
        }
    },
    computed: {
        ...mapGetters(['note', 'note_categories', 'namespaces', 'categories']),
    },
    methods: {
        ...mapActions(['get_categories', 'push_note', 'push_note_categories']),
        exit() {
            this.$router.push('/')
        },
        showAllCategories() {
            this.get_categories()
            this.modalVisible = true
            this.modalButtons = [
                {value: "Закрыть", status: true}
            ]
        },
        addNoteCategory(category) {
            let haveThisCategory = 0
            this.note_categories.forEach( el => {
                if (el.id === category.id) {
                    haveThisCategory++
                }
            })

            if (haveThisCategory === 0) {
                this.note_categories.push(category)
            }

            haveThisCategory = 0
        },
        deleteNoteCategory(category) {
            this.note_categories.splice(this.note_categories.indexOf(category))

            console.log('local b ytn')
            console.log(this.note_categories)
        },
        closeModal() {
            this.modalVisible = false
        },
        getNamespaceNotes(namespaceId) {
            this.get_notes(namespaceId)
            this.$router.push('/notes')
        },
        save() {
            this.push_note()
            this.push_note_categories()
            this.$router.push('/note')

        }
    },
    mounted() {
    }
}
</script>

<style scoped>

</style>