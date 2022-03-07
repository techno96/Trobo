import { useState, useEffect } from "react";
import CommentForm from "./CommentForm";
import Comment from "./Comment";
import {
  getComments as getCommentsApi,
  createComment as createCommentApi,
  updateComment as updateCommentApi,
  deleteComment as deleteCommentApi,
} from "../api";

const Comments = ({ commentsUrl, currentUserId }) => {
  const [backendComments, setBackendComments] = useState([]);
  const [activeComment, setActiveComment] = useState(null);
  const rootComments = backendComments.filter(
    (backendComment) => backendComment.parentId === null
  );
  const [trollResponse, setTrollResponse] = useState("");
  const [imgResponse, setImgResponse] = useState(false);
  const getReplies = (commentId) =>
    backendComments
      .filter((backendComment) => backendComment.parentId === commentId)
      .sort(
        (a, b) =>
          new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      );

  const addComment = (text, parentId) => {
    createCommentApi(text, parentId).then((comment) => {
      setBackendComments([comment, ...backendComments]);
      setActiveComment(null);
      setTrollResponse("");
      setImgResponse(false);
    });
  };

  const updateComment = (text, commentId) => {
    updateCommentApi(text).then(() => {
      const updatedBackendComments = backendComments.map((backendComment) => {
        if (backendComment.id === commentId) {
          return { ...backendComment, body: text };
        }
        return backendComment;
      });
      setBackendComments(updatedBackendComments);
      setActiveComment(null);
    });
  };

  const deleteComment = (commentId) => {
    if (window.confirm("Are you sure you want to remove comment?")) {
      deleteCommentApi().then(() => {
        const updatedBackendComments = backendComments.filter(
          (backendComment) => backendComment.id !== commentId
        );
        setBackendComments(updatedBackendComments);
      });
    }
  };

  const trollComment = (comment, strategy) => {
  
    let query = "http://localhost:9000/predict?query=" + comment.body + "&strategy=" +strategy
    console.log(query)
    if(strategy == "MEME"){
      setImgResponse(true)
    } else {
      setImgResponse(false)
    }
    console.log(imgResponse)
  fetch(query,{
    'methods':['GET','POST']
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.prediction)
    setTrollResponse(data.prediction)
    setTrollResponse((prevState) => {
      console.log("new state is", prevState);
      return prevState;
    })
    //console.log("troll response updated is ",trollResponse) 
  })
  .catch(error => console.log(error))
  }

  useEffect(() => {
    getCommentsApi().then((data) => {
      setBackendComments(data);
    });
  }, []);

  return (

    <div className="comments" key={trollResponse}>
      
      <CommentForm submitLabel="Post" handleSubmit={addComment} />
      <div className="comments-container">
        {rootComments.map((rootComment) => (
          <Comment
            key={rootComment.id}
            comment={rootComment}
            replies={getReplies(rootComment.id)}
            activeComment={activeComment}
            setActiveComment={setActiveComment}
            addComment={addComment}
            deleteComment={deleteComment}
            updateComment={updateComment}
            trollComment={trollComment}
            currentUserId={currentUserId}
            trollResponse={trollResponse}
            imgResponse={imgResponse}
          />
        ))}
      </div>
    </div>

  );
};

export default Comments;
