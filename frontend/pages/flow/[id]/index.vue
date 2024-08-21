<script lang="ts" setup>
import type { Question } from "~/types/question";

definePageMeta({
    title: "Фидбек",
    layout: "empty",
    middleware: [
        async (to, from) => {
            try {
                await useAPI(`forms/${to.params.id}`, {}, true);
            } catch (error: any) {
                return abortNavigation({
                    statusCode: error.statusCode,
                    message:
                        error.statusCode === 422
                            ? "Организация не существует"
                            : error.message,
                });
            }
        },
    ],
});
const {
    params: { id: flow_id },
} = useRoute();

const root = document.querySelector(":root");
if (root) root.classList.remove("dark");

const { data: info } = await useAsyncData(async () => {
    const retval = await useAPI(`forms/${flow_id}`, {}, true);
    return retval;
});

const state = reactive({});

const notFilled = computed(() => {
    let retval = false;
    info.value.questions.forEach((question: Question) => {
        if (state[question.id] === undefined) retval = true;
    });
    return retval;
});

const submitFeedback = async () => {
    const body: {
        question_id: number;
        answer: number;
    }[] = [];
    const ids = Object.keys(state);
    ids.forEach((key) => {
        body.push({
            question_id: parseInt(key),
            answer: state[key] as number,
        });
    });
    //
    try {
        await useAPI(
            "forms",
            {
                method: "POST",
                body: body,
            },
            true
        );
        done.value = true;
    } catch (error) {
        toast.add({
            color: "red",
            title: "Ошибка",
            description: error as string,
        });
    }
};
const done = ref(false);
</script>

<template>
    <div class="__flow flex flex-col gap-8 p-4 sm:p-8 items-center">
        <h1 class="text-4xl font-extralight mt-8">Feedbacker</h1>
        <FlowAuth />
        <hr />
        <UCard class="w-full">
            <h2 class="text-3xl font-semibold mb-4">
                2. Оставьте фидбек на {{ info.org_name }}
            </h2>
            <div class="flex flex-col gap-4" v-if="!done">
                <UCard
                    v-for="(question, index) in info.questions"
                    :key="question.id"
                >
                    <p>{{ question.description }}</p>
                    <div class="flex items-center gap-2">
                        <SmileyRating
                            v-if="question.type === 'Smile'"
                            v-model="state[question.id]"
                        />
                        <SliderRating
                            v-else-if="question.type === 'Range'"
                            v-model="state[question.id]"
                        />
                    </div>
                </UCard>
                <UButton
                    label="Оставить фидбек!"
                    variant="soft"
                    size="xl"
                    :disabled="notFilled"
                    @click="submitFeedback"
                />
            </div>
            <div class="flex flex-col items-center gap-4" v-else>
                <hr />
                <h2 class="text-3xl font-semibold">Готово!</h2>
            </div>
        </UCard>
        <UCard v-if="done" class="w-full">
            <h2 class="text-3xl font-semibold mb-4 flex items-center gap-4">
                <p>
                    3. Скачай приложение для
                    <UIcon name="mingcute:android-2-fill" />
                </p>
                <UButton
                    target="_blank"
                    label="Скачать"
                    to="https://disk.yandex.ru/d/tFDHG8Nil_PLrQ"
                />
            </h2>
        </UCard>
    </div>
</template>

<style lang="scss" scoped></style>
