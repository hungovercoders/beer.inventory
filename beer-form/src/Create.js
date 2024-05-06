import { useState } from "react";
import { useNavigate } from 'react-router-dom'

const Create = () => {
    //state
    const [name, setName] = useState('');
    const [brewer, setBrewer] = useState('');
    const [strength, setStrength] = useState('');
    const [flavours, setFlavours] = useState('');
    const [isPending, setIsPending] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault(); //stops page refresh
        const beer = {name, brewer, strength, flavours};
        setIsPending(true);
        
        fetch('http://localhost:8000/beers', {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(beer)
        }).then(() => {
            console.log(JSON.stringify(beer));
            setIsPending(false);
            navigate('/');
        })

    }

    return ( 
        <div className="create">
            <h2>Add a New Beer</h2>
            <form onSubmit={handleSubmit}>
                <label>Beer Name</label>
                <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                />
                 <label>Brewer</label>
                <textarea
                required
                value={brewer}
                onChange={(e) => setBrewer(e.target.value)}
                ></textarea>
                <label>Strength</label>
                <input
                type="text"
                required
                value={strength}
                onChange={(e) => setStrength(e.target.value)}
                />
                <select
                value={flavours}
                onChange={(e) => setFlavours(e.target.value)}
                >
                    <option value="hoppy">hoppy</option>
                    <option value="caramel">caramel</option>
                </select> 
                { !isPending && <button>Add Beer</button> }
                { isPending && <button disabled>Adding Beer...</button> }
            </form>
        </div>
     );
}
 
export default Create;