import { Pagination, Box } from "@mui/material";
export const Review = ({ reviewData }) => {
  const { review_list } = reviewData;
  const onPageChange = (event, page) => {
    console.log(page);
  };
  return reviewData?.length === 0 ? (
    <div>리뷰가 없습니다.</div>
  ) : (
    <div>
      <ul>
        {/* pagination needed */}
        {review_list?.map((e) => (
          <li key={e.id}>
            <p>{e.writer}</p>
            <p>{e.content}</p>
          </li>
        ))}
      </ul>
      <Pagination
        count={parseInt(review_list?.length / 10) + 1}
        size="small"
        color="primary"
        onChange={onPageChange}
        defaultPage={1}
        style={{ justifyContent: "center" }}
      />
    </div>
  );
};
