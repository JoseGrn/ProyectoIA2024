import React, { useState } from 'react';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import SplitButton from 'react-bootstrap/SplitButton';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

const Review = () => {
  const [selectedItem, setSelectedItem] = useState(null);
  const [selectedItemName, setSelectedItemName] = useState("");
  const [formData, setFormData] = useState({
    addValoracion: '',
    addReview: '', 
  });

  const handleSelect = (eventKey, event) => {
    const key = parseInt(eventKey, 10);
    setSelectedItem(key === 0 ? null : key);
    setSelectedItemName(event.target.innerText); // Obtener el nombre de la opción seleccionada
    if(key === 0){
      setFormData({ addValoracion: '', addReview: ''});
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Datos ingresado:', {selectedItemName, ...formData});
  };



  return (
    <div className='Review'>
        <h1>Registro de Valoración y Review de Películas</h1>
       <div className="mb-2">
        {[SplitButton].map((DropdownType, idx) => (
          <DropdownType
            as={ButtonGroup}
            key={idx}
            id={`dropdown-button-drop-${idx}`}
            size="lg"
            title={"Selecciona una película"} // Mostrar el nombre de la opción seleccionada
            onSelect={handleSelect}>
            <Dropdown.Item eventKey="0">Ninguno</Dropdown.Item>
            <Dropdown.Item eventKey="1">Los Increíbles 2</Dropdown.Item>
            <Dropdown.Item eventKey="2">Cars</Dropdown.Item>
            <Dropdown.Item eventKey="3">Mulan</Dropdown.Item>
          </DropdownType>
        ))}
        
        {selectedItem !== null && (
        <Form className="mt-3" onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicText">
            <Form.Label>Opción Seleccionada</Form.Label>
            <Form.Control
              type="text"
              placeholder="Selected option will appear here"
              value={`${selectedItemName}`}
              readOnly
            />
          </Form.Group>
          
          {(selectedItem !== 0 ) && (
            <Form.Group controlId="formDatos">
              <Form.Label>Valoración: </Form.Label>
              <Form.Control
                type="text"
                placeholder="ingresa el valor"
                name="addValoracion"
                value={formData.addValoracion}
                onChange={handleChange}
              />
              <Form.Label>Review: </Form.Label>
              <Form.Control
                type="text"
                placeholder="ingresa el valor"
                name="addReview"
                value={formData.addReview}
                onChange={handleChange}
              />
            </Form.Group>)}
          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
        )}
      </div>
    </div>
  )
}

export default Review