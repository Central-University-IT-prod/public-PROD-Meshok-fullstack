<script lang="ts" setup>
import { boolean, number, object, string, type InferType } from "yup";
import type { FormSubmitEvent } from "#ui/types";

const access_cookie = useCookie("user_access_token");
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
    age: "",
    gender: true,
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
        const { token } = await useAPI(
            "users/login",
            {
                method: "POST",
                body: event.data,
            },
            true
        );
        access_cookie.value = token;
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
    age: number()
        .required("Обязательное поле")
        .min(0, "Невалидный возраст")
        .transform((val, orig) => (orig == "" ? undefined : val))
        .typeError("Возраст должнен быть числом"),
    gender: boolean().required("Обязательное поле"),
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
        } = await useAPI(
            "users/register",
            {
                method: "POST",
                body: {
                    ...event.data,
                    gender: event.data.gender ? "Male" : "Female",
                },
            },
            true
        );
        access_cookie.value = token;
    } catch (error) {
        toast.add({
            color: "red",
            title: "Ошибка авторизации",
            description: error as string,
        });
    }
    pending_state.signing_in = false;
};

const { data: userInfo, refresh } = await useAsyncData(async () => {
    const retval = useAPI("users/me", {}, true);
    return retval;
});

watch(access_cookie, () => refresh());
</script>

<template>
    <UCard class="w-full">
        <h2 class="text-3xl font-semibold">1. Авторизуйтесь</h2>
        <div class="flex flex-col" v-if="userInfo">
            <h2 class="text-xl font-semibold flex items-center gap-2">
                <UIcon
                    name="line-md:circle-to-confirm-circle-twotone-transition"
                />
                <i>{{ userInfo.email }}</i>
            </h2>
        </div>
        <div class="flex flex-col items-center p-8" v-else>
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
                        <UFormGroup
                            required
                            class="w-full"
                            label="Возраст"
                            name="age"
                            pattern="\d*"
                        >
                            <UInput v-model="signup_state.age" />
                        </UFormGroup>
                        <UFormGroup
                            required
                            class="w-full"
                            label="Пол"
                            name="gender"
                        >
                            <div class="flex items-center gap-4">
                                <UBadge
                                    label="Женский"
                                    color="pink"
                                    variant="subtle"
                                />
                                <UToggle
                                    v-model="signup_state.gender"
                                    :color="
                                        signup_state.gender ? 'cyan' : 'pink'
                                    "
                                    :ui="{
                                        inactive:
                                            'bg-{color}-500 dark:bg-{color}-400',
                                    }"
                                />
                                <UBadge
                                    label="Мужской"
                                    color="cyan"
                                    variant="subtle"
                                />
                            </div>
                        </UFormGroup>
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
        </div>
    </UCard>
</template>
