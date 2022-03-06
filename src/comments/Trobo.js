import React from "react"



export default function Trobo(props){



        


        return (
            <div
              className="comment-action"
            >
              <div class="selectWrapper">
              <select id="strategy" onChange={() => props.trollComment(props.comment,document.getElementById("strategy").value)}>
              <option value="Trobo">Trobo</option>
              <option value="Jokes">Jokes</option>
              <option value="Memes">Memes</option>
              <option value="Quotes">Quotes</option>
              <option value="Toxic">Toxic</option>
            </select>
            </div>

            </div>
        )




}