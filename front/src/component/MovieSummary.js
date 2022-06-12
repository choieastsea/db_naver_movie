import { Button } from "@mui/material";
import { useEffect, useState } from "react";

export default function MovieSummary({ movieData }) {
  const [buttonText, setButtonText] = useState("제작노트 보기");
  const [showMakingNote, setShowMakingNote] = useState(false);
  const handleOnClick = (e) => {
    setShowMakingNote((showMakingNote) => !showMakingNote);
  };
  useEffect(() => {
    setButtonText(showMakingNote ? "제작노트 접기" : "제작노트 보기");
  }, [showMakingNote]);

  return (
    <div>
      <h2>줄거리</h2>
      <p>{movieData.story}</p>
      {movieData?.making_note && (
        <Button onClick={handleOnClick}>{buttonText}</Button>
      )}
      {showMakingNote && <p>{movieData.making_note}</p>}
    </div>
  );
}
