import { Grid, Pagination } from "@mui/material";
import { useEffect, useState } from "react";
export const ETC = ({ movie_code }) => {
  const [quotesData, setQuotesData] = useState({});
  const [curPage, setCurPage] = useState(1);

  useEffect(() => {
    async function fetchReviewData() {
      const data = await fetch(
        `api/movie/quotes?code=${movie_code}&page=${curPage}`
      );
      const res = await data.json();
      console.log(res);
      setQuotesData(res);
    }
    fetchReviewData();
  }, [movie_code, curPage]);
  const onPageChange = (event, page) => {
    console.log(page);
    setCurPage(page);
  };
  const { quotes_list } = quotesData;
  let count = parseInt(quotesData.length / 10);
  if (quotesData.length % 10 !== 0) {
    count += 1;
  }
  return (
    <Grid container spacing={1}>
      <Grid item xs={6}>
        <h2>명대사</h2>
        {quotesData?.length === 0 || quotesData.result === "fail" ? (
          <div>등록된 명대사가 없습니다.</div>
        ) : (
          <div>
            <ul>
              {/* pagination needed */}
              {quotes_list?.map((e) => (
                <li key={e.quotes.quotes_id}>
                  <p>
                    {e.quotes.quotes}(추천 {e.quotes.good}) by {e.quotes.userid}
                  </p>
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
        )}
      </Grid>
      <Grid item xs={6}>
        <h2>연관영화</h2>
      </Grid>
    </Grid>
  );
};
