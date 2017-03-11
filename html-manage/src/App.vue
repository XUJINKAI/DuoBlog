<template>
  <div id="app">
    <Navs></Navs>
    <router-view></router-view>
  </div>
</template>

<script>
import Navs from '@/components/Navs'
export default {
  name: 'app',
  components: {
    Navs
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 10px;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
}
</style>
