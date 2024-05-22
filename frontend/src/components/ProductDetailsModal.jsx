import React from 'react';

const ProductDetailsModal = ({ productId, products, onClose }) => {
  const selectedProducts = products.filter((product) => product.pid === productId);

  if (!selectedProducts) {
    return null;
  }

  
  return (
    <div className="modal">
      <h2>Product Details: {selectedProducts[0].title}</h2>
      <p>{selectedProducts[0].name}</p>
      
      {Object.keys(selectedProducts).length > 0 && (
        <div>
          <ul>
            {Object.entries(selectedProducts[0]).map(([key, value]) => (
              <li >{key}: {value}</li>
            ))}
          </ul>
        </div>
      )}
      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default ProductDetailsModal;