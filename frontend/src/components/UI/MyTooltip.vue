<template>
    <div
            id="tooltip"
            :style="{ top: `${clientY}px`, left: `${clientX}px` }"
            v-if="toolTipVisible"
    >
        {{toolTipMessage}}
    </div>
</template>

<script>
    export default {
        name: "MyTooltip",
        props: {
            toolTipVisible: {
                type: Boolean
            },
            clientX: {},
            clientY: {},
            toolTipMessage: {}
        },
    };
</script>

<style scoped>
    #tooltip {
        border: 1px solid black;
        padding: 5px;
        position: absolute;
        background-color: white;
    }
</style>