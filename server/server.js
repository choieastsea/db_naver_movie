const express = require("express");
const mysql = require("mysql2/promise");
const app = express();
const pool = mysql.createPool({
  host: "localhost",
  user: "db_konkuk",
  database: "naver_movie",
  password: "6812",
});
app.get("/api/movie/basic", async (req, res) => {
  const code = req.query.code;
  console.log(`code ${code} requested`);
  try {
    let [row] = await pool.query(
      `select * from movie where movie_code=${code}`
    );
    let [score_row] = await pool.query(
      `select * from score where movie_movie_code = ${code}`
    );
    let [casting_row] = await pool.query(
      `select * from casting, mpeoole where casting.movie_appearance_mpeoole_mpeoole_id = mpeoole.mpeople_code and movie_appearance_movie_movie_code = ${code}`
    );
    let [photo_row] = await pool.query(
      `select * from photo where movie_movie_code=${code}`
    );
    score_arr = [];
    for (let i = 0; i < score_row.length; i++) {
      score_arr.push({
        id: score_row[i].score_id,
        type: score_row[i].type,
        score: score_row[i].score,
        number: score_row[i].comment_number,
      });
    }
    casting_arr = [];
    for (let i = 0; i < casting_row.length; i++) {
      casting_arr.push({
        id: casting_row[i].casting_id,
        person_code: casting_row[i].movie_appearance_mpeoole_mpeoole_id,
        person_name: casting_row[i].name,
        casting_name: casting_row[i].casting_name,
      });
    }
    photo_arr = [];
    for (let i = 0; i < photo_row.length; i++) {
      photo_arr.push({
        id: photo_row[i].photo_id,
        url: photo_row[i].url,
      });
    }
    row = row[0];
    return_obj = {
      code: row.movie_code,
      film_rate_kor: row.film_rate_kor,
      title_kor: row.title_kor,
      title_foregin: row.title_foregin,
      making_note: row.makingnote,
      story: row.story,
      aka: row.aka,
      release_date: row.release_date,
      current_opening: row.current_opening,
      img_url: row.img_url,
      screening: row.screening,
      score_arr: score_arr,
      casting_arr: casting_arr,
      photo_arr: photo_arr,
    };
    console.log(return_obj);
    res.json(return_obj);
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.get(`/api/movie/review`, async (req, res) => {
  const code = req.query.code;
  try {
    const [row] = await pool.query(
      `select * from review where movie_movie_code=${code}`
    );
    const review_list = [];
    for (let i = 0; i < row.length; i++) {
      const review = row[i];
      // console.log(review);
      review_list.push({
        id: review.review_id,
        content: review.contents,
        title: review.title,
        view_num: review.view_num,
        good: review.good,
        date: review.date,
        writer: review.writer,
      });
      console.log(review_list);
    }
    res.json({ review_list, length: row.length });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
//in main pages...
app.get("/api/getMovies", async (req, res) => {
  try {
    const [row] = await pool.query("select * from movie");
    let arr = [];
    console.log(`data length : ${row.length}`);
    for (var i = 0; i < row.length; i++) {
      // console.log(`${row[i].title}`);
      arr.push({
        code: row[i].code,
        title_kor: row[i].title_kor,
        title_eng: row[i].title_eng,
        making_note: row[i].makingnote,
        summary: row[i].summary,
        aka: row[i].aka,
        country: row[i].country,
        release_date: row[i].releasedate,
        screening: row[i].screening,
      });
    }
    console.log(arr);
    res.json(arr);
  } catch (e) {
    console.error(e);
    res.json({ result: "fail" });
  }
});
app.get("/api/start", async (req, res) => {
  const userInput = req.query.userInput;
  console.log(`${userInput}`);
  try {
    const [row1] = await pool.query(
      `select title_kor,movie_code,release_date from movie where title_kor like "${userInput}%";`
    );
    console.log(row1);
    res.json(row1);
    // const [row2] = await pool.query("select * from movie");
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.get("/api/search", async (req, res) => {
  const userInput = req.query.userInput;
  console.log(`/api/search?userInput=${userInput}`);
  try {
    const [row] = await pool.query(
      `select * from movie where title_kor like "%${userInput}%"`
    );
    // console.log(row);
    console.log({ result: "success", data: row });
    res.json({ result: "success", data: row });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.listen(3001, () => {
  console.log("server start at port 3001");
});
