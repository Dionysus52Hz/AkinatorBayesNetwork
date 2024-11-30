import axios from 'axios';

const config = {
   headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
   },
};

const axiosInstance = (baseURL: string) => {
   return axios.create({
      baseURL,
      ...config,
   });
};

export default axiosInstance;
