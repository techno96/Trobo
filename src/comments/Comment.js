import { useState } from "react/cjs/react.production.min";
import CommentForm from "./CommentForm";
import Trobo from "./Trobo";
import TrollResp from "./TrollResp"

const Comment = ({
  comment,
  replies,
  setActiveComment,
  activeComment,
  updateComment,
  deleteComment,
  addComment,
  trollComment,
  trollResponse,
  imgResponse,
  parentId = null,
  currentUserId,
}) => {
  const isEditing =
    activeComment &&
    activeComment.id === comment.id &&
    activeComment.type === "editing";
  
    const isReplying =
    activeComment &&
    activeComment.id === comment.id &&
    activeComment.type === "replying";

  const isTrolling =
    activeComment &&
    activeComment.id === comment.id &&
    activeComment.type === "trolling";
  
  const canCounterTroll = true;
  const fiveMinutes = 300000;
  const timePassed = new Date() - new Date(comment.createdAt) > fiveMinutes;
  const canDelete =
    currentUserId === comment.userId && replies.length === 0 && !timePassed;
  const canReply = Boolean(currentUserId);
  const canEdit = currentUserId === comment.userId && !timePassed;
  const replyId = parentId ? parentId : comment.id;
  const createdAt = new Date(comment.createdAt).toLocaleDateString();
  const canTroll = trollResponse.length > 0 ? true: false;
  //const [commentTrollResp, setCommentTrollResp] = useState({trollResponse})

  return (
    <div key={comment.id} className="comment">
      <div className="comment-image-container">
        <img src="/user-icon.png" />
      </div>
      <div className="comment-right-part">
        <div className="comment-content">
          <div className="comment-author">{comment.username}  <span className="created">{createdAt}</span></div>
          
        </div>
        {!isEditing && <div className="comment-text">{comment.body}</div>}
        {isEditing && (
          <CommentForm
            submitLabel="Update"
            hasCancelButton
            initialText={comment.body}
            handleSubmit={(text) => updateComment(text, comment.id)}
            handleCancel={() => {
              setActiveComment(null);
            }}
          />
        )}
        <div className="comment-actions">
          {canReply && (
            <div
              className="comment-action"
              onClick={() =>
                setActiveComment({ id: comment.id, type: "replying" })
              }
            >
              Reply
            </div>
          )}
          {canEdit && (
            <div
              className="comment-action"
              onClick={() =>
                setActiveComment({ id: comment.id, type: "editing" })
              }
            >
              Edit
            </div>
          )}
          {canDelete && (
            <div
              className="comment-action"
              onClick={() => deleteComment(comment.id)}
            >
              Delete
            </div>
          )}
         
          {canCounterTroll && (
             <div
             className="comment-action"
             onClick={() =>
               setActiveComment({ id: comment.id, type: "trolling" })
             }
           >
               <Trobo trollComment={trollComment} comment={comment}/>
           </div>
          )}

          
        </div>
        
        {canTroll && !imgResponse && (
          <CommentForm
            submitLabel="Reply"
            handleSubmit={(text) => addComment(text, replyId)}
            initialText={trollResponse}
            hasCancelButton={true}
            handleCancel={deleteComment}
          />
        )}

        {console.log("Image response is ", imgResponse)}

        {canTroll && imgResponse && (
          <TrollResp
          submitLabel="Reply"
          handleSubmit={(text) => addComment(text, replyId)}
          hasCancelButton={true}
          handleCancel={deleteComment}
        />
        )
        }
        
        {isReplying && (
          <CommentForm
            submitLabel="Reply"
            handleSubmit={(text) => addComment(text, replyId)}
          />
        )}

        

        {replies.length > 0 && (
          <div className="replies">
            {replies.map((reply) => (
              <Comment
                comment={reply}
                key={reply.id}
                setActiveComment={setActiveComment}
                activeComment={activeComment}
                updateComment={updateComment}
                deleteComment={deleteComment}
                addComment={addComment}
                trollComment={trollComment}
                trollResponse={trollResponse}
                imgResponse={imgResponse}
                parentId={comment.id}
                replies={[]}
                currentUserId={currentUserId}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Comment;
