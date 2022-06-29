import React from "react";
import { default as Logokanal } from "../assets/logokanal.png";

const Header = () => {
  return (
    <div className="header">
      <img className="img-logo" src={Logokanal} alt="Logo" />
    </div>
  );
};

export default Header;
