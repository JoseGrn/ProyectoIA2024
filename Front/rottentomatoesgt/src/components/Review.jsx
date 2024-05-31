import React, { useState } from 'react';
import { Button, Col, Container, Form, Row } from 'react-bootstrap';
import { useLocation, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const Review = () => {
  const [rating, setRating] = useState('');
  const [review, setReview] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { movie } = location.state || {};
  const userId = Cookies.get('userId');

  const handleRatingChange = (e) => {
    setRating(e.target.value);
  };

  const handleReviewChange = (e) => {
    setReview(e.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Lógica para enviar la información del formulario
    fetch('http://127.0.0.1:5000/api/review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
        body: JSON.stringify({ 
          userid: userId,
          movieid: movie.id,
          score: rating,
          comment: review,
         }),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data.Mensaje === "Review creada correctamente")
          navigate('/listaPeliculas', {state:{userId: userId}});
        else {
          console.error('Error en la autenticación');
        }
      })
      .catch(error => console.error('Error:', error)); 
    // Puedes enviar esta información a tu backend aquí
  };

  return (
    <Container>
      <Row className="justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Col xs={12} md={6} lg={4}>
          <h2 className="text-center mb-4">Valoración de Películas</h2>
          <Form onSubmit={handleSubmit}>

            <Form.Label>{movie.titulo}</Form.Label>

            <Form.Group controlId="formRating">
              <Form.Label className="mt-3">Valoración</Form.Label>
              <Form.Control type="number" min="1" max="10" placeholder="Valoración (1-10)" value={rating} onChange={handleRatingChange} />
            </Form.Group>

            <Form.Group controlId="formReview">
              <Form.Label className="mt-3">Reseña</Form.Label>
              <Form.Control as="textarea" rows={3} placeholder="Escribe tu reseña" value={review} onChange={handleReviewChange} />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100 mt-3">
              Enviar
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Review;
