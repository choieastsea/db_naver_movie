import { useState } from "react";
import Button from "@mui/material/Button";
import {
  List,
  ListItemButton,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import ManageSearchIcon from "@mui/icons-material/ManageSearch";
import { useNavigate } from "react-router-dom";
export const Search = () => {
  /* Search Bar와 아래의 자동 완성 리스트까지 */
  const [userInput, setUserInput] = useState("");
  const [which, setWhich] = useState("영화");
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
  const handleChange = (e) => {
    setWhich(e.target.value);
  };
  return (
    <div>
      {/* <Select
        labelId="demo-simple-select-label"
        id="demo-simple-select"
        value={which}
        onChange={handleChange}
        size= "small"
      >
        <MenuItem value={"영화"}>영화 제목</MenuItem>
        <MenuItem value={"영화인"}>영화인</MenuItem>
        <MenuItem value={"장르"}>장르</MenuItem>
      </Select> */}
      <TextField
        id="outlined-basic"
        label="영화/영화인 검색"
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
      {autoFillList?.length !== 0 && <AutoFillList list={autoFillList} />}
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
        {list.map((e) =>
          e.movie_code ? (
            <li key={e.movie_code}>
              <ListItemButton href={`movie?code=${e.movie_code}`}>
                {e.title_kor}
              </ListItemButton>
            </li>
          ) : (
            <li key={e.mpeople_code}>
              <ListItemButton href={`person?code=${e.people_code}`}>
                {e.name}
              </ListItemButton>
            </li>
          )
        )}
      </List>
    </div>
  );
};
