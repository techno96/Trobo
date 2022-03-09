import React from "react"



export default function Trobo(props){

  const [valueState,setValueState] = React.useState("TROBO")

  function updateHandler(event) {
    const value = event.target.value
    console.log(event.target.value)
    setValueState(() => value)
    props.trollComment(props.comment,event.target.value)
}

    
        return (
            <div
              className="comment-action"
            >
              <div key={props.id} class="selectWrapper">
              <select id="strategy" value={valueState} onChange={updateHandler}>
              <option value="TROBO">Troll Option</option>
              <option value="JOKE">Jokes</option>
              <option value="MEME">Memes</option>
              <option value="QUOTE">Quotes</option>
              <option value="TOXIC">Toxic</option>
            </select>
            </div>
            </div>
        )




}