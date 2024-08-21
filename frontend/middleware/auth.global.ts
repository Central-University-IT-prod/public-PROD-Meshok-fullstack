export default defineNuxtRouteMiddleware(async (to, from) => {
	const authPath = "/auth"
	if (to.path.startsWith(authPath) || to.path.startsWith("/flow")) return
	try { await useAPI("orgs/me") }
	catch {
		return navigateTo(authPath)
	}
})
