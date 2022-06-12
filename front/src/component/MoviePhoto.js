export const MoviePhoto = ({ photoData }) => {
  return (
    <div>
      {photoData?.map((e) => (
        <div key={e.id}>
          <img src={e.url} alt={e.url} />
        </div>
      ))}
    </div>
  );
};
