import { Pagination, Box, Rating } from "@mui/material";
import { useEffect, useState } from "react";
export const Score = ({ movie_code }) => {
  /* need update to score data from review */
  const [commentData, setCommentData] = useState({});
  const [curPage, setCurPage] = useState(1);
  useEffect(() => {
    async function fetchReviewData() {
      const data = await fetch(
        `api/movie/comment?code=${movie_code}&page=${curPage}`
      );
      const res = await data.json();
      console.log(res);
      setCommentData(res);
    }
    fetchReviewData();
  }, [movie_code, curPage]);

  const { comment_list } = commentData;

  let count = parseInt(commentData.length / 10);
  if (commentData.length % 10 !== 0) {
    count += 1;
  }
  // let count = 10;

  const onPageChange = (event, page) => {
    console.log(page);
    setCurPage(page);
  };
  return commentData?.length === 0 || commentData?.result === "fail" ? (
    <div>평점이 없습니다.</div>
  ) : (
    <div>
      {/* <p>총 리뷰 : {commentData.length}건</p> */}
      <ul>
        {/* pagination needed */}
        {comment_list?.map((e) => (
          <li key={e.comment_id}>
            <a href={`/movie/review?code=${movie_code}&user=4807776`}>
              {e.writer}
            </a>
            {/* needed to change! */}
            <Rating
              name="read-only"
              value={e.comment.score / 2}
              precision={0.1}
              readOnly
            />
            <p>{e.comment.comment}</p>
          </li>
        ))}
      </ul>
      <Pagination
        count={isNaN(count) ? 1 : count}
        size="small"
        color="primary"
        onChange={onPageChange}
        defaultPage={1}
        style={{ justifyContent: "center" }}
      />
    </div>
  );
};
