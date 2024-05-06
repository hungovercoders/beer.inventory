import { Link } from 'react-router-dom'

const Navbar = () => {
    return ( 
        <nav className="navbar">
            <h1>Beers</h1>
            <div className="links">
                <Link to="/">Home</Link>
                <Link to="/create" >New Beer</Link>
            </div>
        </nav>
     );
}
 
export default Navbar;