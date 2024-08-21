<script lang="ts" setup>
import { useWindowSize } from "@vueuse/core";
const { width } = useWindowSize();
const access_cookie = useCookie("access_token");

const links = [
    {
        label: "Главная",
        to: "/dashboard",
    },
    {
        label: "Ответы",
        to: "/dashboard/responses",
    },
    {
        label: "Аналитика",
        to: "/dashboard/analytics",
    },
];

const root = ref();

const calculateHeight = () => {
    if (width.value) {
        const layout = document.querySelector(
            ".__layout-default"
        ) as HTMLDivElement;
        if (layout && root.value) {
            layout.style.paddingTop = `${root.value.offsetHeight}px`;
        }
    }
};

watchEffect(calculateHeight);
onMounted(calculateHeight);

const router = useRouter();
</script>

<template>
    <div
        class="header flex justify-between items-center p-4 sm:p-6 gap-4 fixed w-full top-0 z-10 backdrop-blur-lg backdrop-brightness-95"
        ref="root"
    >
        <ULink to="/" class="logo select-none">
            <h1 class="text-3xl font-extralight">Feedbacker</h1>
        </ULink>
        <div class="links flex gap-x-4 flex-wrap justify-center">
            <ULink
                v-for="link in links"
                :text="link.label"
                :to="link.to"
                active-class="text-primary"
                inactive-class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
            />
        </div>
        <div
            class="flex gap items-center flex-wrap gap-x-4 justify-center gap-y-2"
        >
            <ColorModeSwitch />
            <UButton
                label="Выйти"
                variant="soft"
                @click="
                    access_cookie = undefined;
                    router.push('/auth');
                "
            />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.header {
    border-bottom: 1px solid rgba(var(--inverted-rgb), 0.1);
}
</style>
