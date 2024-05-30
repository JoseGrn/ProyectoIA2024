import React from 'react';
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
  const dataList = [
    { id: 1, name: 'Cars', duration: 60, year: 2010 },
    { id: 2, name: 'Los increibles 2', duration: 34, year: 2009 },
    { id: 3, name: 'Mulan', duration: 23, year: 2008 },
    { id: 4, name: 'The idea of you', duration: 45, year: 1997 },
  ];

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
          {dataList.map((item) => (
            <ListItem key={item.id} data={item} />
          ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default ListaPeliculas;