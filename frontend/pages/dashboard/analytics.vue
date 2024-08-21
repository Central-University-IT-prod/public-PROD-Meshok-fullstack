<script lang="ts" setup>
import { BarChart, DoughnutChart } from "vue-chart-3";
import type { Metric } from "~/types/metric";
definePageMeta({
    title: "Аналитика",
});

const { data: conversion } = await useAsyncData(async () => {
    const retval = await useAPI("orgs/metric");
    return retval;
});

const genDataFormat = (stats: Metric["stats"], type: Metric["type"]) => {
    const pickFrom =
        type === "Smile"
            ? ["#facc15", "#34d399", "#fb7185"]
            : [
                  "#fb7185",
                  "#fb7185",
                  "#fb7185",
                  "#fb7185",
                  "#facc15",
                  "#facc15",
                  "#facc15",
                  "#facc15",
                  "#34d399",
                  "#34d399",
                  "#34d399",
              ];
    const retval = {
        labels:
            type === "Range"
                ? Object.keys(stats).map(
                      (num: string) =>
                          `${num} балл${
                              parseInt(num) > 1
                                  ? parseInt(num) > 4
                                      ? "ов"
                                      : "а"
                                  : ""
                          }`
                  )
                : ["😐", "😁", "😠"],
        datasets: [
            {
                label: `Оценок`,
                data: Object.values(stats),
                backgroundColor: pickFrom,
            },
        ],
    };
    return retval;
};

const { data: analytics, refresh } = await useAsyncData<Metric[]>(async () => {
    const retval = await useAPI("orgs/statistics", {
        query: {
            age: filterState.age ?? undefined,
            gender: filterState.gender ?? undefined,
        },
    });
    return retval;
});

const interval = ref();

onMounted(() => {
    refresh();
    interval.value = setInterval(refresh, 2000);
});

onUnmounted(() => clearInterval(interval.value));

const genderFilter = [
    {
        value: null,
        label: "Любой",
    },
    {
        value: "Male",
        label: "Мужской",
    },
    {
        value: "Female",
        label: "Женский",
    },
];

const ageFilter = [
    {
        value: null,
        label: "Любой",
    },
    {
        value: "child",
        label: "< 18",
    },
    {
        value: "adult",
        label: "18+",
    },
];

const filterState = reactive({
    age: null,
    gender: null,
});

watch(filterState, refresh);
</script>

<template>
    <div class="__analytics">
        <template v-if="conversion.forms_opened">
            <h3 class="text-2xl font-semibold">
                Конверсия (процент пользователей которые проходят опрос до
                конца):
                {{
                    Math.floor(
                        (conversion.forms_confirmed / conversion.forms_opened) *
                            100
                    )
                }}%
            </h3>
            <hr class="my-2" />
        </template>
        <div class="flex gap-4 py-4">
            <URadioGroup :options="genderFilter" v-model="filterState.gender" />
            <URadioGroup :options="ageFilter" v-model="filterState.age" />
        </div>
        <UAccordion
            :items="
                analytics?.map((analytic) => {
                    return {
                        ...analytic,
                        label: analytic.question,
                        defaultOpen: true,
                    };
                })
            "
            v-if="analytics && analytics.length > 0"
        >
            <template #item="{ item, index, open }"
                ><div
                    class="dark:bg-gray-950 rounded-2xl p-4 flex justify-center"
                >
                    <DoughnutChart
                        :options="{}"
                        class="h-64 w-full"
                        v-if="item.type === 'Smile'"
                        :chartData="genDataFormat(item.stats, item.type)"
                        :chartOptions="{
                            plugins: { legend: { display: false } },
                        }"
                    />
                    <BarChart
                        v-else
                        class="h-64 w-full"
                        :options="{}"
                        :chartData="genDataFormat(item.stats, item.type)"
                    />
                </div>
            </template>
        </UAccordion>
        <div class="flex justify-center p-4 items-center text-2xl gap-2" v-else>
            <UIcon name="heroicons:server-stack-20-solid" />
            <p>Пока нет данных...</p>
        </div>
    </div>
</template>
