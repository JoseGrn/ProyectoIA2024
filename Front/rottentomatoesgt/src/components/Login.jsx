import React, { useState } from 'react';
import { Button, Col, Container, Form, Row } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const Login = () => {
  const [email, setEmail] = useState('');
  const [passwordW, setPassword] = useState('');
  const navigate = useNavigate();

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
  
      fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
        body: JSON.stringify({ 
          user: email,
          password: passwordW,
         }),
      })
      .then(response => response.json())
      .then(data => {
        if (data[0].id > 0)
        {
          Cookies.set('userId', data[0].id);
          navigate('/listaPeliculas', {state:{userId: data.id}});
        }
        else {
          console.error('Error en la autenticación');
        }
      })
      .catch(error => console.error('Error:', error)); 
  };

  return (
    <Container>
      <Row className="justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Col xs={12} md={6} lg={4}>
          <h2 className="text-center mb-4">Inicio de Sesión</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>Correo Electrónico</Form.Label>
              <Form.Control type="email" placeholder="ejemplo@correo.com" value={email} onChange={handleEmailChange} />
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label className='mt-3'>Contraseña</Form.Label>
              <Form.Control type="password" placeholder="Contraseña" value={passwordW} onChange={handlePasswordChange} />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100 mt-3">
              Ingresar
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Login;
