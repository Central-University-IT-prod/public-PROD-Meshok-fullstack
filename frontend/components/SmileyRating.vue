<script lang="ts" setup>
const model = defineModel();
const options = [
    {
        name: "fluent-emoji:angry-face",
        value: -1,
    },
    {
        name: "fluent-emoji:neutral-face",
        value: 0,
    },
    {
        name: "fluent-emoji:beaming-face-with-smiling-eyes",
        value: 1,
    },
];
</script>

<template>
    <div class="flex gap-4">
        <UIcon
            v-for="option in options"
            :name="option.name"
            class="w-16 h-16 cursor-pointer option"
            :class="{ selected: option.value === model }"
            @click="model = option.value"
        />
    </div>
</template>

<style lang="scss" scoped>
.option {
    transition: all 0.3s ease-in-out;
    scale: 0.9;
    &.selected {
        scale: 1;
        filter: drop-shadow(0 0 1rem oRange);
    }
}
</style>
