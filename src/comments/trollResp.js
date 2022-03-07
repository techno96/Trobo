import { useState } from "react";
import { Component } from "react/cjs/react.production.min";

const TrollResp = ({
  handleSubmit,
  submitLabel,
  hasCancelButton = false,
  handleCancel,
  initialText = "",
}) => {
  const [text, setText] = useState(initialText);
  const isTextareaDisabled = text.length === 0;
  const onSubmit = (event) => {
    event.preventDefault();
    handleSubmit(text);
    setText("");
  };

  console.log("Rendering stuff ", initialText);
  
  return (
    <form onSubmit={onSubmit}>
      <div contentEditable="true">
        <img src={text}/>
        </div>
      <button className="form--submit" disabled={isTextareaDisabled}>
        {submitLabel}
      </button>
      {hasCancelButton && (
        <button
          type="button"
          className="form--submit comment-form-cancel-button"
          onClick={handleCancel}
        >
          Cancel
        </button>
      )}
    </form>
  );
};

export default TrollResp;
