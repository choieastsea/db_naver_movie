export const MovieVideo = ({ viedeoData }) => {
  return (
    <div>
      {viedeoData?.map((e) => (
        <div key={e.id}>
          <a href={e.video_url}>
            <img src={e.thumbnail} alt={e.thumbnail} />
          </a>
        </div>
      ))}
    </div>
  );
};
