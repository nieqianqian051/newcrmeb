import { defineStore } from 'pinia';
import { Device } from '@/types/device';

export const useDeviceStore = defineStore('device', {
  state: () => ({
    devices: [] as Device[],
    groups: [] as string[]
  }),
  actions: {
    addDevice(device: Device) {
      this.devices.push(device);
    },
    removeDevice(id: string) {
      this.devices = this.devices.filter(d => d.id !== id);
    },
    updateDevice(id: string, updates: Partial<Device>) {
      const device = this.devices.find(d => d.id === id);
      if (device) {
        Object.assign(device, updates);
      }
    }
  }
});
