<template>
   <div
      class="grid grid-cols-10 grid-rows-5 items-center justify-center min-w-full px-4"
   >
      <h1
         class="game-name col-start-4 col-end-8 row-start-1 row-end-2 text-center"
      >
         Read Your Mind
      </h1>
      <div class="akinator-photo col-start-4 col-end-8 row-start-1 row-end-6">
         <img
            src="../assets/photos/pose1.png"
            alt=""
         />
      </div>
      <Card
         class="col-start-2 col-end-4 row-start-2 row-end-4 bg-primary text-primary-foreground text-center"
      >
         <CardContent class="p-6"
            >{{
               gameLanguage == 'en'
                  ? 'Hello, I am Akinator'
                  : 'Xin chào, tôi là Akinator'
            }}
         </CardContent>
      </Card>
      <Card
         class="col-start-8 col-end-11 row-start-3 row-end-4 bg-primary text-primary-foreground text-center"
      >
         <CardContent class="p-6">
            {{
               gameLanguage == 'en'
                  ? 'Think about an character from anime. I will try to guess who it is'
                  : 'Nghĩ về một nhân vật trong phim hoạt hình và tôi sẽ đoán xem đó là ai'
            }}
         </CardContent>
      </Card>
      <Button
         variant="ghost"
         class="row-start-5 row-end-6 col-start-4 col-end-8 text-4xl h-20 uppercase font-black"
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
