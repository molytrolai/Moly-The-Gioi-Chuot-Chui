package com.mole.login
{
   import com.mole.login.net.*;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
   import flash.events.*;
   
   public class LoginServerMenu
   {
      
      private var _serverPage:LoginServerPage;
      
      private var _menu_mc:Sprite;
      
      private var _btn1:SimpleButton;
      
      private var _btn2:SimpleButton;
      
      private var _btn3:SimpleButton;
      
      private var _btn4:SimpleButton;
      
      private var _btn5:SimpleButton;
      
      private var _btn6:SimpleButton;
      
      public function LoginServerMenu(param1:Sprite, param2:LoginServerPage)
      {
         super();
         this._menu_mc = param1;
         this._btn1 = this._menu_mc["btn_0"];
         this._btn2 = this._menu_mc["btn_1"];
         this._btn3 = this._menu_mc["btn_2"];
         this._btn4 = this._menu_mc["btn_3"];
         this._btn5 = this._menu_mc["btn_4"];
         this._btn6 = this._menu_mc["btn_5"];
         this._btn1.addEventListener(MouseEvent.CLICK,this.onClick1);
         this._btn2.addEventListener(MouseEvent.CLICK,this.onClick2);
         this._btn3.addEventListener(MouseEvent.CLICK,this.onClick3);
         this._btn4.visible = false;
         this._btn5.visible = false;
         this._btn6.visible = false;
      }
      
      private function onClick1(param1:MouseEvent) : void
      {
         LoginPktParser.GetAllServers(1,100);
         StatisticsManager.send(473);
      }
      
      private function onClick2(param1:MouseEvent) : void
      {
         LoginPktParser.GetAllServers(101,200);
         StatisticsManager.send(474);
      }
      
      private function onClick3(param1:MouseEvent) : void
      {
         LoginPktParser.GetAllServers(201,300);
         StatisticsManager.send(475);
      }
      
      private function onClick4(param1:MouseEvent) : void
      {
         LoginPktParser.GetAllServers(301,400);
      }
      
      private function onClick5(param1:MouseEvent) : void
      {
         LoginPktParser.GetAllServers(401,500);
      }
      
      private function onClick6(param1:MouseEvent) : void
      {
         LoginPktParser.GetAllServers(501,600);
      }
      
      public function show() : void
      {
         this._menu_mc.visible = true;
      }
      
      public function hide() : void
      {
         this._menu_mc.visible = false;
      }
      
      public function destroy() : void
      {
         this._btn1.removeEventListener(MouseEvent.CLICK,this.onClick1);
         this._btn2.removeEventListener(MouseEvent.CLICK,this.onClick2);
         this._btn3.removeEventListener(MouseEvent.CLICK,this.onClick3);
         this._btn4.removeEventListener(MouseEvent.CLICK,this.onClick4);
         this._btn5.removeEventListener(MouseEvent.CLICK,this.onClick5);
         this._btn6.removeEventListener(MouseEvent.CLICK,this.onClick6);
      }
   }
}

