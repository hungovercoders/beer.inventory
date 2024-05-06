import BeerList from "./BeerList";
import useFetch from "./useFetch";

const Home = () => {

    const {data: beers, isPending, error} = useFetch('http://localhost:8000/beers')

    return (
        <div className="home">
            {error && <div>{error}</div>}
            {isPending && <div>Pouring...</div>}
            {beers && <BeerList beers={beers} />}
        </div>
    );
}

export default Home;