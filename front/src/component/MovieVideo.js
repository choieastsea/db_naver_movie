export const MovieVideo = ({ viedeoData }) => {
  return (
    <div>
      <p>(클릭시 동영상 링크로 연결됩니다.)</p>
      {viedeoData?.map((e) => (
        <div key={e.video_id}>
          <p>{e.title}</p>
          <a href={`https://${e.video_url}`}>
            <img src={e.thumbnail_url} alt={e.thumbnail_url} />
          </a>
        </div>
      ))}
    </div>
  );
};
