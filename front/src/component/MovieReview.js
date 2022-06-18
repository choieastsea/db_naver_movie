import { Pagination, Box } from "@mui/material";
import { useEffect, useState } from "react";
export const Review = ({ movie_code }) => {
  const [reviewData, setReviewData] = useState({});
  const [curPage, setCurPage] = useState(1);
  useEffect(() => {
    async function fetchReviewData() {
      const data = await fetch(
        `api/movie/review?code=${movie_code}&page=${curPage}`
      );
      const res = await data.json();
      console.log(res);
      setReviewData(res);
    }
    fetchReviewData();
  }, [movie_code, curPage]);

  const { review_list } = reviewData;

  let count = parseInt(reviewData.length / 10) + 1; //총 페이지 수
  // let count = 10;

  const onPageChange = (event, page) => {
    console.log(page);
    setCurPage(page);
  };
  return reviewData?.length === 0 ? (
    <div>리뷰가 없습니다.</div>
  ) : (
    <div>
      <p>총 리뷰 : {reviewData.length}건</p>
      <ul>
        {/* pagination needed */}
        {review_list?.map((e) => (
          <li key={e.id}>
            <a href={`/movie/review?code=${movie_code}&user=4807776`}>
              {e.writer}
            </a>
            {/* needed to change! */}
            <p>{e.content}</p>
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
