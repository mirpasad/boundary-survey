import { CrossIcon } from "./Icons";

const Sidebar = ({ isSidebarShow, setSidebarShow }) => {
  return (
    <>
      <aside
        className={`${
          isSidebarShow ? "translate-x-0" : "-translate-x-full xl:translate-x-0"
        } fixed left-0 top-0 xl:static max-w-[220px] min-w-[220px] 3xl:max-w-[220px] 3xl:min-w-[220px] h-screen overflow-hidden bg-primary transition-all duration-300 ease-in-out z-50`}
      >
        <div className="px-4 lg:px-7 3xl:px-8 h-full flex flex-col">
          <div className="flex items-center justify-between my-5 lg:my-6">
            <h2 className="text-white text-lg font-semibold">Sidebar</h2>
            <button className="xl:hidden" onClick={() => setSidebarShow(false)}>
              <CrossIcon />
            </button>
          </div>

          <div className="flex grow pt-5 lg:pt-6 text-white flex-col gap-3 mt-2">
            <p className="text-white text-sm opacity-70">Navigation removed</p>
          </div>
        </div>
      </aside>

      {isSidebarShow && (
        <div
          onClick={() => setSidebarShow(false)}
          className="fixed top left-0 bg-primary/30 w-full h-full z-10"
        ></div>
      )}
    </>
  );
};

export default Sidebar;
