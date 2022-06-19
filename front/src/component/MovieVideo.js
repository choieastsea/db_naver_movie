export const MovieVideo = ({ viedeoData }) => {
  return (
    <div>
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
