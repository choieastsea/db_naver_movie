import { useEffect, useState } from "react";
import { Search } from "../component/Search";
import { Movie } from "../component/Movie";
export const Main = () => {
  const [movieList, setMovieList] = useState([]);
  useEffect(() => {
    async function fetchData() {
      const data = await fetch("api/getMovies");
      const res = await data.json();
      // console.log(res);
      setMovieList(res);
    }
    fetchData();
  }, []);
  return (
    <div>
      <Search />
      {/* {movieList.map((e) => (
        <div key={e.code}>
          <Movie movieData={e} onMain={true} />
        </div>
      ))} */}
    </div>
  );
};
