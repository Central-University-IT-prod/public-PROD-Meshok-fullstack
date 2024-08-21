<script lang="ts" setup>
import type { User } from "~/types/user";
import type { Response } from "~/types/response";
definePageMeta({
    title: "Ответы",
});

const userInfo = useState<User>("g_user_info");
const { data: responses } = await useAsyncData<Response[]>(async () => {
    const retval = useAPI(`orgs/answers`);
    return retval;
});

const questions = computed(() => {
    if (!responses.value) return [];
    const validate = new Set();
    const retval: any[] = [];
    responses.value.forEach((response: Response) => {
        if (!validate.has(response.question.description)) {
            validate.add(response.question.description);
            retval.push(response.question);
        }
    });
    return retval.map((question: any) => {
        return {
            label: question.description,
            ...question,
        };
    });
});

const columns = [
    {
        key: "user.email",
        label: "Почта",
    },
    {
        key: "user.age",
        label: "Возраст",
    },
    {
        key: "user.gender",
        label: "Пол",
    },
    {
        key: "user.points.current_level",
        label: "Ранг",
    },
    {
        key: "user.points.current_xp",
        label: "Опыт",
    },
    {
        key: "answer",
        label: "Ответ",
    },
];

const smileys = {
    "-1": "😠",
    "0": "😐",
    "1": "😁",
};
</script>

<template>
    <div class="__responses">
        <UAccordion :items="questions" v-if="responses && responses.length > 0">
            <template #item="{ item, index, open }">
                <div class="flex flex-col gap-4">
                    <UTable
                        :rows="
                            responses.filter(
                                (response) =>
                                    item.label === response.question.description
                            )
                        "
                        :columns="columns"
                    >
                        <template #user.gender-data="{ row }">
                            {{
                                row.user.gender === "Male"
                                    ? "Мужской"
                                    : "Женский"
                            }}
                        </template>
                        <template #answer-data="{ row }">
                            {{
                                item.type === "Smile"
                                    ? smileys[row.answer]
                                    : row.answer
                            }}
                        </template>
                    </UTable>
                </div>
            </template>
        </UAccordion>
        <div class="flex justify-center p-4 items-center text-2xl gap-2" v-else>
            <UIcon name="heroicons:server-stack-20-solid" />
            <p>Пока нет данных...</p>
        </div>
    </div>
</template>
