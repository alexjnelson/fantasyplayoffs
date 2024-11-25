import { useContext } from "react";

import AxiosContext, { AxiosContextValue } from "./AxiosContext";

const useAxios = (): AxiosContextValue => {
  const context = useContext(AxiosContext);

  if (!context) {
    throw new Error("useAxios must be used within an AxiosProvider");
  }

  return context;
};

export default useAxios;
