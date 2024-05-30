import React from 'react'
import { Navbar, Container, Button, Nav} from 'react-bootstrap';

const Barra = () => {
    return (
    <Navbar bg="dark" data-bs-theme="dark">
      <Container>
        <Navbar.Brand href="/home">Rotten Tomatoes GT</Navbar.Brand>
        <Nav className="me-auto">
            <Nav.Link href="/ListaPeliculas">Lista Películas</Nav.Link>
        </Nav>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
            <Button variant="info" className='me-2' href='/Login'>Inicio Sesión</Button>
            <Button variant="secondary" href='/Register'>Registro</Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    )
}

export default Barra