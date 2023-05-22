


function Search_r() {

    const [allname, setAllname]= React.useState([]);
    const [filterresult, setFilterresult]= React.useState([]);
    const [searchname, setSearchname]= React.useState("");
    const [searchemail, setSearchemail]= React.useState("");

    const handlesearch = (event) => {
        const search = event.target.value;
        console.log(search);
        setSearchname(search);
        setSearchemail(search);

        if (search !== "") {
            const filterdata = allname.filter((item) => {
                return Object.value(item)
                    .join("")
                    .toLowerCase()
                    .includes(serach.toLowerCase());

            });
            setFilterresult(filterdata);
        } else {
            setFilterresult(allname);
        }
    };

    
        
        // React.useEffect(() => {
        //     getName();
        //     setInterval(getName, props);
        // }, []
        // )
       

    useEffect(() => {
        const getname = async () => {
            const getres = axios.get("/listall").then((result) => {setname(result.data)});
            const setname = await getres.json;
            console.log(setname);
            setAllname(await setname);
        };
        getname();
    },[]);
    
    return (
        <div className="search_bar">
            <input
                type="text"
                className="form_control"
                placeholder="Enter Name or Email"
                onChange={(e) =>{
                    handlesearch(e);
                }}
            />
            <table clasName="result_table">
                <thead>
                    <tr>
                        <th> Name</th>
                        <th> Email</th>
                    </tr>
                </thead>
                <tbody>
                    {searchname.length > 1
                    ? filterresult.map((filtername, index) => (
                        <tr key={index}>
                            <td> {filtername[0]} </td>
                            <td> {filtername[1]} </td>
                        </tr>
                    ))
                :   allname.map((getcon, index) =>(
                    <tr key={index}>
                        <td> {getcon.name} </td>
                        <td> {getcon.email} </td>
                </tr>
                ))}
                </tbody>
            </table>
        </div>
        
    );
}

// ReactDOM.render(document.getElementById("searchRoot"));
