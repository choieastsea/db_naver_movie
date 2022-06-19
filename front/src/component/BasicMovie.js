import { Rating, Grid } from "@mui/material";
export default function BasicMovie({
  movieData,
  photo_arr,
  scoreData,
  casting_arr,
}) {
  const score = [null, "네티즌", "관람객", "평론가"];
  return (
    <div>
      <img
        src={`${
          movieData?.img_url
            ? movieData.img_url
            : "https://ssl.pstatic.net/static/movie/2012/06/dft_img133x190.png"
        }`}
        alt={`${movieData?.img_url}`}
      />
      <h1>
        {movieData.title_kor}
        {movieData.title_foreign &&
          `(${movieData.title_foreign} ${!movieData.release_date ? ")" : ""}`}
        {movieData.release_date && `, ${movieData.release_date.split(".")[0]})`}
      </h1>
      <p>{movieData.current_opening === 1 && "상영중"}</p>
      <p>
        {movieData.cumulate_audience &&
          "누적 관객 " + movieData.cumulate_audience + "명"}
      </p>
      <Grid container spacing={0} justifyContent="center">
        {scoreData?.length > 0 ? (
          scoreData?.map((e) =>
            e.score !== null ? (
              <Grid item xs={2} key={e.score_id}>
                <p>
                  {score[e.type]}({e.comment_number}명 참여)
                </p>
                <p>{e.score}점</p>
                <Rating
                  name="read-only"
                  value={e.score / 2}
                  precision={0.1}
                  readOnly
                />
              </Grid>
            ) : (
              <div></div>
            )
          )
        ) : (
          <div></div>
        )}
      </Grid>
      <p>{movieData.running_time > 0 && `${movieData.running_time} 분`}</p>
      <p>{movieData.release_date && `${movieData.release_date} 개봉`}</p>
    </div>
  );
}
