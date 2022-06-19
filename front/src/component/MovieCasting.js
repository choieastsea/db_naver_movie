import {
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Grid,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

export const MovieCasting = ({ castingData }) => {
  const navigate = useNavigate();
  const toFilmPage = (code) => {
    navigate(`/person?code=${code}`);
  };
  return (
    <div>
      <h1>배우</h1>
      <Grid container spacing={3} justifyContent="center">
        {castingData?.map(
          (e) =>
            e.casting_name === "감독" && (
              <Grid item xs={2}>
                <Card>
                  <CardActionArea onClick={() => toFilmPage(e.people_code)}>
                    <CardContent>
                      <Typography
                        sx={{ fontSize: 15 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.name}
                      </Typography>
                      <Typography
                        sx={{ fontSize: 12 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.casting_name === null ? "" : `(${e.casting_name})`}
                      </Typography>
                      <Typography
                        sx={{ fontSize: 12 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.role}
                      </Typography>
                      <CardMedia
                        component="img"
                        image={`${e.thumbnail}`}
                        alt={`${e.thumbnail}`}
                      />
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            )
        )}
        {castingData?.map((e) =>
          e.thumbnail ? (
            e.casting_name !== "감독" && (
              <Grid item xs={2}>
                <Card >
                  <CardActionArea onClick={() => toFilmPage(e.people_code)}>
                    <CardContent>
                      <Typography
                        sx={{ fontSize: 15 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.name}
                      </Typography>
                      <Typography
                        sx={{ fontSize: 12 }}
                        color="text.secondary"
                        gutterBottom
                      ></Typography>
                      <Typography
                        sx={{ fontSize: 12 }}
                        color="text.secondary"
                        gutterBottom
                      >
                        {e.role}
                      </Typography>
                      <CardMedia
                        component="img"
                        image={`${e.thumbnail}`}
                        alt={`${e.thumbnail}`}
                      />
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            )
          ) : (
            <Grid item xs={2}>
              <p>
                {e.name} {e.casting_name === null ? "" : `(${e.casting_name})`}
              </p>
              <p>{e.role}</p>
            </Grid>
          )
        )}
      </Grid>
    </div>
  );
};
