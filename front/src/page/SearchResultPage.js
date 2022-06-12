import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import BasicMovie from "../component/BasicMovie";
import { NotFound } from "./NotFound";
export const SearchResultPage = () => {
  const [searchParams] = useSearchParams();
  const userInput = searchParams.get("userInput");
  const [resultData, setResultData] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [dataList, setDataList] = useState([]);

  useEffect(() => {
    async function fetchMovie() {
      console.log("fetchMovie");
      const data = await fetch(`api/search?userInput=${userInput}`);
      const res = await data.json();
      console.log(res);
      setResultData(res);
      setDataList(res.data);
      setIsLoading(false);
    }
    fetchMovie();
  }, [userInput]);
  return resultData.result === "success" ? (
    dataList.map((e) => <BasicMovie movieData={e} />)
  ) : (
    <NotFound />
  );
};
