import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Game from '@/views/Game.vue';
import Result from '@/views/Result.vue';

const routes = [
   {
      path: '/',
      component: Home,
      name: 'home-page',
   },
   {
      path: '/game',
      component: Game,
      name: 'game-page',
   },
   {
      path: '/result',
      component: Result,
      name: 'result-page',
   },
];

const router = createRouter({
   history: createWebHistory(),
   routes,
});

export default router;
