import "./../css/Navbar.css";

const Navbar = () => {
  return (
    <div className="navbar">
      <button className="button">Home</button>
      <button className="button">About</button>
      <button className="button">Contact</button>
      <button className="button">Login</button>
      <button className="character_button">
        <h1>C</h1>
      </button>
    </div>
  );
};

export default Navbar;
