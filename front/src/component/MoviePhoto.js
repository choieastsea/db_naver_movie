import { Grid } from "@mui/material";

export const MoviePhoto = ({ photoData }) => {
  return (
    <Grid container justifyContent={"center"} sx={{ marginTop: "20px" }}>
      {photoData?.map((e) => (
        <Grid xs={2} key={e.url}>
          <img src={e.url} alt={e.url} width="180px" />
        </Grid>
      ))}
    </Grid>
  );
};
