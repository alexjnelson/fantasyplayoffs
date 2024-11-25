import { AxiosInstance } from "../utils/axios/AxiosContext";

const URL_BASE = '/auth';

interface AuthenticateResponse {
    google_id: string;
}

export function authenticate(axios: AxiosInstance, token: string): Promise<AuthenticateResponse> {
    return axios.post<AuthenticateResponse>(URL_BASE + '/login-sso', {id_token: token});
}