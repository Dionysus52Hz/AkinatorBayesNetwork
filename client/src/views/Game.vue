<template>
   <!-- <Button @click="changeDatabase()">Change Database</Button> -->
   <div class="p-6">
      <Button
         variant="outline"
         :as="RouterLink"
         :to="{ name: 'home-page' }"
      >
         <ArrowLeftFromLine class="w-4 h-4 mr-2" />
         {{
            gameLanguage.value == 'en' ? 'Back To Home' : 'Về trang chủ'
         }}</Button
      >
   </div>

   <div class="grid grid-cols-2 p-6 gap-x-4 md:pt-0 md:gap-0 lg:grid-cols-5">
      <div
         class="akinator-photo grid place-content-center p-4 lg:col-start-1 lg:col-end-3"
      >
         <div v-show="predictCharacterIsShown == false">
            <img
               :src="akinatorPosePhoto"
               alt=""
               class="object-contain"
            />
         </div>
         <div v-show="predictCharacterIsShown == true">
            <img
               src="../assets/photos/pose4.png"
               alt=""
            />
         </div>
      </div>

      <div class="flex items-center lg:col-start-3 lg:col-end-6">
         <Card
            v-show="predictCharacterIsShown == false"
            class="w-full"
         >
            <CardHeader class="flex-column p-0 mb-4 lg:mb-6 border-b">
               <!-- Skeleton here -->
               <div
                  v-show="questionSkeletionIsShown == true"
                  class="flex items-center justify-stretch space-x-4 p-4"
               >
                  <Skeleton
                     class="h-20 lg:h-[120px] w-20 lg:w-[120px] rounded-lg bg-slate-200"
                  />
                  <Skeleton class="h-12 lg:h-[80px] grow bg-slate-200" />
               </div>

               <div
                  v-show="questionSkeletionIsShown == false"
                  class="flex"
               >
                  <div
                     class="flex question-number p-7 lg:p-10 bg-primary text-primary-foreground items-center justify-center"
                  >
                     <p class="text-2xl font-bold">
                        {{ questionNumber }}
                     </p>
                  </div>
                  <CardTitle class="p-4 text-lg lg:text-xl">
                     {{ questionContent }}</CardTitle
                  >
               </div>
            </CardHeader>
            <CardContent class="grid p-4 lg:p-6 pt-0 lg:pt-0 gap-y-4">
               <RadioGroup
                  default-value="comfortable"
                  class="lg:gap-y-6"
               >
                  <div
                     class="flex items-center"
                     v-for="choice in choices"
                  >
                     <RadioGroupItem
                        :id="choice.id"
                        :value="choice.value.toString()"
                        class="hidden peer"
                     />
                     <Label
                        class="cursor-pointer flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground w-full peer-data-[state=checked]:border-primary [&:has([data-state=checked])]:border-primary"
                        :for="choice.id"
                        @click="
                           sendEvidence({
                              attribute: question.attribute,
                              answer: choice.value,
                           })
                        "
                        >{{
                           gameLanguage === 'en'
                              ? choice.label_en
                              : choice.label_vi
                        }}</Label
                     >
                  </div>
               </RadioGroup>
            </CardContent>
         </Card>

         <Card
            v-show="predictCharacterIsShown == true"
            class="w-full"
         >
            <CardHeader class="bg-primary">
               <CardTitle class="text-center text-primary-foreground"
                  >Tôi đoán là</CardTitle
               >
            </CardHeader>

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
                  class="predict-character-photo rounded-lg border-2 border-slate-800 overflow-hidden mt-4 flex justify-center p-3"
               >
                  <img
                     :src="predictedCharacter?.image_address"
                     alt=""
                     class="rounded-md object-cover aspect-square object-top max-h-[480px]"
                  />
               </div>
            </CardContent>

            <CardFooter>
               <div class="w-full grid grid-flow-col justify-stretch gap-x-4">
                  <Button
                     variant="secondary"
                     class="text-base"
                     @click="continueGame"
                  >
                     <Annoyed class="w-5 h-5 mr-2"></Annoyed>
                     Tạch rồi
                  </Button>
                  <Button
                     class="text-base"
                     @click="directToResultPage"
                     :as="RouterLink"
                     :to="{ name: 'result-page' }"
                  >
                     <PartyPopper class="w-5 h-5 mr-2"></PartyPopper>
                     Đúng zị
                  </Button>
               </div>
            </CardFooter>
         </Card>
      </div>
   </div>
</template>
<script setup lang="ts">
   import {
      Card,
      CardContent,
      CardHeader,
      CardTitle,
   } from '@/components/ui/card';
   import { Skeleton } from '@/components/ui/skeleton';
   import { Button } from '@/components/ui/button';
   import { Label } from '@/components/ui/label';
   import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
   import axios from 'axios';
   import { onMounted, ref, onBeforeMount, watch } from 'vue';
   import CardFooter from '@/components/ui/card/CardFooter.vue';
   import { Annoyed, PartyPopper, ArrowLeftFromLine } from 'lucide-vue-next';
   import { RouterLink, useRouter } from 'vue-router';

   type Question = {
      attribute: string;
      question_en: string;
      question_vi: string;
   };

   type Evidence = {
      attribute: string;
      answer: number;
   };

   const choices: {
      id: string;
      value: number;
      label_en: string;
      label_vi: string;
   }[] = [
      {
         id: 'yes',
         value: 1,
         label_en: 'Yes',
         label_vi: 'Có',
      },
      {
         id: 'no',
         value: 0,
         label_en: 'No',
         label_vi: 'Không',
      },

      {
         id: 'dont-know',
         value: 0.5,
         label_en: "Don't Know",
         label_vi: 'Không biết',
      },
   ];

   const question = ref<Question>({
      attribute: '',
      question_en: '',
      question_vi: '',
   });
   const questionContent = ref<string>('');
   const answer = ref<Number>();
   const predictedCharacter = ref(null);
   const gameLanguage = ref('vi');
   const questionNumber = ref(0);
   const akinatorPosePhoto = ref<string>('');
   const questionSkeletionIsShown = ref(false);
   const predictCharacterIsShown = ref(false);
   const isMaxQuestion = ref(false);
   const router = useRouter();

   const renderQuestion = (question: Question) => {
      if (question != null) {
         if (gameLanguage.value === 'en') {
            questionContent.value = question.question_en;
         } else if (gameLanguage.value === 'vi') {
            questionContent.value = question.question_vi;
         }
      }
   };

   const renderAkinatorPosePhoto = () => {
      if (questionNumber.value % 2 != 0) {
         let i = ((questionNumber.value + 1) / 2) % 6;
         if (i == 0) {
            i = 1;
         }
         akinatorPosePhoto.value = `/src/assets/photos/pose${i}.png`;
      }
   };

   const continueGame = () => {
      if (localStorage.getItem('is_max_question') !== null) {
         isMaxQuestion.value = JSON.parse(
            localStorage.getItem('is_max_question')
         );
      }

      if (isMaxQuestion.value === false) {
         predictCharacterIsShown.value = false;
         predictedCharacter.value = null;
      } else {
         predictCharacterIsShown.value = true;
         router.push({
            name: 'result-page',
         });
      }
   };

   const mainGamePathOnServer = 'http://localhost:5000/main-game';

   const getFirstQuestion = () => {
      questionSkeletionIsShown.value = true;
      questionNumber.value++;
      renderAkinatorPosePhoto();
      axios
         .get(mainGamePathOnServer)
         .then((res) => {
            question.value = res.data.first_question;
            renderQuestion(question.value);
            questionSkeletionIsShown.value = false;
         })
         .catch((error) => {
            console.log(error);
         });
   };

   const sendEvidence = async (evidence: Evidence) => {
      try {
         console.log(evidence);

         questionNumber.value++;
         renderAkinatorPosePhoto();
         questionSkeletionIsShown.value = true;

         const res = await axios.post(mainGamePathOnServer, evidence, {
            headers: {
               'Content-Type': 'application/json',
            },
         });

         console.log(res);
         question.value = res.data?.next_question;
         renderQuestion(res.data?.next_question);
         questionSkeletionIsShown.value = false;

         if (res.data?.max_question !== null) {
            localStorage.setItem('is_max_question', res.data?.max_question);
         }

         if (res.data?.predict_character_result !== null) {
            predictedCharacter.value = JSON.parse(
               res.data?.predict_character_result
            )[0];

            localStorage.setItem(
               'predicted_character',
               JSON.stringify(predictedCharacter.value)
            );
         } else predictedCharacter.value = res.data?.predict_character_result;
      } catch (error) {
         console.log(error);
      }
   };

   // const changeDatabase = () => {
   //    axios
   //       .get('http://localhost:5000/change-db')
   //       .then((res) => {
   //          console.log(res);
   //       })
   //       .catch((error) => {
   //          console.log(error);
   //       });
   // };

   const directToResultPage = () => {
      console.log(predictedCharacter.value);
   };

   watch(predictedCharacter, (newValue, oldValue) => {
      try {
         console.log(newValue);
         if (newValue !== null) {
            console.log('I guess that is ', newValue);
            predictCharacterIsShown.value = true;
         }
      } catch (error) {
         console.log(error);
      }
   });

   onBeforeMount(() => {
      getFirstQuestion();
   });
</script>
<style scoped></style>
