import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8080', // Replace with your backend URL
  });
  
  export default instance;