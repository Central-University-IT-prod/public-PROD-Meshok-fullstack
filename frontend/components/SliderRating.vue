<script lang="ts" setup>
const model = defineModel<number>();
if (!model.value) model.value = 5;
const RangeColor = computed(() => {
    if (model.value >= 8) return "primary";
    else if (model.value >= 4) return "yellow";
    else return "rose";
});
</script>

<template>
    <div class="flex gap-2 items-center w-fit min-w-0">
        <UBadge label="Очень плохо" color="rose" variant="subtle" />
        <URange
            v-model="model"
            :color="RangeColor"
            class="min-w-54 w-96"
            :min="1"
            :max="10"
        />
        <UBadge label="Очень хорошо" variant="subtle" />
    </div>
</template>
