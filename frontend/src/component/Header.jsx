import React from "react";

const isHeadingElement = (el) =>
  React.isValidElement(el) &&
  typeof el.type === "string" &&
  /^(h[1-6])$/.test(el.type.toLowerCase());

const Header = ({ children }) => {
  return (
    <header className="flex flex-col lg:flex-row justify-between pl-3 lg:pl-6 3xl:pl-8 pr-3 pt-3 pb-5 sm:py-3">

      {isHeadingElement(children) ? (
        children
      ) : (
        <h3 className="text-[26px] grow font-switzerMedium text-primary">
          {children}
        </h3>
      )}
    </header>
  );
};

export default Header;
