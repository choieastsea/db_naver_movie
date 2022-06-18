import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { NotFound } from "./NotFound";
import BasicMovie from "../component/BasicMovie";
import MovieSummary from "../component/MovieSummary";
import { Tabs, Tab, Box, CircularProgress } from "@mui/material";
import { Review } from "../component/MovieReview";
import { MovieCasting } from "../component/MovieCasting";
import { MoviePhoto } from "../component/MoviePhoto";
export const MoviePage = () => {
  /* 해당 영화 코드의 영화의 페이지. 여러 탭으로 구성되어 있으며, 각 탭에 접근시 데이터를 가져오도록 함 */
  const [searchParams] = useSearchParams();
  const code = searchParams.get("code");
  const [movieData, setMovieData] = useState({});
  const [reviewData, setReviewData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [value, setValue] = useState(0);

  /* control tab bar */
  const handleChange = (e, newValue) => {
    setValue(newValue);
    
  };

  useEffect(() => {
    async function fetchMovie() {
      const data = await fetch(`api/movie/basic?code=${code}`); //영화 데이터 중 메인에서 필요한 것만 가져옴
      const res = await data.json();
      console.log(res);
      setMovieData(res);
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
            <BasicMovie movieData={movieData} />
            <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
              <Tabs
                value={value}
                onChange={handleChange}
                aria-label="basic tabs example"
              >
                <Tab label="주요 정보" {...a11yProps(0)} />
                <Tab label="배우/제작진" {...a11yProps(1)} />
                <Tab label="포토" {...a11yProps(2)} />
                <Tab label="동영상" {...a11yProps(3)} />
                <Tab label="평점" {...a11yProps(4)} />
                <Tab label="리뷰" {...a11yProps(5)} />
                <Tab label="명대사/연관영화" {...a11yProps(6)} />
              </Tabs>
            </Box>
            <TabPanel value={value} index={0}>
              {/* 주요 정보 */}
              <MovieSummary movieData={movieData} />
            </TabPanel>
            <TabPanel value={value} index={1}>
              {/* 배우/제작진 */}
              <MovieCasting castingData={movieData.casting_arr} />
            </TabPanel>
            <TabPanel value={value} index={2}>
              {/* 포토 */}
              <MoviePhoto photoData={movieData.photo_arr} />
            </TabPanel>
            <TabPanel value={value} index={3}>
              {/* 동영상 */}
              Item 4
            </TabPanel>
            <TabPanel value={value} index={4}>
              {/* 평점 */}
              Item 5
            </TabPanel>
            <TabPanel value={value} index={5}>
              {/* 리뷰 */}
              <Review movie_code={code} />
            </TabPanel>
            <TabPanel value={value} index={6}>
              {/* 명대사/관련영화 */}
              Item 7
            </TabPanel>
          </div>
        )
      ) : (
        <NotFound />
      )}
    </div>
  );
};
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  );
}

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}
