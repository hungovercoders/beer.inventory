import { useNavigate, useParams } from "react-router-dom";
import useFetch from "./useFetch";

const BeerDetails = () => {
    const { id } = useParams();
    const { data: beer, error, isPending } = useFetch('http://localhost:8000/beers/' + id);
    const navigate = useNavigate();

    const handleClick = () => {
        fetch('http://localhost:8000/beers/' + beer.id, {
            method: 'DELETE'
        }).then(() => {
            navigate('/');
        })
    }

    return (
        <div className="beer-details">
            {isPending && <div>Pouring...</div>}
            {error && <div>{error}</div>}
            {beer && (
                <article>
                    <h2>{beer.name}</h2>
                    <p>Brewed by {beer.brewer}</p>
                    <div>Strength: {beer.strength} %</div>
                    <div>Flavours: {beer.flavours}</div>
                    <button onClick={handleClick}>Delete Beer</button>
                </article>
            )}
        </div>
    );
}

export default BeerDetails;