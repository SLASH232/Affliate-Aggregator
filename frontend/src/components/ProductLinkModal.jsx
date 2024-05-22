import React from 'react';

const ProductLinkModal = ({ link, onClose }) => {
  return (
    <div className="modal">
      <a href={link} target="_blank" rel="noopener noreferrer">
        {link}
      </a>
      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default ProductLinkModal;