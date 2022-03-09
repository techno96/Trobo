import Comments from "./comments/Comments";
import NavBar from "./NavBar";


const App = () => {
  return (
    <div >
      <NavBar/>
      <Comments
        commentsUrl="http://localhost:3004/comments"
        currentUserId="1"
      />
    </div>
  );
};



export default App;
