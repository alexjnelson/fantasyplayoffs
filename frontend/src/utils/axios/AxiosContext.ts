import { createContext } from "react";

export interface AxiosInstance {
  get<T>(url: string, config?: object | undefined): Promise<T>;
  post<T>(url: string, config?: object | undefined): Promise<T>;
  put<T>(url: string, config?: object | undefined): Promise<T>;
  delete<T>(url: string, config?: object | undefined): Promise<T>;
}

export interface AxiosContextValue {
  axios: AxiosInstance;
}

const AxiosContext = createContext<AxiosContextValue | undefined>(undefined);

export default AxiosContext;
