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
            <div class="title">Enter Message:</div>
            <input type="text" name="message" autoFocus />
            <br></br><input type="submit" value="Add" />
        </form>
    )
}


ReactDOM.render(<AddMessageForm />, document.getElementById("addForm"));