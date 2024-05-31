import React, { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const ReviewForm = ({ userId }) => {
  const [reviews, setReviews] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const { movie } = location.state || {};


  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/reviewbymovie')
    .then((response) => response.json)
    .then((data) => {
        console.log(data);
        setReviews(data);
    })
    .catch((err) => {
        console.log("Error API")
    });
  }, []);

  const handleRegreso = (e) => {
    e.preventDefault();
    navigate('/listaPeliculas', {state:{userId: userId}});
  };

  return (
    <div>
      <h2>{movie.titulo}</h2>
        <div>
          <h3>Historial de Reseñas</h3>
          <ul>
            {reviews.map(review => (
              <li key={review.id}>
                <strong>Valoración: {review.rating}</strong><br />
                <span>Reseña: {review.review}</span>
              </li>
            ))}
          </ul>
        </div>
      <Link to="/listaPeliculas">
        <Button onSubmit={handleRegreso} variant="secondary">Regresar</Button>
      </Link>
    </div>
  );
};

export default ReviewForm;
