import { Grid } from "@mui/material";
import CustomizedRating from "./StyledRating";
export const MovieTrend = ({ trendData }) => {
  const { viewer_sat, netizen_sat, viewing_trend } = trendData;
  return (
    <div>
      <Grid container justifyContent="center">
        <Grid item xs={3}>
          <p>관람객 만족도</p>
          <SatisfactionView sat={viewer_sat} />
        </Grid>
        <Grid item xs={3}>
          <p>네티즌 만족도</p>
          <SatisfactionView sat={netizen_sat} />
        </Grid>
        <Grid item xs={3}>
          <p>관람 추이</p>
          <div>
            <TrendView viewing_trend={viewing_trend} />
          </div>
        </Grid>
      </Grid>
    </div>
  );
};
const SatisfactionView = ({ sat }) => {
  return (
    <div>
      <p className="ft-sm">
        남성 : {sat.male} / 여성 : {sat.female}
      </p>
      <p className="ft-sm">(평균 만족도)</p>
      <CustomizedRating rating={(sat.male + sat.female) / 2} />
      <div
        style={{
          padding: "20px",
          backgroundColor: "#EEEEEE",
          borderRadius: "25px",
          margin: "10px",
        }}
      >
        <Grid container justifyContent={"center"} spacing={"10"}>
          <Grid item>
            <p className="ft-sm">10대</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">20대</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">30대</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">40대</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">50대</p>
          </Grid>
        </Grid>
        <Grid container justifyContent={"center"} spacing={"10"}>
          <Grid item>
            <p className="ft-sm">{sat.tenth}</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">{sat.twentieth}</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">{sat.thirtieth}</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">{sat.fortieth}</p>
          </Grid>
          <Grid item>
            <p className="ft-sm">{sat.fiftieth}</p>
          </Grid>
        </Grid>
      </div>
    </div>
  );
};
const TrendView = ({ viewing_trend }) => {
  return (
    <div>
      <br />
      <p>10대 {viewing_trend.tenth}%</p>
      <p>20대 {viewing_trend.twentieth}%</p>
      <p>30대 {viewing_trend.thirtieth}%</p>
      <p>40대 {viewing_trend.fortieth}%</p>
      <p>50대 {viewing_trend.fiftieth}%</p>
    </div>
  );
};
