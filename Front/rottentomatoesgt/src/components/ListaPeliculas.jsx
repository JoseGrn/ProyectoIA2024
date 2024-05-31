import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';
import { useLocation, useNavigate } from 'react-router-dom';

// Componente para cada fila
const ListItem = ({ data, onSelectGenerateReview, onSelectViewReview }) => {
  return (
    <tr>
      <td>{data.titulo}</td>
      <td>{data.duracion}</td>
      <td>{data.FechaEstreno}</td>
      <td>{data.Genero}</td>
      <td>
        <button onClick={() => onSelectGenerateReview(data)}>Generar Review</button>
        <button onClick={() => onSelectViewReview(data)}>Ver Review</button>
      </td>
    </tr>
  );
};

// Componente de listado
const ListaPeliculas = () => {
  const [movies, setMovies] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const { userId } = location.state || {};

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/allmovies')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        setMovies(data);
    })
    .catch((err) => {
        console.log("Error API")
    });
  }, []);

  const handleSelectGenerateReview = (movie) => {
    console.log(movie);
    navigate(`/review`, { state: { movie, userId } });
  };

  const handleSelectViewReview = (movie) => {
    console.log(movie);
    navigate(`/reviewMovie`, { state: { movie } });
    // Aquí puedes navegar a la página de "Ver Review" o realizar alguna acción específica
  };

  return (
    <Container className="mt-5">
      <h2>Listado de Películas</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Duración</th>
            <th>Fecha Estreno</th>
            <th>Género</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {movies.map((item) => (
            <ListItem
              key={item.id}
              data={item}
              onSelectGenerateReview={handleSelectGenerateReview}
              onSelectViewReview={handleSelectViewReview}
            />
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default ListaPeliculas;