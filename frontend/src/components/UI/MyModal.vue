<template>
    <div v-if="show" class="dialog">
        <div class="dialog-content">
            <div class="mb-3">
                <slot></slot>  <!-- todo именовать слоты -->
            </div>
            <div class="d-flex justify-content-center">
                <MyButton v-for="button in buttons" :key="button.value"  @click="$emit('update', button.status)"
                          class="me-3 blue-buttons"
                >
                    {{button.value}}
                </MyButton>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "MyModal",
        props: {
            show: {
                type: Boolean
            },
            buttons: {},
            answer: {}
        },
        methods: {
            checkAnswer(status){
                this.$emit('update:answer', status)
            }
        }
    }
</script>

<style scoped>
    .dialog {
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
        background: rgba(0, 0, 0, 0.5);
        position: fixed;
        display: flex;
        z-index: 99999;
    }
    .dialog-content {
        margin: auto;
        background: white;
        border-radius: 12px;
        min-height: 100px;
        min-width: 300px;
        max-width: 600px;
        padding: 20px;
    }
</style>