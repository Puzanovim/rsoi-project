<template>
    <span>
        <select v-model="selectedOptions">
            <option v-for="item in list" :key="item.id">
                {{item.value}}
            </option>
        </select>
    </span>
</template>

<script>
    import { ref } from 'vue'
    import {mapGetters} from "vuex";
    export default {
        name: "MySelect",
        computed: {
            ...mapGetters(['mainJSON']),
        },
        props: {
            list: {},
            listID: {},
            selected: {}
        },
        setup(props) {
            let selectedOptions = ref(props.selected)
            if(props.selected === "NA"){
                selectedOptions = ref('Выбери ответ:')
            }
            return {
                selectedOptions,
            }
        },
        watch: {
            selectedOptions(el){
                this.$emit('answer', el, this.listID)
            }
        }
    }
</script>

<style scoped>

</style>