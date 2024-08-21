import type { NitroFetchRequest, NitroFetchOptions } from 'nitropack'

export const useAPI = async (request: NitroFetchRequest, opts?: NitroFetchOptions<NitroFetchRequest, "get" | "head" | "patch" | "post" | "put" | "delete" | "connect" | "options" | "trace"> | undefined, client_mode?: boolean): Promise<any> => {
	const API_SERVER = "https://api.feedbacker.online"
	const access = useCookie(client_mode ? "user_access_token" : "access_token")
	return $fetch(`${API_SERVER}/${request}`, {
		headers: {
			Authorization: `Bearer ${access.value}`
		},
		...opts
	})
}
