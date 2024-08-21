<script lang="ts" setup>
import type { User } from "~/types/user";

const userInfo = useState<User>("g_user_info");
const SITE_URL = "https://feedbacker.online";

const AIHintState = reactive({
    enabled: false,
    response: undefined,
    lines: [],
});

const generateLines = () => {
    AIHintState.lines = [];
    for (let i = 0; i < 18; i++) {
        setTimeout(() => {
            AIHintState.lines[i] = 0;
            setTimeout(() => {
                AIHintState.lines[i] = Math.random() * 50 + 50;
            }, 100);
        }, i * 500);
    }
};

const getAIHint = async () => {
    AIHintState.enabled = true;
    AIHintState.response = undefined;
    generateLines();
    const { text } = await useAPI("orgs/hints");
    AIHintState.response = text;
};
</script>

<template>
    <div class="__info p-4 sm:px-8">
        <UModal
            v-model="AIHintState.enabled"
            :prevent-close="!AIHintState.response"
        >
            <UCard :ui="{ background: 'bg-white dark:bg-black' }">
                <template #header>
                    <div class="flex">
                        <UButton
                            class="ml-auto"
                            color="white"
                            variant="link"
                            icon="mdi:close"
                            :disabled="!AIHintState.response"
                            @click="AIHintState.enabled = false"
                        />
                    </div>
                </template>
                <div class="flex flex-col gap-4"></div>
                <img
                    src="/YandexGPT2.jpg"
                    alt="Yandex GPT"
                    class="dark:invert contrast-200 rounded-3xl w-full h-32 object-cover"
                />
                <MarkdownFormatter v-if="AIHintState.response">
                    <MDC :value="AIHintState.response" />
                </MarkdownFormatter>
                <div class="flex gap-2 flex-col my-3" v-else>
                    <USkeleton
                        v-for="line in AIHintState.lines"
                        class="w-full h-4 transition-all"
                        :style="{ width: `${line}%` }"
                    />
                </div>
                <UButton
                    color="white"
                    icon="svg-spinners:pulse-rings-2"
                    label="По новой"
                    @click="getAIHint"
                    :disabled="!AIHintState.response"
                />
            </UCard>
        </UModal>
        <div
            class="info-banner flex items-center gap-4 justify-between h-64"
            v-if="userInfo"
        >
            <div class="flex flex-col gap-2">
                <h1 class="text-3xl font-bold">{{ userInfo.name }}</h1>

                <UButton
                    @click="getAIHint"
                    variant="soft"
                    class="animate-pulse w-fit"
                >
                    <UBadge size="lg" variant="subtle" class="flex gap-2"
                        ><UIcon name="fluent:brain-circuit-20-regular" />AI
                        рекомендации на основе аналитики</UBadge
                    >
                </UButton>
            </div>
            <QRCode :value="`${SITE_URL}/flow/${userInfo.id}`" />
        </div>
        <div v-else class="flex justify-between items-center h-64">
            <USkeleton class="h-10 w-96" />
            <USkeleton class="h-56 w-56 rounded-xl" />
        </div>
        <hr class="my-4" />
        <slot />
    </div>
</template>

<style lang="scss" scoped></style>
