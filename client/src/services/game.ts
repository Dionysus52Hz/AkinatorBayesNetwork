import axiosInstance from '@/services/axios.ts';
import { AxiosInstance } from 'axios';

class GameService {
   API: AxiosInstance;
   constructor(baseURL = '/v1/main-game') {
      this.API = axiosInstance(baseURL);
   }

   async getQuestions() {
      return (await this.API.get('/')).data;
   }
}

export default new GameService();
