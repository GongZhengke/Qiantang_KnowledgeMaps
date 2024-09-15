<template>
    <div class="header">
      <a-space :size="12" direction="vertical" align="center">
        <a-avatar :style="{ backgroundColor: '#14a9f8' }" :size="64">{{username[0]}}</a-avatar>
        <a-typography-title :heading="6" style="margin: 0">
          {{username}}
        </a-typography-title>
        <div class="user-msg">
          <a-space :size="18">
            <div>
              <icon-user />
              <a-typography-text>ID: {{userid}}</a-typography-text>
            </div>
            <div>
              <icon-home />
              <a-typography-text v-if="staff == 1">
                系统管理员
              </a-typography-text>
              <a-typography-text  v-else>
                普通用户
              </a-typography-text>
            </div>
            <div>
              <icon-location />
              <a-typography-text>{{phone}}</a-typography-text>
            </div>
          </a-space>
        </div>
      </a-space>
    </div>
  </template>
  <script>

 import { IconCamera , IconUser , IconHome , IconLocation } from '@arco-design/web-vue/es/icon';

export default {
  setup() {

    return {
    }
  },
  name: 'HomeView',
  data() {
    return {
      
    }
  },
  components: {
    IconCamera,
    IconUser,
    IconHome,
    IconLocation
  },
  props:['username','userid','email','staff','phone']
}

</script>
  
  <style scoped>
    .header {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 204px;
      color: var(--gray-10);
      background: url(//p3-armor.byteimg.com/tos-cn-i-49unhts6dw/41c6b125cc2e27021bf7fcc9a9b1897c.svg~tplv-49unhts6dw-image.image)
        no-repeat;
      background-size: cover;
      border-radius: 4px;
      margin-bottom:10px;

    }
  
    .header :deep(.arco-avatar-trigger-icon-button) {
        color: rgb(var(--arcoblue-3));
  
      }

      .header :deep(.arco-avatar-trigger-icon-button) :deep(.arco-icon) {
          vertical-align: -1px;
        }
    .header .user-msg .arco-typography {
        margin-left: 6px;
      }
      .header .user-msg .arco-icon {
          color: rgb(var(--gray-10));
        }
  </style>