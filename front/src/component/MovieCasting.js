export const MovieCasting = ({ castingData }) => {
  return (
    <div>
      <h1>배우</h1>
      {castingData?.map((e) => (
        <div key={e.id}>
          <a href={`/person?code=${e.person_code}`}>{e.person_name}|{e.casting_name}</a>
        </div>
      ))}
    </div>
  );
};
