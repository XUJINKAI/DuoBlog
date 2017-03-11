<template>
  <div id="app">
    <div id="header">
      <a href="javascript: window.location.reload();">Manager</a>
      <router-link to='/'>Blogs</router-link>
      <router-link to='/blog/1'>Blogs-1</router-link>
      <router-link to='/blog/1/posts'>Blogs-1-posts</router-link>
      <router-link to='/setting'>Setting</router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
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
