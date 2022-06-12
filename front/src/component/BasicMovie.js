import { Rating, Grid } from "@mui/material";
export default function BasicMovie({ movieData }) {
  return (
    <div>
      <img src={`${movieData?.img_url}`} alt={`${movieData?.img_url}`} />
      <h1>
        {movieData.title_kor}({movieData.title_foregin},{" "}
        {movieData.release_date?.split(".")[0]})
      </h1>
      <Grid container spacing={0} justifyContent="center">
        {movieData?.score_arr?.map((e) => (
          <Grid item xs={2} key={e.id}>
            <p>{e.type}</p>
            <p>{e.score}점</p>
            <Rating
              name="read-only"
              value={e.score / 2}
              precision={0.1}
              readOnly
            />
          </Grid>
        ))}
      </Grid>
      <p>{movieData.screening}분</p>
      <p>{movieData.release_date} 개봉</p>
    </div>
  );
}
