import React,{useState,useEffect} from "react";
import axios from "../../axios";
import './CommissionRate.css'
import Spinner from 'react-bootstrap/Spinner';




const CommissionRates= ()=>{
    const [productLink,setProductLink]=useState("");
    const [commissionRates,setCommssionRates]=useState([]);
    const [isLoading,setLoader]=useState(false);

    const handleSubmit= async(e)=>{
        e.preventDefault();
        setLoader(true)
        try{
           const respone=await axios.post('/get_commission_rates',{"productLink":productLink});
           setCommssionRates(respone.data);     
        }
        catch (error) {
            console.error('Error fetching commission rates:', error);
          }
        setLoader(false)

    };
    return (
        <div className="container">

          <h2 className="title">Know Your Affiliate Commissions</h2>
          <form className="form" onSubmit={handleSubmit}>
            <input className="input" type="text" placeholder="Enter Product Link" value={productLink} onChange={(e) => setProductLink(e.target.value)} />
            {
          isLoading?(
            <span >Loading...</span>):
          (<button className="button" type="submit">Get Commission Rates</button>)
        }
          </form>
          <div className="card-container">
            {Object.entries(commissionRates).map(([site,rate],index) => (
              <div className="card"key={index}>
                <h3 className="card-title">{site}</h3>
                <p className="rate">{rate}%</p>
              </div>
            ))}
          </div>
        </div>
      );

}
export default CommissionRates;
