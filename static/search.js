
function Search() {
    // C:\react-js\myreactdev\src\App.js

    // Initial state
    let allname = [];
    let filterresult = [];
    let serachname = "";

    // Helper function to handle search
    const handleSearch = (event) => {
    const search = event.target.value;
    console.log(search);
    setSearchName(search);

    if (search !== "") {
        const filterData = allname.filter((item) => {
        return Object.values(item)
            .join("")
            .toLowerCase()
            .includes(search.toLowerCase());
        });
        setFilterResult(filterData);
    } else {
        setFilterResult(allname);
    }
    };

    // Fetch data from the server
    const getName = async () => {
    const getRes = await fetch("http://127.0.0.1:5000/listall");
    const setName = await getRes.json();
    console.log(setCounty);
    allname = setName;
    filterResult = setName;
    };

    // Initial data fetch
    getName();

    // Render function

    const input = document.createElement("input");
    input.type = "text";
    input.className = "form-control";
    input.placeholder = "Enter Keyword";
    input.addEventListener("input", (e) => {
        handleSearch(e);
    });
    const inputContainer = document.createElement("div");
    inputContainer.className = "search_bar";
    inputContainer.appendChild(input);
    row.appendChild(inputContainer);

    const table = document.createElement("table");
    table.className = "result_table";

    const thead = document.createElement("thead");
    const tr = document.createElement("tr");

    const th1 = document.createElement("th");
    th1.textContent = "Name";
    const th2 = document.createElement("th");
    th2.textContent = "Email";

    tr.appendChild(th1);
    tr.appendChild(th2);
    thead.appendChild(tr);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");
    if (serachname.length > 1) {
        filterresult.forEach((filtername, index) => {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        td1.textContent = filtername.email;
        const td2 = document.createElement("td");
        td2.textContent = filtername.name;
        tr.appendChild(td1);
        tr.appendChild(td2);
        tbody.appendChild(tr);
        });
    } else {
        allname.forEach((getcon, index) => {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td");
        td1.textContent = getcon.email;
        const td2 = document.createElement("td");
        td2.textContent = getcon.name;
        tr.appendChild(td1);
        tr.appendChild(td2);
        tbody.appendChild(tr);
        });
    }

    table.appendChild(tbody);
    row.appendChild(table);
    container.appendChild(row);

    // Find the element where you want to append the result (e.g., <div id="root"></div>)
    const rootElement = document.getElementById("searchRoot");

};