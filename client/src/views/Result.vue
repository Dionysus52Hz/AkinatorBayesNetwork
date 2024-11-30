<template>
   <div
      class="grid grid-cols-10 grid-rows-10 items-center justify-center min-w-full px-6"
   >
      <h1
         class="game-name col-start-4 col-end-8 row-start-1 row-end-2 text-center text-4xl font-black uppercase"
      >
         {{ gameLanguage == 'en' ? 'Result' : 'Kết quả' }}
      </h1>
      <div class="akinator-photo col-start-1 col-end-5 row-start-3 row-end-10">
         <img
            src="../assets/photos/pose5.png"
            alt=""
         />
      </div>
      <Card
         class="col-start-3 col-end-7 row-start-2 row-end-4 bg-primary text-primary-foreground text-center z-[100]"
      >
         <CardContent class="p-6">
            {{
               gameLanguage == 'en'
                  ? 'I guessed right one more time!'
                  : 'Tôi lại đoán đúng lần nữa rồi!'
            }}</CardContent
         >
      </Card>

      <Card class="w-full col-start-6 col-end-11 row-start-3 row-end-10">
         <CardContent class="text-center grid p-6">
            <p
               class="predict-character-name text-2xl text-slate-800 font-extrabold uppercase"
            >
               {{ predictedCharacter?.character }}
            </p>
            <p class="predict-character-anime text-slate-600">
               {{ predictedCharacter?.anime_name }}
            </p>
            <div
               class="predict-character-photo rounded-lg border-2 border-slate-800 overflow-hidden p-3 mt-4"
            >
               <img
                  :src="predictedCharacter?.image_address"
                  alt=""
                  class="rounded-md object-cover aspect-square object-top"
               />
            </div>
         </CardContent>
      </Card>

      <div
         class="flex col-span-full row-start-10 row-end-11 items-center justify-center gap-x-4 py-3"
      >
         <Button
            variant="secondary"
            class="row-start-10 row-end-11 col-start-4 col-end-8 text-base"
            :as="RouterLink"
            :to="{ name: 'home-page' }"
         >
            <ArrowLeftFromLine class="w-4 h-4 mr-2" />
            {{ gameLanguage == 'en' ? 'Back To Home' : 'Về trang chủ' }}
         </Button>
         <Button
            class="row-start-10 row-end-11 col-start-4 col-end-8 text-base"
            :as="RouterLink"
            :to="{ name: 'game-page' }"
         >
            <RotateCcw class="w-4 h-4 mr-2" />
            {{ gameLanguage == 'en' ? 'Play Again' : 'Chơi lại' }}
         </Button>
      </div>
   </div>
</template>
<script setup lang="ts">
   import { Button } from '@/components/ui/button';
   import { Card, CardHeader, CardContent } from '@/components/ui/card';
   import { RouterLink } from 'vue-router';
   import { onBeforeMount, ref } from 'vue';
   import { ArrowLeftFromLine, RotateCcw } from 'lucide-vue-next';

   const predictedCharacter = ref(null);
   const gameLanguage = ref<string>('');

   onBeforeMount(() => {
      predictedCharacter.value = JSON.parse(
         localStorage.getItem('predicted_character')
      );
      gameLanguage.value = localStorage.getItem('akinator_game_language');
   });
</script>
<style scoped></style>
