import React,{useState,useEffect}  from "react";
import axios from "../axios";

const AddProduct=()=>{
    const [productTitle, setProductTitle] = useState('');
    const [amazon_url, setAmazonURL] = useState('');
    const [flipkart_url, setFlipkartURL] = useState('');
    const [keyword, setKeyword] = useState('');
    const [isLoading,setLoader]=useState(false);
    const [errors, setErrors] = useState(''); // State for error messages

    const validateForm = () => {
      let newErrors = ''; 
    
      if (productTitle.trim() === ""||amazon_url.trim() === ""||flipkart_url.trim() === ""||keyword.trim() === "") {
        newErrors= "Fields cannot be empty";
      }
    
      setErrors(newErrors); 
      return newErrors === '';
    };
    const handleSubmit=async (e)=>{
        e.preventDefault();
        if(validateForm()){
        setLoader(true)
        try{

            const respone=await axios.post('/create_link',{"title":productTitle,"amazon_url":amazon_url,"flipkart_url":flipkart_url,"keyword":keyword}); 
         }
         catch (error) {
             console.error('Error fetching commission rates:', error);
           }
           setLoader(false)
        }
    };

    return (
    <div>
        <h2 className="title">Add Your Affiliate Links</h2>
        <form onSubmit={handleSubmit}>
            <input type="text" value={productTitle} onChange={(e) => setProductTitle(e.target.value)} placeholder="Product Title" />
            <input type="text" value={amazon_url} onChange={(e) => setAmazonURL(e.target.value)} placeholder="Amazon URL" />
            <input type="text" value={flipkart_url} onChange={(e) => setFlipkartURL(e.target.value)} placeholder="Flipkart URL" />
            <input type="text" value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="keyword" />
            {isLoading?(
            <span >Generating...</span>):
            (<button type="submit">Create Link</button>)
            }
        </form>
        {errors!=''&&(<span className="error">*{errors}</span>)}
        </div>
)
};

export default AddProduct