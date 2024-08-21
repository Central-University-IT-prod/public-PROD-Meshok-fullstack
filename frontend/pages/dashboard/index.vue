<script lang="ts" setup>
import { boolean, object, string, type InferType } from "yup";
import type { User } from "~/types/user";
import type { Question } from "~/types/question";

definePageMeta({
    title: "Личный кабинет",
});

const userInfo = useState<User>("g_user_info");

const questionTypes = [
    { value: "Smile", label: "Смайлики" },
    { value: "Range", label: "Ползунок" },
];

const { data: questions, refresh } = await useAsyncData<Question[]>(
    async () => {
        if (userInfo.value) {
            const retval = await useAPI(`forms`);
            return retval;
        }
    }
);

const categories = computed(() => {
    if (!questions.value) return [];
    const retval = new Set();
    questions.value.forEach((question: Question) =>
        retval.add(question.category)
    );
    return Array.from(retval);
});

const addStateSchema = object({
    type: string().required("Обязательное поле"),
    description: string().required("Обязательное поле"),
    category: string().required("Обязательное поле"),
    enabled: boolean(),
});

const initialAddState = {
    type: questionTypes[0].value as "Range" | "Smile",
    description: "",
    category: "",
};

const addState = reactive<Partial<Question>>({ ...initialAddState });

const addQuestion = async () => {
    try {
        if (addState.category && (addState.category as any).label)
            addState.category = (addState.category as any).label;
        await useAPI("forms/add", {
            method: "POST",
            body: addState,
        });
        refresh();
        const keys = Object.keys(
            initialAddState
        ) as (keyof typeof initialAddState)[];
        keys.forEach((key) => {
            console.log("Reset", key);
            addState[key] = initialAddState[key] as any;
        });
    } catch (error) {}
};

const removeState = reactive<{
    enabled: boolean;
    id: number;
}>({
    enabled: false,
    id: 0,
});

const removeQuestion = async () => {
    try {
        await useAPI(`forms/${removeState.id}/remove`, {
            method: "DELETE",
        });
        refresh();
        removeState.enabled = false;
    } catch (error) {}
};

watch(userInfo, (newUserInfo) => {
    if (newUserInfo) refresh();
});
</script>

<template>
    <div class="flex flex-col gap-5">
        <UModal v-model="removeState.enabled">
            <UCard>
                <h3>Вы уверенны что хотите удалить вопрос?</h3>
                <div class="flex mt-4 gap-2">
                    <UButton
                        label="Удалить"
                        variant="soft"
                        color="rose"
                        @click="removeQuestion"
                    />
                    <UButton
                        label="Отмена"
                        color="white"
                        @click="removeState.enabled = false"
                    />
                </div>
            </UCard>
        </UModal>
        <!-- Actual page -->
        <h2 class="text-2xl font-semibold">Вопросы для фидбека</h2>
        <UAlert
            color="yellow"
            variant="subtle"
            icon="ic:round-live-help"
            title="Как писать вопросы?"
            ><template #description>
                <ol class="list-decimal">
                    <li>
                        Ответом на вопрос должна быть оценка вашей
                        услуги/продукта в диапазоне от 'плохо' до 'хорошо'.
                    </li>
                    <li>
                        Напишите как можно больше вопросов, а мы покажем
                        пользователю 3 из них с наименьшим количеством ответов.
                    </li>
                    <li>
                        Чем короче и проще сформулирован вопрос, тем быстрее
                        пользователь ответит на него.
                    </li>
                </ol>
            </template></UAlert
        >
        <UForm :state="addState" :schema="addStateSchema">
            <div class="flex flex-col gap-4">
                <UFormGroup label="Вопрос" required>
                    <UInput v-model="addState.description" />
                </UFormGroup>
                <UFormGroup label="Тип ответа" required>
                    <USelectMenu
                        v-model="addState.type"
                        value-attribute="value"
                        :options="questionTypes"
                    >
                        <template #label>
                            {{
                                questionTypes.filter(
                                    (option: any) =>
                                        addState.type === option.value
                                )[0].label
                            }}
                        </template>
                    </USelectMenu>
                </UFormGroup>
                <UFormGroup label="Категория" required>
                    <USelectMenu
                        v-model="addState.category"
                        :options="categories"
                        searchable
                        searchable-placeholder="Поиск..."
                        creatable
                    >
                        <template #option-create="{ option }">
                            <span class="flex-shrink-0">Новая категория:</span>
                            <span class="block truncate">{{
                                option.label
                            }}</span>
                        </template>
                    </USelectMenu>
                </UFormGroup>
                <UButton
                    type="submit"
                    variant="soft"
                    label="Создать"
                    :disabled="
                        addState.category === '' || addState.description === ''
                    "
                    class="w-fit"
                    @click="addQuestion"
                />
            </div>
        </UForm>
        <hr class="my-4" />
        <UCard v-for="category in categories">
            <h3 class="text-xl font-semibold text-primary-400 mb-4">
                {{ category }}
                <span class="ml-4 opacity-5 select-none">Категория</span>
            </h3>
            <div class="flex flex-col gap-4" v-if="questions">
                <UAlert
                    v-for="(question, index) in questions.filter(
						(question: Question) => question.category === category
					)"
                    :key="question.id"
                    :title="question.description"
                >
                    <template #description>
                        <div class="flex items-center gap-2">
                            <SmileyRating v-if="question.type === 'Smile'" />
                            <SliderRating
                                v-else-if="question.type === 'Range'"
                            />
                            <UButton
                                icon="mdi:close"
                                variant="soft"
                                color="rose"
                                class="h-fit ml-auto"
                                @click="
                                    removeState.enabled = true;
                                    removeState.id = question.id;
                                "
                            />
                        </div>
                    </template>
                </UAlert>
            </div>
        </UCard>
    </div>
</template>

<style lang="scss" scoped></style>
