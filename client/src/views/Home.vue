<template>
   <div class="game-name flex justify-center pt-6">
      <img
         src="../assets/photos/logo.png"
         alt=""
         class="object-cover h-[120px] lg:h-[200px]"
      />
   </div>
   <div class="grid grid-cols-12 grid-rows-3 px-4">
      <div
         class="akinator-photo flex justify-center row-span-full col-start-3 col-end-11"
      >
         <img
            src="../assets/photos/pose1.png"
            alt=""
            class="object-cover h-[360px] lg:h-[480px]"
         />
      </div>
      <div
         class="row-start-1 row-span-1 col-start-2 col-end-6 flex items-end lg:col-start-3 lg:col-end-6"
      >
         <Card class="bg-primary text-primary-foreground text-center">
            <CardContent class="p-4 lg:text-xl"
               >{{
                  gameLanguage == 'en'
                     ? 'Hello, I am Akinator'
                     : 'Xin chào, tui là Akinator'
               }}
            </CardContent>
         </Card>
      </div>

      <div class="row-start-2 row-span-1 col-start-9 col-end-13 lg:col-end-12">
         <Card
            class="bg-primary text-primary-foreground text-center lg:text-xl"
         >
            <CardContent class="p-4">
               {{
                  gameLanguage == 'en'
                     ? 'Think about an character from anime. I will try to guess who it is'
                     : 'Nghĩ về một nhân vật trong anime và tui sẽ đoán xem đó là ai'
               }}
            </CardContent>
         </Card>
      </div>
   </div>

   <div class="flex justify-center">
      <Button
         variant="ghost"
         class="text-4xl h-20 uppercase font-black px-10"
         :as="RouterLink"
         :to="{ name: 'game-page' }"
         >{{ gameLanguage == 'en' ? 'Play' : 'Chơi' }}</Button
      >
   </div>

   <!-- <div>
      <ul class="grid grid-cols-2 gap-y-3">
         <li
            v-for="image in images"
            class="flex"
         >
            <div>{{ image?.character }}</div>
            <div>
               <img
                  :src="image?.image_address"
                  alt=""
                  class="w-40"
               />
            </div>
         </li>
      </ul>
   </div> -->

   <!-- <form
      class="w-2/3 space-y-6"
      @submit="onSubmit"
   >
      <FormField
         v-slot="{ componentField }"
         name="character"
      >
         <FormItem>
            <FormLabel>Character</FormLabel>
            <FormControl>
               <Input
                  type="text"
                  v-bind="componentField"
               />
            </FormControl>
            <FormMessage />
         </FormItem>
      </FormField>

      <FormField
         v-slot="{ componentField }"
         name="anime_name"
      >
         <FormItem>
            <FormLabel>Anime Name</FormLabel>
            <FormControl>
               <Input
                  type="text"
                  v-bind="componentField"
               />
            </FormControl>
            <FormMessage />
         </FormItem>
      </FormField>

      <FormField
         v-slot="{ componentField }"
         name="image_address"
      >
         <FormItem>
            <FormLabel>Image Address</FormLabel>
            <FormControl>
               <Input
                  type="text"
                  v-bind="componentField"
               />
            </FormControl>
            <FormMessage />
         </FormItem>
      </FormField>
      <Button type="submit"> Submit </Button>
   </form> -->
   <Button @click="changeDatabase">Change database</Button>
</template>
<script setup lang="ts">
   import { Button } from '@/components/ui/button';
   import { Card, CardHeader, CardContent } from '@/components/ui/card';
   import { RouterLink } from 'vue-router';

   import { h, onBeforeMount, onMounted, ref } from 'vue';
   import { useForm } from 'vee-validate';
   import { toTypedSchema } from '@vee-validate/zod';
   import * as z from 'zod';

   import {
      FormControl,
      FormDescription,
      FormField,
      FormItem,
      FormLabel,
      FormMessage,
   } from '@/components/ui/form';
   import {
      Dialog,
      DialogContent,
      DialogDescription,
      DialogFooter,
      DialogHeader,
      DialogTitle,
      DialogTrigger,
   } from '@/components/ui/dialog';
   import { Input } from '@/components/ui/input';
   import { Label } from '@/components/ui/label';
   import axios from 'axios';

   const isDialogOpen = ref(false);
   const isDialog2Open = ref(false);

   const formSchema = toTypedSchema(
      z.object({
         character: z.string(),
         anime_name: z.string(),
         image_address: z.string(),
      })
   );

   const { handleSubmit } = useForm({
      validationSchema: formSchema,
   });

   const onSubmit = handleSubmit((values) => {
      // toast({
      //    title: 'You submitted the following values:',
      //    description: h(
      //       'pre',
      //       { class: 'mt-2 w-[340px] rounded-md bg-slate-950 p-4' },
      //       h('code', { class: 'text-white' }, JSON.stringify(values, null, 2))
      //    ),
      // });
      console.log(values);
      changeDatabase(values);
   });

   const changeDatabase = async (values) => {
      try {
         const res = await axios.post(
            'http://localhost:5000/change-db',
            values,
            {
               headers: {
                  'Content-Type': 'application/json',
               },
            }
         );
      } catch (error) {
         console.log(error);
      }
   };

   const images = ref([]);
   const testImage = async () => {
      try {
         const res = (await axios.get('http://localhost:5000/change-db')).data;
         images.value = res;
      } catch (error) {
         console.log(error);
      }
   };

   const gameLanguage = ref<string>('');

   onBeforeMount(() => {
      gameLanguage.value = localStorage.getItem('akinator_game_language');
   });

   onMounted(async () => {
      await testImage();
   });
</script>
<style scoped></style>
