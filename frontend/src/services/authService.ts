import { AxiosInstance } from "../utils/axios/AxiosContext";

const URL_BASE = '/auth';

interface AuthenticateResponse {
    google_id: string;
}

export function authenticate(axios: AxiosInstance, token: string): Promise<AuthenticateResponse> {
    return axios.post<AuthenticateResponse>(URL_BASE + '/login-sso', {id_token: token});
}

export function devLogin(axios: AxiosInstance, email: string): Promise<AuthenticateResponse> {
    return axios.post<AuthenticateResponse>(URL_BASE + '/dev-login', {email: email});
}

export function devCreateAccount(axios: AxiosInstance, email: string, name: string): Promise<AuthenticateResponse> {
    return axios.post<AuthenticateResponse>(URL_BASE + '/dev-create-user', {email: email, name: name});
}