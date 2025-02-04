export interface Device {
  id: string;
  name: string;
  type: 'light' | 'ac' | 'tv' | 'curtain';
  status: 'online' | 'offline';
  group?: string;
}
