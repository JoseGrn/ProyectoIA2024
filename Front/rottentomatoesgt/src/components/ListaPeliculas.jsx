import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';

// Componente para cada fila
const ListItem = ({ data }) => {
  return (
    <tr>
      <td>{data.id}</td>
      <td>{data.name}</td>
      <td>{data.duration}</td>
      <td>{data.year}</td>
    </tr>
  );
};

// Componente de listado
const ListaPeliculas = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/allmovies')
    .then((response) => response.json)
    .then((data) => {
        console.log(data);
        setMovies(data);
    })
    .catch((err) => {
        console.log("Error API")
    });
  }, []);

  return (
    <Container className="mt-5">
      <h2>Listado de Películas</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Duracion</th>
            <th>Año</th>
          </tr>
        </thead>
        <tbody>
          {movies.map((item) => (
            <ListItem key={item.id} data={item} />
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default ListaPeliculas;