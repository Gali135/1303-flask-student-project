

function Messages(props) {
    const [messages, setMessages] = React.useState([]);
    const getMessages = () => {
        axios.get("/messages").then((result) => {
            setMessages(result.data);
        })
    }
    React.useEffect(() => {
        getMessages();
        setInterval(getMessages, props.interval);
    }, []
    )
    return (
        <div>
            <h3>Messages</h3>
            <div>{messages.map((item) =>
                <div>
                    <h6>{item[1]}</h6>
                    <b>{item[0]}</b>
                </div>
            )}</div>
            {/* <button onClick={getMessages}>Get New Messages</button> */}
        </div>
    );
}

ReactDOM.render(<Messages interval={60*60*1000} />, document.getElementById("Hmessages"));
