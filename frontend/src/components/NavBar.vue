<template>
    <nav class="navbar">
        <div class="title"> <RouterLink to="/overview">價格追蹤小幫手</RouterLink></div>
        <ul v-if="menuOpen" class="options">
            <li><RouterLink to="/overview">物價概覽</RouterLink></li>
            <li><RouterLink to="/trending" >物價趨勢</RouterLink></li>
            <li><RouterLink to="/news" >相關新聞</RouterLink></li>
            <li v-if="!isLoggedIn"><RouterLink to="/login" >登入</RouterLink></li>
            <li v-else @click="logout">Hi, {{ getUserName }}! 登出</li>
        </ul>
        <button class="menu-button" @click="toggleMenu">
            <span> &#9776;</span>
        </button>
    </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'NavBar',
    data() {
    return {
            menuOpen: window.innerWidth >= 768
        }
    },
    computed: {
        isLoggedIn(){
            const userStore = useAuthStore();
            return userStore.isLoggedIn;
        },
        getUserName(){
            const userStore = useAuthStore();
            return userStore.getUserName;
        }
    },
    methods: {
        logout(){
            const userStore = useAuthStore();
            userStore.logout();
        },
        toggleMenu() {
            this.menuOpen = !this.menuOpen;   
        },
        closeMenu() {
            this.menuOpen = false;
        }
  }
};
</script>

<style scoped>
@media screen and (max-width: 768px) {
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5em;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    box-shadow: 0 0 5px #000000;
    background-color: #fff;
}

/* 漢堡按鈕固定右上 */
.menu-button {
    position: absolute;
    top: 15px;
    right: 15px;
    background: none;
    border: none;
    font-size: 2em;
    cursor: pointer;
    z-index: 2001;
}

.options {
    position: absolute;
    top: 60px;   /* 與 navbar 高度對齊 */
    left: 0;
    width: 100vw;
    list-style: none;
    padding: 0;
    margin: 0;
    background: #fff;
    z-index: 999;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.title {
  font-size: 1.4em;
  font-weight: bold;
}
.navbar li {
    width: 100%;
    padding: 15px;
    text-align: center;
    border-bottom: 1px solid #ddd;
    cursor: pointer;
}

.navbar li:hover{
    background-color: #f0f0f0;
}

.navbar a {
    text-decoration: none;
    color: #575B5D;
}

}

/* 桌面版樣式 */
@media screen and (min-width: 769px) {
.navbar {
    display: flex;
    justify-content: space-between;
    background-color: #f3f3f3;
    padding: 1.5em;
    height: 4.5em;
    width: 100%;
    align-items: center;
    box-shadow: 0 0 5px #000000;
}
.menu-button{
    display: none;
}
.navbar ul {
    list-style: none;
    display: flex;
    justify-content: space-around;
}

.title > a{
    font-size: 1.4em;
    font-weight: bold;
    color: #2c3e50 !important;
}

.navbar li {
    color: #575B5D;
    margin: 0 .5em;
    font-size: 1.2em;
}

.navbar li:hover{
    cursor: pointer;
    font-weight: bold;
}

.navbar a {
    text-decoration: none;
    color: #575B5D;
}

}

</style>

