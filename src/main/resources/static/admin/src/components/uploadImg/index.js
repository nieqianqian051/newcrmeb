import Vue from "vue";
import upload from "./upload.vue";

let UploadConstructor = Vue.extend(upload);
let instance;
let zIndex = 1000;

function appendInstance() {
  let topWindow = window.top;
  let maskList = topWindow.document.querySelectorAll('.ivu-modal-mask');
  let zIndexList = [];
  for (let i = 0; i < maskList.length; i++) {
    zIndexList.push(Number(maskList[i].style.zIndex));
  }
  zIndexList.sort((a, b) => {return a - b});
  if (zIndexList.length) {
    zIndex = zIndexList[zIndexList.length - 1] + 1;
  }
  topWindow.document.body.appendChild(instance.$el);
}

function UploadImg(options) {
  instance = new UploadConstructor({
    data: options
  });
  instance.$mount();
  appendInstance();
  instance.visible = true;
  instance.zIndex = zIndex;
  return instance;
}

export default UploadImg;