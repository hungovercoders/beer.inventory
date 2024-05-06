import { Link } from "react-router-dom";

const BeerList = ({ beers }) => {
  return (
    <div className="beer-list">
      {beers.map(beer => (
        <div className="beer-preview" key={beer.id} >
          <Link to={`/beers/${beer.id}`}>
            <h2>{beer.name}</h2>
            <p>Brewed by {beer.brewer}</p>
          </Link>
        </div>
      ))}
    </div>
  );
}

export default BeerList;