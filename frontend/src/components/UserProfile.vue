<template>
    <NamespacesNavBar/>
    <div class="d-flex justify-content-center align-items-center">
      <div class="d-flex">
          <div class="border-right">
              <div class="d-flex flex-column align-items-center text-center p-3 py-5">
                  <img class="rounded-circle mt-5" style="width: 150px"
                       src="../assets/default_user_profile_photo.jpg" alt="Фото">
                  <span class="font-weight-bold">{{ user_me.username }}</span>
                  <span class="text-black-50">{{ user_me.email }}</span>
              </div>
          </div>
          <div class="row g-3" style="max-width: 80%">
              <div class="p-3 py-5">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                      <h4 class="text-right">Настройки профиля</h4>
                  </div>
                  <div class="d-flex">
                      <div class="col-md-6 me-2">
                          <label class="form-label">Имя</label>
                          <input type="text" class="form-control" placeholder="Имя" v-model="user_me.first_name">
                      </div>
                      <div class="col-md-6">
                          <label class="form-label">Фамилия</label>
                          <input type="text" class="form-control" placeholder="Фамилия" v-model="user_me.second_name">
                      </div>
                  </div>
                  <div>
                      <div>
                          <label class="form-label">Логин</label>
                          <input type="text" class="form-control" placeholder="Логин" v-model="user_me.username">
                      </div>
                      <div>
                          <label class="form-label">Почта</label>
                          <input type="text" class="form-control" placeholder="Почта" v-model="user_me.email">
                      </div>
                  </div>
<!--                  <div class="mt-5 text-center">
                      <MyButton style="width: 250px" class="blue-buttons" @click="saveProfile">
                          Сохранить изменения
                      </MyButton>
                  </div>-->
              </div>
          </div>
      </div>
    </div>

    <div v-if="this.user_me.is_superuser">
        <div>
            Статистика:
        </div>
        <table class="table">
            <thead>
            <tr>
                <th scope="col">Название сервиса</th>
                <th scope="col">Описание</th>
                <th scope="col">Время создания</th>
                <th scope="col">ID</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="statistic in statistics" :key="statistic.id">
                <td>{{ statistic.service }}</td>
                <td>{{ statistic.description }}</td>
                <td>{{ statistic.created_time }}</td>
                <td>{{ statistic.id }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";
import NamespacesNavBar from "@/components/NamespacesNavBar.vue";

export default {
    name: "UserProfile",
    components: {NamespacesNavBar},
    data() {
        return {
        }
    },
    computed: {
        ...mapGetters(['token', 'user_me', 'namespaces', 'statistics']),
    },
    methods: {
        ...mapActions(['get_users_me', 'get_namespaces', 'get_notes']),
        ...mapMutations(['put_user']),
        saveProfile() {
            this.put_user({
                first_name: this.user_me.first_name,
                second_name: this.user_me.second_name,
                username: this.user_me.username,
                email: this.user_me.email,
                is_superuser: this.user_me.is_superuser,
                id: this.user_me.id
            })
        },
        exit() {
            this.$router.push('/')
        },
    },
    created() {
        this.get_users_me()
        console.log(this.user_me)
    }
}
</script>

<style scoped>

</style>