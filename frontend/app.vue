<script lang="ts" setup>
const { site_name } = useAppConfig();
watchEffect(() => {
    const {
        meta: { title },
    } = useRoute();
    useHead({
        htmlAttrs: {
            lang: "ru",
        },
        link: [
            {
                rel: "icon",
                type: "image/svg+xml",
                href: "/favicon.svg",
            },
        ],
        title: title as string,
        titleTemplate: (title) =>
            title ? `${title} | ${site_name}` : site_name,
    });
});
const mail = "support@feedbacker.online";
</script>

<template>
    <div class="__app">
        <NuxtLoadingIndicator color="rgb(var(--color-primary-DEFAULT))" />
        <NuxtLayout>
            <NuxtPage />
        </NuxtLayout>
        <footer
            class="p-4 flex gap-4 justify-between fixed bottom-0 bg-white dark:bg-gray-900"
            style="border-top-right-radius: 1rem"
        >
            <a class="text-primary" :href="`mailto:${mail}`">{{ mail }}</a>
        </footer>
        <UNotifications />
    </div>
</template>
