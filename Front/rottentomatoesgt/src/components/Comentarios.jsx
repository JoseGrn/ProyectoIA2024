import React, { useEffect, useState } from 'react';
import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';
 
// Componente para cada fila
const ListItem = ({ data }) => {
  return (
    <tr>
      <td>{data.movie}</td>
      <td>{data.comentario}</td>
    </tr>
  );
};
 
// Componente de listado
const Comentarios = () => {
  const [coments, setComents] = useState([]);
 
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/allmovies')
    .then((response) => response.json)
    .then((data) => {
        console.log(data);
        setComents(data);
    })
    .catch((err) => {
        console.log("Error API")
    });
  }, []);
 
  return (
    <Container className="mt-5">
      <h2>Listado de Comentarios</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Pelicula</th>
            <th>Comentario</th>
          </tr>
        </thead>
        <tbody>
          {coments.map((item) => (
            <ListItem key={item.id} data={item} />
          ))}
        </tbody>
      </Table>
    </Container>
  );
};
 
export default Comentarios;