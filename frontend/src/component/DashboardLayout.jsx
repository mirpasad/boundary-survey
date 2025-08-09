import { useState } from "react";
import Sidebar from "./Sidebar";

const DashboardLayout = ({ children }) => {
  const [isSidebarShow, setSidebarShow] = useState(false);

  return (
    <div>
      <main className="flex h-[100dvh] overflow-hidden w-full">
        <Sidebar
          isSidebarShow={isSidebarShow}
          setSidebarShow={setSidebarShow}
        />
        <div className="w-full xl:w-[calc(100vw-220px)]">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
