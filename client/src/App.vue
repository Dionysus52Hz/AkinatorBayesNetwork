<template>
   <main class="max-w-[1320px] mx-auto">
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
