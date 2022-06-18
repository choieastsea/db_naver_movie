import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import BasicMovie from "../component/BasicMovie";
import { NotFound } from "./NotFound";
import { CircularProgress } from "@mui/material";
export const SearchResultPage = () => {
  const [searchParams] = useSearchParams();
  const userInput = searchParams.get("userInput");
  const [resultData, setResultData] = useState({});
  const [dataList, setDataList] = useState([]);

  useEffect(() => {
    async function fetchMovie() {
      console.log("fetchMovie");
      const data = await fetch(`api/search?userInput=${userInput}`);
      const res = await data.json();
      console.log(res);
      setResultData(res);
      setDataList(res.data);
    }
    fetchMovie();
  }, [userInput]);
  return resultData?.result === "success" ? (
    <div>
      {/* 정렬도 해야함!!!! */}
      {dataList.length !== 0 ? (
        <ul>
          {dataList.map((e) => (
            <div></div>
          ))}
        </ul>
      ) : (
        <p>"{userInput}"으로 시작하는 정보가 없습니다</p>
      )}
    </div>
  ) : (
    <CircularProgress />
  );
};
