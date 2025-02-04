<script setup lang="ts">
import { ref } from 'vue';
import { useDeviceStore } from '@/stores/device';
import { Device } from '@/types/device';
import DeviceCard from '@/components/device/DeviceCard.vue';
import { useDeviceDiscovery } from '@/utils/deviceDiscovery';

const deviceStore = useDeviceStore();
const { discoveredDevices, isScanning, startDiscovery, stopDiscovery } = useDeviceDiscovery();
const showAddDialog = ref(false);
const showDiscoveryDialog = ref(false);
const newDevice = ref<Partial<Device>>({
  name: '',
  type: 'light',
  status: 'offline'
});

const handleAddDevice = () => {
  if (newDevice.value.name) {
    deviceStore.addDevice({
      id: Date.now().toString(),
      name: newDevice.value.name,
      type: newDevice.value.type as Device['type'],
      status: newDevice.value.status as Device['status'],
      group: newDevice.value.group
    });
    showAddDialog.value = false;
    newDevice.value = { name: '', type: 'light', status: 'offline' };
  }
};

const handleStartDiscovery = () => {
  showDiscoveryDialog.value = true;
  startDiscovery();
};

const handleStopDiscovery = () => {
  stopDiscovery();
  showDiscoveryDialog.value = false;
};

const handleBindDevice = (device: Device) => {
  deviceStore.addDevice(device);
  uni.showToast({
    title: '设备绑定成功',
    icon: 'success'
  });
};

const handleEditDevice = (device: Device) => {
  uni.showModal({
    title: '编辑设备',
    content: '功能开发中...',
    showCancel: false
  });
};

const handleDeleteDevice = (device: Device) => {
  uni.showModal({
    title: '删除设备',
    content: '确定要删除该设备吗？',
    success: (res) => {
      if (res.confirm) {
        deviceStore.removeDevice(device.id);
      }
    }
  });
};
</script>

<template>
  <view class="container">
    <view class="header">
      <text class="title">设备管理</text>
      <view class="header-buttons">
        <button @tap="handleStartDiscovery" type="primary" size="mini">发现设备</button>
        <button @tap="showAddDialog = true" type="primary" size="mini">手动添加</button>
      </view>
    </view>

    <view class="device-list">
      <DeviceCard
        v-for="device in deviceStore.devices"
        :key="device.id"
        :device="device"
        @edit="handleEditDevice"
        @delete="handleDeleteDevice"
      />
    </view>

    <uni-popup v-model:show="showAddDialog" type="dialog">
      <uni-popup-dialog
        mode="input"
        title="添加设备"
        placeholder="设备名称"
        :value="newDevice.name"
        @confirm="handleAddDevice"
      />
    </uni-popup>

    <uni-popup v-model:show="showDiscoveryDialog" type="dialog">
      <view class="discovery-dialog">
        <view class="discovery-header">
          <text class="discovery-title">发现设备</text>
          <text v-if="isScanning" class="discovery-status">扫描中...</text>
          <text v-else class="discovery-status">扫描完成</text>
        </view>
        <view class="discovered-devices">
          <view
            v-for="device in discoveredDevices"
            :key="device.id"
            class="discovered-device"
          >
            <text class="device-info">{{ device.name }} ({{ device.type }})</text>
            <button
              @tap="handleBindDevice(device)"
              type="primary"
              size="mini"
            >绑定</button>
          </view>
        </view>
        <button
          @tap="handleStopDiscovery"
          type="default"
          class="discovery-close"
        >关闭</button>
      </view>
    </uni-popup>
  </view>
</template>

<style>
.container {
  padding: 16px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.title {
  font-size: 20px;
  font-weight: bold;
}
.device-list {
  display: flex;
  flex-direction: column;
}

.header-buttons {
  display: flex;
  gap: 8px;
}

.discovery-dialog {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  width: 80vw;
  max-width: 600px;
}

.discovery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.discovery-title {
  font-size: 16px;
  font-weight: bold;
}

.discovery-status {
  font-size: 14px;
  color: #666;
}

.discovered-devices {
  max-height: 60vh;
  overflow-y: auto;
}

.discovered-device {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.device-info {
  font-size: 14px;
}

.discovery-close {
  margin-top: 16px;
  width: 100%;
}
</style>
