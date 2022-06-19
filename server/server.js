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
      `select * from score where movie_code = ${code}`
    );
    let [casting_row] = await pool.query(
      `select * from movie_appearance, people, casting where movie_appearance.people_code = people.people_code and movie_appearance.movie_code = ${code} and casting.movie_code = movie_appearance.movie_code and casting.people_code = movie_appearance.people_code;`
    );
    let [photo_row] = await pool.query(
      `select * from photo where movie_code=${code}`
    );
    let [relative_row] = await pool.query(
      `select * from movie m1, relate_movie m2 where m2.movie_code = m1.movie_code and m1.movie_code = ${code}`
    );
    let [video_row] = await pool.query(
      `select * from video where movie_code=${code};`
    );
    // select * from satisfying_netizen where movie_code=192608;
    // select * from satisfying_viewer where movie_code=192608;
    // select  * from viewing_trend where movie_code=192608;
    let [netizen_sat] = await pool.query(
      `select * from satisfying_netizen where movie_code=${code};`
    );
    let [viewer_sat] = await pool.query(
      `select * from satisfying_viewer where movie_code=${code};`
    );
    let [viewing_trend] = await pool.query(
      `select * from viewing_trend where movie_code=${code};`
    );

    score_arr = [];
    for (let i = 0; i < score_row.length; i++) {
      score_arr.push(score_row[i]);
    }
    casting_arr = [];
    for (let i = 0; i < casting_row.length; i++) {
      casting_arr.push(casting_row[i]);
    }
    photo_arr = [];
    for (let i = 0; i < photo_row.length; i++) {
      photo_arr.push(photo_row[i]);
    }
    relative_arr = [];
    for (let i = 0; i < relative_row.length; i++) {
      relative_row.push(relative_row[i]);
    }
    video_arr = [];
    for (let i = 0; i < video_row.length; i++) {
      video_arr.push(video_row[i]);
    }
    row = row[0];
    return_obj = {
      movie_data: row,
      score_arr: score_arr,
      casting_arr: casting_arr,
      photo_arr: photo_arr,
      relative_arr: relative_arr,
      video_arr,
      netizen_sat: netizen_sat[0],
      viewer_sat: viewer_sat[0],
      viewing_trend: viewing_trend[0],
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
  const page = req.query.page;
  try {
    const [firstrow] = await pool.query(
      `select review_id from review where movie_code=${code} order by review_id limit 1;`
    );
    const [totalrow] = await pool.query(
      `select count(*) as cnt from review where movie_code=${code};`
    );
    const total_count = totalrow[0].cnt;
    // console.log(firstrow);
    const offset = parseInt(firstrow[0].review_id) + (page - 1) * 10 - 1;
    // console.log(offset);

    const [row] = await pool.query(
      `select * from review where movie_code=${code} and review_id > ${offset} limit 10;`
    );
    const review_list = [];
    for (let i = 0; i < row.length; i++) {
      const review = row[i];
      // console.log(review);
      review_list.push({
        review,
      });
      console.log(review_list);
    }
    res.json({ result: "success", review_list, length: total_count });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.get(`/api/movie/comment`, async (req, res) => {
  const code = req.query.code;
  const page = req.query.page;
  try {
    const [firstrow] = await pool.query(
      `select comment_id from comment where movie_code=${code} order by comment_id limit 1;`
    );
    const [totalrow] = await pool.query(
      `select count(*) as cnt from comment where movie_code=${code};`
    );
    const total_count = totalrow[0].cnt;
    // console.log(firstrow);
    const offset = parseInt(firstrow[0].comment_id) + (page - 1) * 10 - 1;
    // console.log(offset);
    const [row] = await pool.query(
      `select * from comment where movie_code=${code} and comment_id > ${offset} limit 10;`
    );
    const comment_list = [];
    for (let i = 0; i < row.length; i++) {
      const comment = row[i];
      // console.log(review);
      comment_list.push({
        comment,
      });
      // console.log(comment_list);
    }
    res.json({
      result: "success",
      comment_list,
      length: total_count,
      curpage: page,
    });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.get(`/api/movie/quotes`, async (req, res) => {
  const code = req.query.code;
  const page = req.query.page;
  try {
    const [firstrow] = await pool.query(
      `select quotes_id from quotes where movie_code=${code} order by quotes_id limit 1;`
    );
    const [totalrow] = await pool.query(
      `select count(*) as cnt from quotes where movie_code=${code};`
    );
    const total_count = totalrow[0].cnt;
    // console.log(firstrow);
    const offset = parseInt(firstrow[0].quotes_id) + (page - 1) * 10 - 1;
    // console.log(offset);
    const [row] = await pool.query(
      `select * from quotes where movie_code=${code} and quotes_id > ${offset} limit 10;`
    );
    const quotes_list = [];
    for (let i = 0; i < row.length; i++) {
      const quotes = row[i];
      // console.log(review);
      quotes_list.push({
        quotes,
      });
      // console.log(comment_list);
    }
    res.json({
      result: "success",
      quotes_list,
      length: total_count,
      curpage: page,
    });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.get("/api/start", async (req, res) => {
  const userInput = req.query.userInput;
  console.log(`${userInput}`);
  try {
    const [row1] = await pool.query(
      `select title_kor, movie_code from movie where title_kor like "${userInput}%" limit 5;`
    );
    const [row2] = await pool.query(
      `select * from people where name like "${userInput}%" limit 5;`
    );
    console.log(row1);
    res.json(row1.concat(row2));
    // const [row2] = await pool.query("select * from movie");
  } catch (e) {
    console.log(e);
    res.json({ result: "fail" });
  }
});
app.get("/api/search/movie", async (req, res) => {
  const userInput = req.query.userInput;
  const sortBy = req.query.sortby;
  const onlyRunning = req.query.onlyRunning;
  // `api/search/movie?userInput=${userInput}&sortby=${sortBy}`
  console.log(`/api/search?userInput=${userInput}`);
  try {
    let result;
    if (onlyRunning == "true") {
      console.log(
        `select * from movie where title_kor like "${userInput}%" and current_opening=${
          onlyRunning ? 1 : 0
        } order by ${sortBy};`
      );
      result = await pool.query(
        `select * from movie where title_kor like "${userInput}%" and current_opening=${
          onlyRunning ? 1 : 0
        } order by ${sortBy};`
      );
    } else {
      result = await pool.query(
        `select * from movie where title_kor like "${userInput}%" order by ${sortBy};`
      );
    }
    const [row] = result;
    // console.log(row);
    console.log({ result: "success", data: row });
    res.json({ result: "success", data: row });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail", data: e });
  }
});
app.get("/api/search/people", async (req, res) => {
  const userInput = req.query.userInput;
  console.log(`/api/search?userInput=${userInput}`);
  try {
    const [prow] = await pool.query(
      `select * from people where name like "${userInput}%";`
    );
    // console.log(row);
    // console.log({ result: "success", data: prow });
    res.json({ result: "success", data: prow });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail", data: e });
  }
});
app.get("/api/person/filmography", async (req, res) => {
  const code = req.query.code;
  try {
    const [actor_name] = await pool.query(
      `select name from people where people_code=${code};`
    );
    const [row] = await pool.query(`
    select c.casting_name, p.name, m.title_kor, m.movie_code, m.release_date, m.img_url
    from people p, casting c, movie m
    where p.people_code = c.people_code
    and m.movie_code = c.movie_code
    and p.people_code = "${code}";`);
    res.json({ result: "success", name: actor_name[0].name, data: row });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail", data: e });
  }
});
app.get("api/movie/relate", async (req, res) => {
  const code = req.query.code;
  try {
    const [movie_list] = await pool.query(
      `select r.movie_code1 from relate_movie r, movie m where m.movie_code = r.movie_code and m.movie_code =${code};`
    );
    res.json({ result: "success", movie_list, length: row.length });
  } catch (e) {
    console.log(e);
    res.json({ result: "fail", data: e });
  }
});
app.listen(3001, () => {
  console.log("server start at port 3001");
});
