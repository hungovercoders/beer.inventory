//import logo from './logo.svg';
//import './App.css';
import Navbar from './Navbar'
import Home from './Home'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Create from './Create';
import BeerDetails from './BeerDetails';
import NotFound from './NotFound';

function App() {

  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="content">
          <Routes>
            <Route path='/' element={<Home />} />
             <Route path='/create' element={<Create />} />
             <Route path='/beers/:id' element={<BeerDetails />} />
            <Route path='*' element={<NotFound />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
