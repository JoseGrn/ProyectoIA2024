import React, { useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [nameR, setName] = useState('');
  const [lastnameR, setLastName] = useState('');
  const [emailR, setEmail] = useState('');
  const [passwordR, setPassword] = useState('');
  const navigate = useNavigate();

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleLastNameChange = (e) => {
    setLastName(e.target.value);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:5000/api/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
      body: JSON.stringify({ 
        name: nameR,
        lastname: lastnameR,
        user: emailR,
        password: passwordR,
        level: 3,
       }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      if (data.Mensaje === "Usuario creado correctamente")
        navigate('/login');
      else {
        console.error('Error en el registro');
      }
    })
    .catch(error => console.error('Error:', error)); 
  };

  return (
    <Container>
      <Row className="justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Col xs={12} md={6} lg={4}>
          <h2 className="text-center mb-4">Registro</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicFullName" className='mt-3'>
              <Form.Label>Nombre</Form.Label>
              <Form.Control type="text" placeholder="Nombres" value={nameR} onChange={handleNameChange} />
            </Form.Group>

            <Form.Group controlId="formBasicFullName" className='mt-3'>
              <Form.Label>Apellidos</Form.Label>
              <Form.Control type="text" placeholder="Apellidos" value={lastnameR} onChange={handleLastNameChange} />
            </Form.Group>

            <Form.Group controlId="formBasicEmail" className='mt-3'>
              <Form.Label>Correo Electrónico</Form.Label>
              <Form.Control type="email" placeholder="ejemplo@correo.com" value={emailR} onChange={handleEmailChange} />
            </Form.Group>

            <Form.Group controlId="formBasicPassword" className='mt-3'>
              <Form.Label>Contraseña</Form.Label>
              <Form.Control type="password" placeholder="Contraseña" value={passwordR} onChange={handlePasswordChange} />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100 mt-3">
              Registrar
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Register;
