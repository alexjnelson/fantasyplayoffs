import Header from "./Header";
import Footer from "./Footer";
import { ReactNode } from "react";


export interface LayoutProps {
  children: ReactNode
};

function Layout({children}: LayoutProps) {
  return <>
    <Header />
    {children}
    <Footer />
  </>;
}

export default Layout;
