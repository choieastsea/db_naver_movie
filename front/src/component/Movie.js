import { Link } from "react-router-dom";

export const Movie = ({ movieData, onMain = false }) => {
  return (
    <div
      style={{
        display: "inline-block",
        width: "800px",
        backgroundColor: "#FCF8E8",
        borderRadius: "20px",
        padding: "30px",
        margin: "20px",
        lineHeight: "25px",
      }}
    >
      <h2>
        <Link to={`/movie?code=${movieData?.code}`}>{movieData?.title}</Link>
      </h2>
      <h4>{movieData?.title_eng}</h4>
      {movieData?.aka && <p>a.k.a {movieData.aka}</p>}
      <p>{movieData.screening}분</p>
      <p>{movieData?.summary}</p>
      {!onMain && (
        <div>
          <h4>making note</h4>
          <p>{movieData?.making_note}</p>
          <h4>Review</h4>
          {movieData.review
            ? movieData.review.map((e) => (
                <div key={e.review_id}>
                  <p>작성자 : {e.writer}</p>
                  <p>{e.content}</p>
                  <hr />
                </div>
              ))
            : ""}
        </div>
      )}
    </div>
  );
};
