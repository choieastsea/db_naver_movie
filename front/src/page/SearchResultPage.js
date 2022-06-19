import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import BasicMovie from "../component/BasicMovie";
import { NotFound } from "./NotFound";
import {
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  FormGroup,
  Grid,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
export const SearchResultPage = () => {
  const [searchParams] = useSearchParams();
  const userInput = searchParams.get("userInput");
  const [result, setResult] = useState({});
  const [resultMovieList, setResultMovieList] = useState([]);
  const [resultPeopleList, setResultPeopleList] = useState([]);
  const [sortBy, setSortBy] = useState("title_kor");
  const [onlyRunning, setOnlyRunning] = useState(false);
  useEffect(() => {
    async function fetchMovie() {
      console.log("fetchMovie");
      const movie_data = await fetch(
        `api/search/movie?userInput=${userInput}&sortby=${sortBy}&onlyRunning=${onlyRunning}`
      );
      const movie_res = await movie_data.json();
      const people_data = await fetch(
        `api/search/people?userInput=${userInput}`
      );
      const people_res = await people_data.json();
      setResultMovieList(movie_res.data);
      setResultPeopleList(people_res.data);
      setResult(movie_res.result && people_res.result);
    }
    fetchMovie();
  }, [userInput, sortBy, onlyRunning]);
  const handleChange = (e) => {
    setSortBy(e.target.value);
  };
  const handleChange2 = (e) => {
    setOnlyRunning(e.target.checked);
  };
  const navigate = useNavigate();
  const toFilmPage = (code) => {
    navigate(`/movie?code=${code}`);
  };
  const toPeoplePage = (code) => {
    navigate(`/person?code=${code}`);
  };
  return result === "success" ? (
    <div>
      {/* 현재 상영중인 영화 결과만 보기 */}
      <h2>영화 검색 결과</h2>
      <FormControlLabel
        control={
          <Checkbox
            checked={onlyRunning}
            onChange={handleChange2}
            inputProps={{ "aria-label": "controlled" }}
          />
        }
        label="상영중인 영화만 보기"
      />
      {/* 정렬도 해야함!!!! */}
      <Select
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={sortBy}
        onChange={handleChange}
        size="small"
      >
        {/* 영화에 대하여 정렬 */}
        <MenuItem value="title_kor">가나다순</MenuItem>
        <MenuItem value="release_date desc">년도순</MenuItem>
        <MenuItem value="cumulate_audience desc">누적관객순</MenuItem>
      </Select>

      {resultMovieList.length !== 0 ? (
        <div>
          <h3>검색결과: {resultMovieList.length}건</h3>
          <Grid container spacing={1}>
            {resultMovieList.map((e) => (
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
          </Grid>
        </div>
      ) : (
        <p>"{userInput}"으로 시작하는 영화 정보가 없습니다</p>
      )}
      <div>
        <hr />
      </div>
      <h2>영화인 검색 결과</h2>
      {resultPeopleList.length !== 0 ? (
        <div>
          <h3>검색결과: {resultPeopleList.length}건</h3>
          <Grid container>
            {resultPeopleList.map((e) => (
              <Grid item xs={2}>
                <Card>
                  <CardActionArea onClick={() => toPeoplePage(e.people_code)}>
                    <CardContent>
                      <Typography
                        sx={{ fontSize: 15 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.name}
                      </Typography>

                      <CardMedia
                        component="img"
                        image={`${
                          e.thumbnail !== null
                            ? e.thumbnail
                            : "https://ssl.pstatic.net/static/movie/2012/06/dft_img133x190.png"
                        }`}
                        alt={`${e.thumbnail}`}
                        sx={{ height: "240px" }}
                      />
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        </div>
      ) : (
        <p>"{userInput}"으로 시작하는 인물 정보가 없습니다</p>
      )}
    </div>
  ) : (
    <CircularProgress />
  );
};
