const express = require("express");
const mysql = require("mysql2/promise");
const app = express();
const pool = mysql.createPool({
  host: "localhost",
  user: "db_konkuk",
  database: "moviedb",
  password: "6812",
});

app.get("/", async (req, res) => {
  try {
    const [row] = await pool.query("select * from movie");
    console.log(`${row[0].title}`);
    res.send(`${row[0].title}`);
  } catch (e) {
    console.error(e);
  }
});

app.listen(3000, () => {
  console.log("start!");
});
