import { Pagination, Box, Rating } from "@mui/material";
import { useEffect, useState } from "react";
export const Review = ({ movie_code }) => {
  const [reviewData, setReviewData] = useState({});
  const [curPage, setCurPage] = useState(1);
  const [showcontent, setShowContent] = useState([
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  ]);
  useEffect(() => {
    async function fetchReviewData() {
      const data = await fetch(
        `api/movie/review?code=${movie_code}&page=${curPage}`
      );
      const res = await data.json();
      console.log(res);
      setReviewData(res);
      let ar = [];
      for (let i = 0; i < reviewData.length; i++) {
        ar.push(0);
      }
      setShowContent(ar);
    }
    fetchReviewData();
  }, [movie_code, curPage]);

  const { review_list } = reviewData;

  let count = parseInt(reviewData.length / 10); //총 페이지 수
  if (reviewData.length % 10 !== 0) {
    count += 1;
  }

  const onPageChange = (event, page) => {
    console.log(page);
    setCurPage(page);
  };
  const showContents = (key) => {
    console.log(`show content ${key}`);
    let arr = [];
    for (let i = 0; i < reviewData.length; i++) {
      if (i === key && showcontent[i] === 0) {
        console.log("push 1!");
        arr.push(1);
      } else {
        arr.push(0);
      }
    }
    console.log(`after show content : ${arr}`);
    setShowContent(arr);
  };
  return reviewData?.length === 0 ? (
    <div>리뷰가 없습니다.</div>
  ) : (
    <div>
      <p>총 리뷰 : {reviewData.length}건</p>
      <p className="pt-sm">(클릭하여 해당 리뷰 내용을 볼 수 있습니다.)</p>
      <ul>
        {/* pagination needed */}
        {review_list?.map((e, key) => (
          <li
            style={{ cursor: "pointer" }}
            key={e.review_id}
            onClick={() => showContents(key)}
          >
            {/* needed to change! */}
            <p>
              {e.review.title}({e.review.date})
            </p>
            <p>{e.review.writer}</p>
            {/* <p>{key}</p> */}
            <Rating
              name="read-only"
              value={e.review.review_score / 2}
              precision={0.1}
              readOnly
            />
            <p>조회수 : {e.review.view_num}</p>
            <p>추천수 : {e.review.good}</p>
            <div
              style={{
                display: `${showcontent[key] !== 1 ? "none" : "block"}`,
              }}
              dangerouslySetInnerHTML={{
                __html: e.review.contents.slice(0, -1).slice(1),
              }}
            ></div>
            <hr />
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
