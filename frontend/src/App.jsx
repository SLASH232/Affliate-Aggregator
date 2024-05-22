import { useState, useEffect } from 'react'
import axios from "./axios"
import './App.css'
import CommissionRates from "./components/CommissionRate/CommissionRates"
import AddProduct from "./components/AddProduct"
import ProductTable from "./components/ProductTable"


function App() {

  return (
    <>
      <CommissionRates />

      <hr />
      
      
      <AddProduct />
      
      <hr />
      
      <h2>Your Affiliate Links</h2>
      <ProductTable />
    </>
  )
}

export default App
