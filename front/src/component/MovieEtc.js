import {
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Grid,
  Pagination,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
export const ETC = ({ movie_code }) => {
  const [quotesData, setQuotesData] = useState({});
  const [relateMovieData, setRelativeMovieData] = useState([]);
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
  useEffect(() => {
    async function fetchRelateData() {
      const data = await fetch(`api/movie/relate?code=${movie_code}`);
      const res = await data.json();
      setRelativeMovieData(res);
    }
    fetchRelateData();
  }, [movie_code]);
  const onPageChange = (event, page) => {
    console.log(page);
    setCurPage(page);
  };
  const navigate = useNavigate();
  const toFilmPage = (code) => {
    navigate(`/movie?code=${code}`);
  };
  const { quotes_list } = quotesData;
  const { movie_list } = relateMovieData;
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
        {relateMovieData?.length === 0 || relateMovieData?.result === "fail" ? (
          <p>관련 영화 정보가 없습니다.</p>
        ) : (
          <div>
            {movie_list.map((e) => (
              <Grid item xs={2}>
                <Card>
                  <CardActionArea onClick={() => toFilmPage(e.movie_code)}>
                    <CardContent>
                      <Typography
                        sx={{ fontSize: 15 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.title_kor}
                        {e.release_date && `(${e.release_date.split(".")[0]})`}
                      </Typography>

                      <CardMedia
                        component="img"
                        image={`${
                          e.img_url !== null
                            ? e.img_url
                            : "https://ssl.pstatic.net/static/movie/2012/06/dft_img133x190.png"
                        }`}
                        alt={`${e.img_url}`}
                        sx={{ height: "240px" }}
                      />
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </div>
        )}
      </Grid>
    </Grid>
  );
};
