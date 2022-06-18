import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Main } from "../page/MainPage";
import { MoviePage } from "../page/MoviePage";
import { PersonPage } from "../page/PersonPage";
import { NotFound } from "../page/NotFound";
import { SearchResultPage } from "../page/SearchResultPage";
import { Header } from "./Header";
import { ReviewPage } from "../page/ReviewPage";
function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Header>KU movie</Header>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/search" element={<SearchResultPage />} />
          <Route path="/movie/review" element={<ReviewPage />} />
          <Route path="/movie" element={<MoviePage />} />
          <Route path="/person" element={<PersonPage />} />
          <Route path="/*" element={<NotFound />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
