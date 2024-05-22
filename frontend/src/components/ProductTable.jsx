import React,{useState,useEffect} from "react";
import axios from "../axios";
import ProductDetailsModal from './ProductDetailsModal';
import ProductLinkModal from './ProductLinkModal';
// import {Spinner} from 'react-spinner';
import Spinner from 'react-bootstrap/Spinner';

function ProductTable() {
    const [products, setProducts] = useState([]);
    const [selectedProductId, setSelectedProductId] = useState(null);
    const [selectedLink, setSelectedLink] = useState(null);

    const [isLoading,setIsLoading]=useState(true)

    const handleProductClick = (productId) => {
      setSelectedProductId(productId);
    };

    const handleLinkClick = (link) => {
      setSelectedLink(link);
    };

    const closeModals = () => {
      setSelectedProductId(null);
      setSelectedLink(null);
    };



    const baseURL= 'http://127.0.0.1:8080'
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await axios.get('/result');
          setProducts(response.data);
        } catch (error) {
          console.error('Error fetching products:', error);
        }
      };
      fetchData();
      setIsLoading(false)
    }, []);


  
    return (
      <div>
        
        {isLoading?(
          <div className="loader-container">
            <span>Loading...</span>
            <Spinner animation="grow" />
          </div>):(


        <table>
          <thead>
            <tr>
              <th>Product Title</th>
              <th>Status</th>
              <th>Generated Link</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr className="row"  key={product.pid}>
                <td>
                  {/* <button onClick={()=>handleProductClick(product.pid)}>
                    {product.title}
                    </button>   */}
                    {product.title}
                </td>
                <td>{product.status}</td>
                <td>
                  <div className="link-container">

                  {!selectedLink&&(<button onClick={()=>handleLinkClick(baseURL +'/my-product/'+ product.pid)}>
                    Get Link
                  </button>)}
                  {selectedLink && selectedLink === (baseURL +'/my-product/'+ product.pid) && (
                    <ProductLinkModal link={selectedLink} onClose={closeModals} />
                  )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
         )} 
        {selectedProductId&&(
          <ProductDetailsModal
          productId={selectedProductId}
          products={products}
          onClose={closeModals}/>
        )}
      </div>
    );
  }
  
  export default ProductTable;