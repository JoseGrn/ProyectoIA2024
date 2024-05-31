import React, { useState } from 'react';
import { Button, Col, Container, Form, Row } from 'react-bootstrap';

const Review = () => {
  const [selectedMovie, setSelectedMovie] = useState('');
  const [rating, setRating] = useState('');
  const [review, setReview] = useState('');

  const movies = [
    { id: 1, name: 'The Shawshank Redemption' },
    { id: 2, name: 'The Godfather' },
    { id: 3, name: 'The Dark Knight' },
    // Agrega más películas según sea necesario
  ];

  const handleMovieChange = (e) => {
    setSelectedMovie(e.target.value);
  };

  const handleRatingChange = (e) => {
    setRating(e.target.value);
  };

  const handleReviewChange = (e) => {
    setReview(e.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Lógica para enviar la información del formulario
    console.log({
      movie: selectedMovie,
      rating: rating,
      review: review,
    });
    // Puedes enviar esta información a tu backend aquí
  };

  return (
    <Container>
      <Row className="justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Col xs={12} md={6} lg={4}>
          <h2 className="text-center mb-4">Valoración de Películas</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formMovieSelect">
              <Form.Label>Selecciona una Película</Form.Label>
              <Form.Control as="select" value={selectedMovie} onChange={handleMovieChange}>
                <option value="">Selecciona una película</option>
                {movies.map(movie => (
                  <option key={movie.id} value={movie.name}>{movie.name}</option>
                ))}
              </Form.Control>
            </Form.Group>

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
