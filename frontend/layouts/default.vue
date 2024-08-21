<script lang="ts" setup>
import type { User } from "~/types/user";
const userInfo = useState<User>("g_user_info");

onBeforeMount(async () => {
    const user = (await useAPI("orgs/me")) as User;
    userInfo.value = user;
});
</script>

<template>
    <div class="__layout-default">
        <DashboardHeader />
        <OrganizationInfo>
            <slot />
        </OrganizationInfo>
    </div>
</template>

<style lang="scss" scoped></style>
