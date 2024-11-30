<template>
   <!-- <nav>
      <NavigationMenu>
         <NavigationMenuList>
            <NavigationMenuItem>
               <NavigationMenuLink
                  :class="navigationMenuTriggerStyle()"
                  :as="RouterLink"
                  :to="{ name: 'home-page' }"
               >
                  Home
               </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
               <NavigationMenuLink
                  :class="navigationMenuTriggerStyle()"
                  :as="RouterLink"
                  :to="{ name: 'game-page' }"
                  >Game</NavigationMenuLink
               >
            </NavigationMenuItem>

            <NavigationMenuItem>
               <NavigationMenuLink
                  :class="navigationMenuTriggerStyle()"
                  :as="RouterLink"
                  :to="{ name: 'result-page' }"
                  >Result</NavigationMenuLink
               >
            </NavigationMenuItem>
         </NavigationMenuList>
      </NavigationMenu>
   </nav> -->
   <main>
      <router-view></router-view>
   </main>
</template>
<script setup lang="ts">
   import {
      NavigationMenu,
      NavigationMenuContent,
      NavigationMenuItem,
      NavigationMenuLink,
      NavigationMenuList,
      NavigationMenuTrigger,
      navigationMenuTriggerStyle,
   } from '@/components/ui/navigation-menu';
   import { RouterLink } from 'vue-router';
</script>

<style scoped></style>
