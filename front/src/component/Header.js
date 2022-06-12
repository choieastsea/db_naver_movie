import { Link } from "react-router-dom";

export const Header = ({ children }) => {
  return (
    <header>
      <h1>
        <Link to="/" className="header">{children}</Link>
      </h1>
    </header>
  );
};
