import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './components/Login';
import Register from './components/Register';
import Review from './components/Review';
import ListaPeliculas from './components/ListaPeliculas';
import Comentarios from './components/Comentarios';
import Barra from './components/Barra';

function App() {
  return (
    <Router>
      <div>
        <Barra />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/review" element={<Review />} />
          <Route path="/listapeliculas" element={<ListaPeliculas />} />
          <Route path="/comentarios" element={<Comentarios />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
