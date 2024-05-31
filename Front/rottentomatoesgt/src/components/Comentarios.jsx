import React, { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const Comentarios = () => {
  const [reviews, setReviews] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const { movie } = location.state || {};
  const userId = Cookies.get('userId');


  useEffect(() => {
    console.log(movie);
    fetch('http://127.0.0.1:5000/api/reviewbyuser', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
        body: JSON.stringify({ 
          userid: userId,
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
      <h2>Mis Comentarios</h2>
        <div>
          <h3>Historial de Reseñas</h3>
          <ul>
            {reviews.map(review => (
              <li key={review.comment}>
                <strong>Valoración: {review.tomatometer}</strong><br />
                <span>Reseña: {review.comment}</span><br />
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

export default Comentarios;
