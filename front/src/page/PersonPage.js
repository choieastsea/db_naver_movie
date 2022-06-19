import { useNavigate, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { NotFound } from "./NotFound";
import {
  CircularProgress,
  Card,
  CardContent,
  Typography,
  CardMedia,
  Grid,
  CardActionArea,
} from "@mui/material";
export const PersonPage = () => {
  /* 해당 인물 코드의 영화인의 페이지. 필모그래피를 담고 있음 */
  const [searchParams] = useSearchParams();
  const code = searchParams.get("code");
  //해당 인물이 출연한 영화 코드, 간단한 정보를 가져옴
  const [movieData, setMovieData] = useState({});
  const [filmoList, setFilmoList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    async function fetchMovie() {
      const data = await fetch(`api/person/filmography?code=${code}`); //영화 데이터 중 메인에서 필요한 것만 가져옴
      const res = await data.json();
      console.log(res);
      setMovieData(res);
      if (res.result === "success") {
        setFilmoList(res.data);
      }
      setIsLoading(false);
    }
    fetchMovie();
  }, [code]);
  return (
    <div>
      {code !== null ? (
        isLoading ? (
          <CircularProgress />
        ) : (
          <div>
            <h1>{movieData.name} 필모그래피</h1>
            <Grid container spacing={0} justifyContent="center">
              {filmoList.map((e) => (
                <CastingCard data={e} key={e.title_kor} />
              ))}
            </Grid>
          </div>
        )
      ) : (
        <NotFound />
      )}
    </div>
  );
};

const CastingCard = ({ data }) => {
  const navigate = useNavigate();
  const toFilmPage = () => {
    navigate(`/movie?code=${data.movie_code}`);
  };
  return (
    <Grid item xs={2}>
      <Card>
        <CardActionArea onClick={toFilmPage}>
          <CardContent>
            <Typography
              sx={{ fontSize: 20 }}
              color="text.secondary"
              gutterBottom
            >
              {data.title_kor}
              {data.release_date && `(${data.release_date.split(".")[0]})`}
            </Typography>
            <Typography
              sx={{ fontSize: 15 }}
              color="text.secondary"
              gutterBottom
            >
              {data.casting_name}
            </Typography>
            <CardMedia
              component="img"
              image={`${
                data.img_url !== null
                  ? data.img_url
                  : "https://ssl.pstatic.net/static/movie/2012/06/dft_img133x190.png"
              }`}
              alt={`${data.img_url}`}
            />
          </CardContent>
        </CardActionArea>
      </Card>
    </Grid>
  );
};
