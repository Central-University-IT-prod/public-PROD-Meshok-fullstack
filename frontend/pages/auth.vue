<script lang="ts" setup>
import { object, string, type InferType } from "yup";
import type { FormSubmitEvent } from "#ui/types";

definePageMeta({
    title: "Авторизация",
    layout: "empty",
});
const access_cookie = useCookie("access_token");
const toast = useToast();

const tabs = [
    {
        key: "signup",
        label: "Регистрация",
    },
    {
        key: "login",
        label: "Войти",
    },
];

const route = useRoute();
const router = useRouter();

const signup_state = reactive({
    name: "",
    email: "",
    password: "",
});

const login_state = reactive({ email: "", password: "" });

const pending_state = reactive({
    loging_in: false,
    signing_in: false,
});

const login_schema = object({
    email: string()
        .email("Недействительная почта")
        .required("Обязательное поле")
        .min(5, "Почта должна быть длиннее 5 символов")
        .max(150, "Почта должна быть короче 150 символов"),
    password: string()
        .required("Обязательное поле")
        .min(8, "Пароль должен быть длиннее 8 символов")
        .max(150, "Пароль должен быть короче 150 символов"),
});

type LoginSchema = InferType<typeof login_schema>;

const onSubmitLogin = async (event: FormSubmitEvent<LoginSchema>) => {
    pending_state.loging_in = true;
    try {
        const { token } = await useAPI("orgs/login", {
            method: "POST",
            body: event.data,
        });
        access_cookie.value = token;
        router.push("/");
    } catch (error) {
        toast.add({
            color: "red",
            icon: "fluent:shield-keyhole-24-filled",
            title: "Ошибка авторизации",
            description: error as string,
        });
    }
    pending_state.loging_in = false;
};

const signup_schema = object({
    name: string()
        .required("Обязательное поле")
        .min(3, "Имя должно быть длиннее 3 символов")
        .max(100, "Имя должно быть короче 100 символов"),
    email: string()
        .email("Недействительная почта")
        .required("Обязательное поле")
        .min(5, "Почта должна быть длиннее 5 символов")
        .max(150, "Почта должна быть короче 150 символов"),
    password: string()
        .required("Обязательное поле")
        .min(8, "Пароль должен быть длиннее 8 символов")
        .max(150, "Пароль должен быть короче 150 символов"),
});

type SignupSchema = InferType<typeof signup_schema>;

const onSubmitSignup = async (event: FormSubmitEvent<SignupSchema>) => {
    pending_state.signing_in = true;
    try {
        const {
            auth: { token },
        } = await useAPI("orgs/register", {
            method: "POST",
            body: event.data,
        });
        access_cookie.value = token;
        router.push("/");
    } catch (error) {
        toast.add({
            color: "red",
            title: "Ошибка авторизации",
            description: error as string,
        });
    }
    pending_state.signing_in = false;
};
</script>

<template>
    <main class="__auth flex flex-col items-center p-8 w-full">
        <h1 class="text-4xl font-extralight mt-12 mb-20">Feedbacker</h1>
        <h2 class="text-3xl font-semibold">Авторизация</h2>
        <hr class="max-w-[480px] w-full my-4" />
        <UTabs :items="tabs" class="max-w-[480px] w-full">
            <template #item="{ item }">
                <UForm
                    class="signup flex flex-col items-center p-4 gap-4"
                    :state="signup_state"
                    :schema="signup_schema"
                    @submit="onSubmitSignup"
                    v-if="item.key === 'signup'"
                >
                    <div class="flex w-full gap-4">
                        <UFormGroup
                            required
                            class="w-full"
                            label="Название организации"
                            name="name"
                        >
                            <UInput v-model="signup_state.name" />
                        </UFormGroup>
                    </div>
                    <UFormGroup
                        required
                        class="w-full"
                        label="Почта"
                        name="email"
                    >
                        <UInput v-model="signup_state.email" />
                    </UFormGroup>
                    <UFormGroup
                        required
                        class="w-full"
                        label="Пароль"
                        name="password"
                    >
                        <UInput
                            type="password"
                            v-model="signup_state.password"
                        />
                    </UFormGroup>
                    <UButton
                        :loading="pending_state.signing_in"
                        type="submit"
                        trailing-icon="material-symbols:arrow-right-alt-rounded"
                        label="Зарегистрироваться"
                    />
                </UForm>
                <UForm
                    class="login flex flex-col items-center p-4 gap-4"
                    :state="login_state"
                    :schema="login_schema"
                    @submit="onSubmitLogin"
                    v-else-if="item.key === 'login'"
                >
                    <UFormGroup
                        required
                        class="w-full"
                        label="Почта"
                        name="email"
                    >
                        <UInput v-model="login_state.email" />
                    </UFormGroup>
                    <UFormGroup
                        required
                        class="w-full"
                        label="Пароль"
                        name="password"
                    >
                        <UInput
                            type="password"
                            v-model="login_state.password"
                        />
                    </UFormGroup>
                    <UButton
                        :loading="pending_state.loging_in"
                        type="submit"
                        trailing-icon="material-symbols:arrow-right-alt-rounded"
                        label="Войти"
                    />
                </UForm>
            </template>
        </UTabs>
    </main>
</template>

<style lang="scss" scoped></style>
