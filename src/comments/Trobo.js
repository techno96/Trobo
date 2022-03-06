import React from "react"



export default function Trobo(props){



        return (
            <div
              className="comment-action"
              onClick={() => props.trollComment()}
            >
              <div class="selectWrapper">
              <select >
                <option>Trobo</option>
              <option>Jokes</option>
              <option>Memes</option>
              <option>Quotes</option>
              <option>Toxic</option>
            </select>
            </div>

            </div>
        )




}