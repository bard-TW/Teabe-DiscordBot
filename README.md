# Teabe-DiscordBot

## ❗Attention

The code contains many Chinese traditions
___

## 簡介

提比可以做什麼：

### 一般項目

說話功能: 說道關鍵字，可愛的提比會回應  
隨機功能: 瑪英小屋小鬼的小遊戲  
身份組功能: 管理員設定過的話，打指令給身份組  
管理者\特殊功能: 限時訊息、偽裝提比等

### 管理者設定

基本設定: 控制推齊、回應、打招呼、進離群通知、進群密語  
進群密語: 進群用密語的方式，歡迎並提供進群需要注意的事項  
反應權限: 設定點擊反應的方式，給予身份組  
權限賦予身份組: 對應一般項目身份組功能，設定身份組可以新增刪除其他身份組  
黑名單: 需要BOT所有者驗證的功能，可以紀錄玩家發生的事情

### BOT所有者設定

模塊讀取: 程式修改不必重開提比  
提比打招呼: 教提比打招呼
提比密語: 用提比對其他人密語聊天

### 功能介紹

[介紹連結](https://docs.google.com/spreadsheets/d/1ROWePwmTVo5_G_z8aOVCyj0H1TqRqaghC20mzTccp-Y/edit?usp=sharing)

## 備註

這是單人開發專案，大部分皆是為了好玩而寫，沒時間壓力，所以開發緩慢，未來等功能基本齊了，在寫安裝教學。

### 啟動 celery 指令

celery worker -A teabe -l info
celery -A teabe beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
