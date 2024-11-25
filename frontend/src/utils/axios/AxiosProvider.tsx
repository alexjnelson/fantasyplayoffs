import { ReactNode, useEffect, useMemo } from "react";
import axios from "axios";

import AxiosContext from "./AxiosContext";
import useAuth from "../auth/useAuth";

interface AxiosProviderProps {
  token: string | undefined
  children: ReactNode;
}

const AxiosProvider = ({ token, children }: AxiosProviderProps): JSX.Element => {
  const _axiosInstance = useMemo(() => {
    return axios.create();
  }, []);

  useEffect(() => {
    if (_axiosInstance) {
      if (token) {
        _axiosInstance.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${token}`;
      } else {
        delete _axiosInstance.defaults.headers.common["Authorization"];
      }
    }
  }, [_axiosInstance, token]);

  const baseConfig = {
    baseURL: process.env.REACT_APP_API_BASE_URL,
    headers: undefined,
  };

  const getAxiosConfig = (config: object | undefined): any => {
    return config ? { ...baseConfig, ...config } : baseConfig;
  };

  const getAxiosPostConfig = (
    data: object | undefined,
    config: object | undefined
  ): any => {
    const axiosConfig = getAxiosConfig(config);

    if (data && Object.keys(data).length === 1) {
      axiosConfig.headers = {
        "Content-Type": "text/plain",
      };
    } else if (data) {
      axiosConfig.headers = {
        "Content-Type": "application/json",
      };
    }

    return axiosConfig;
  };

  function _get<T>(url: string, config?: object | undefined): Promise<T> {
    const axiosConfig = getAxiosConfig(config);
    return _axiosInstance.get(url, axiosConfig);
  }

  function _post<T>(
    url: string,
    data?: Object | undefined,
    config?: object | undefined
  ): Promise<T> {
    const axiosConfig = getAxiosPostConfig(data, config);
    return _axiosInstance.post(url, data, axiosConfig);
  }

  function _put<T>(
    url: string,
    data?: Object | undefined,
    config?: object | undefined
  ): Promise<T> {
    const axiosConfig = getAxiosPostConfig(data, config);
    return _axiosInstance.put(url, data, axiosConfig);
  }

  function _delete<T>(url: string, config?: object | undefined): Promise<T> {
    const axiosConfig = getAxiosConfig(config);
    return _axiosInstance.delete(url, axiosConfig);
  }

  return (
    <AxiosContext.Provider
      value={{
        axios: {
          get: _get,
          post: _post,
          put: _put,
          delete: _delete,
        },
      }}
    >
      {children}
    </AxiosContext.Provider>
  );
};

export default AxiosProvider;
