<template>
  <MainLayout>
    <template #header-right>
      <AuthHeader />
    </template>
    <router-view />
  </MainLayout>
</template>

<script setup>
import AuthHeader from './components/AuthHeader.vue'
import MainLayout from './layouts/MainLayout.vue'
</script>
