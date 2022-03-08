import React from "react"



export default function Trobo(props){



    
        return (
            <div
              className="comment-action"
            >
              <div key={props.id} class="selectWrapper">
              <select id="strategy" onChange={() => props.trollComment(props.comment,document.getElementById("strategy").value)}>
              <option value="TROBO">Troll Options</option>
              <option value="JOKE">Jokes</option>
              <option value="MEME">Memes</option>
              <option value="QUOTE">Quotes</option>
              <option value="TOXIC">Toxic</option>
            </select>
            </div>

            </div>
        )




}