import { useState } from "react";
import Button from "@mui/material/Button";
import { List, ListItemButton, TextField } from "@mui/material";
import ManageSearchIcon from "@mui/icons-material/ManageSearch";
import { useNavigate } from "react-router-dom";
export const Search = () => {
  /* Search Bar와 아래의 자동 완성 리스트까지 */
  const [userInput, setUserInput] = useState("");
  const [autoFillList, setAutoFillList] = useState([
    /* 영화 최대 5개, 인물 최대 3인 정도만 받아볼까? */
  ]);
  const navigate = useNavigate();

  async function searchStartsWith(str) {
    const data = await fetch(`/api/start?userInput=${str}`);
    console.log(data);
    const res = await data.json();
    console.log(res);
    setAutoFillList(res);
  }

  const onChangeTextField = (e) => {
    const userInput = e.target.value;
    setUserInput(userInput);
    if (userInput.length > 0) {
      //한글자 바뀔때마다 db에 검색하여 autoFillList 채워야함
      searchStartsWith(userInput);
    } else {
      setAutoFillList([]);
    }
  };
  const onClickBtn = (e) => {
    if (userInput.length > 0) {
      //여기선 autofill list가 아닌, 페이지로 전환해야함...
      navigate(`/search?userInput=${userInput}`);
    }
  };
  const handleKeySubmit = (e) => {
    if (e.keyCode === 13) {
      navigate(`/search?userInput=${userInput}`);
    }
  };

  return (
    <div>
      <TextField
        id="outlined-basic"
        label="영화 검색"
        variant="outlined"
        size="small"
        style={{ width: "300px" }}
        onChange={onChangeTextField}
        onKeyDown={handleKeySubmit}
        value={userInput}
      />
      <Button
        variant="outlined"
        size="large"
        endIcon={<ManageSearchIcon />}
        onClick={onClickBtn}
      />
      <br />
      {autoFillList.length !== 0 && <AutoFillList list={autoFillList} />}
    </div>
  );
};
const AutoFillList = ({ list }) => {
  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        transform: "translate(-60%)",
        width: "300px",
        display: "inline-block",
        zIndex: "2",
        border: "0.5px solid",
        backgroundColor: "white",
        borderRadius: "5px",
      }}
    >
      <List>
        {list.map((e) => (
          <li key={e.movie_code}>
            <ListItemButton href={`movie?code=${e.movie_code}`}>
              {e.title_kor} ({e.release_date?.split(".")[0]})
            </ListItemButton>
          </li>
        ))}
      </List>
    </div>
  );
};
