function AddMessageForm() {
    const handleSubmit=(event)=>{
        event.preventDefault();
        const newMessage=event.target.elements.message.value;
        axios.post("/add_m", {message:newMessage}).then(
            response=>console.log(response.data)
        )
    }
    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="message" autoFocus />
            <input type="submit" value="Add Message" />
        </form>
    )
}


ReactDOM.render(<AddMessageForm />, document.getElementById("addForm"));