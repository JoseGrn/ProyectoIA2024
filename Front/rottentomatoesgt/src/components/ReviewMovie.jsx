import React, { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const ReviewForm = ({ userId }) => {
  const [reviews, setReviews] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const { movie } = location.state || {};


  useEffect(() => {
    console.log(movie);
    fetch('http://127.0.0.1:5000/api/reviewbymovie', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
        body: JSON.stringify({ 
          movieid: movie.id,
         }),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data !== null)
          setReviews(data);
        else {
          console.error('Error en la autenticación');
        }
      })
      .catch(error => console.error('Error:', error));
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
              <li key={review.comment}>
                <strong>Valoración: {review.tomatometer}</strong><br />
                <span>Reseña: {review.comment}</span>
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
