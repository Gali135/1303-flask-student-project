
var today = new Date();
var date = today.toLocaleDateString();
document.getElementById("localDate").innerHTML = date


function addCourse() {
  alert("Corse was added succefuly !");
}

function Message(props){
  const[message, setMessage] = React.useState(["Welcome!"]);

  const getData = () => {
    axios.get("/message").then(response => {
      setMessage(response.data);
    })                                                   
  }

  React/useEffect(() => {
    setInterval(getData, props.interval);
  },[]
  )

  return (
    <div>
        {message.map((item) => 
        <div>{item}</div>
        )}
        
    </div>
  );
}

reactDOM.render(<Message interval={5000} />, document.getElementById("messages"));