// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	devtools: { enabled: true },
	modules: ['@nuxt/ui', '@nuxtjs/mdc'],
	ssr: false,
	css: [
		"assets/style.scss",
	],
	app: {
		pageTransition: {
			name: "page",
			mode: "out-in"
		}
	},
	routeRules: {
		"/": {
			redirect: "/dashboard"
		}
	},
})
