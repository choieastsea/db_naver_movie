import { useSearchParams } from "react-router-dom";

export const ReviewPage = () => {
  const [searchParams] = useSearchParams();
  const movie_code = searchParams.get("code");
  const user_code = searchParams.get("user");
  const url = `https://movie.naver.com/movie/bi/mi/reviewread.naver?nid=${user_code}&code=${movie_code}&order=#tab`;
  return (
    <div>
      <iframe
        title={movie_code.concat(user_code)}
        src={url}
        width={"1000px"}
        height={"1000px"}
      />
    </div>
  );
};
