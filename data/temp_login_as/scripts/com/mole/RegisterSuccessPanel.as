package com.mole
{
   import com.adobe.images.*;
   import flash.display.*;
   import flash.events.*;
   import flash.text.TextField;
   import flash.utils.ByteArray;
   
   public class RegisterSuccessPanel extends Sprite
   {
      
      private var _mainUI:UI_Register_success_panel;
      
      private var _mimiNumTxt:TextField;
      
      private var _passwordTxt:TextField;
      
      private var _loginNowBtn:SimpleButton;
      
      private var _savePasswordBtn:SimpleButton;
      
      private var _loginNowFun:Function;
      
      private var _savePasswordFun:Function;
      
      private var _addressTxt:TextField;
      
      private var _reginfoMC:Sprite;
      
      public function RegisterSuccessPanel(param1:Function, param2:Function)
      {
         super();
         this._mainUI = new UI_Register_success_panel();
         this._reginfoMC = this._mainUI.infoMC;
         this._loginNowFun = param1;
         this._savePasswordFun = param2;
         this._mimiNumTxt = this._reginfoMC["mimiNumTxt"];
         this._passwordTxt = this._reginfoMC["passwordTxt"];
         this._loginNowBtn = this._mainUI.loginNowBtn;
         this._addressTxt = this._reginfoMC["addressTxt"];
         this._savePasswordBtn = this._mainUI.savePasswordBtn;
         this._loginNowBtn.addEventListener(MouseEvent.CLICK,this.onLoginNowClick);
         this._savePasswordBtn.addEventListener(MouseEvent.CLICK,this.onSavePasswordClick);
         addChild(this._mainUI);
      }
      
      private function onSavePasswordClick(param1:MouseEvent) : void
      {
         StatisticsManager.send(469);
         if(this._savePasswordFun != null)
         {
            this._savePasswordFun();
         }
      }
      
      private function onLoginNowClick(param1:MouseEvent) : void
      {
         StatisticsManager.send(468);
         ActivityTmpDataManager.isNewPlayer = true;
         if(this._loginNowFun != null)
         {
            this._loginNowFun(uint(this._mimiNumTxt.text),this._passwordTxt.text);
         }
      }
      
      public function setRegisterInfo(param1:int, param2:String) : void
      {
         this._mimiNumTxt.text = param1.toString();
         this._passwordTxt.text = param2;
      }
      
      public function getRegisterInfoArr() : ByteArray
      {
         this._addressTxt.text = "摩尔庄园网址： mole.61.com";
         var _loc1_:BitmapData = new BitmapData(this._reginfoMC.width,this._reginfoMC.height);
         _loc1_.draw(this._reginfoMC);
         var _loc2_:JPGEncoder = new JPGEncoder(85);
         var _loc3_:ByteArray = _loc2_.encode(_loc1_);
         this._addressTxt.text = "";
         return _loc3_;
      }
      
      public function clear() : void
      {
         this._mimiNumTxt.text = "";
         this._passwordTxt.text = "";
      }
      
      public function destory() : void
      {
         this._loginNowBtn.removeEventListener(MouseEvent.CLICK,this.onLoginNowClick);
         this._savePasswordBtn.removeEventListener(MouseEvent.CLICK,this.onSavePasswordClick);
         this._loginNowBtn = null;
         this._savePasswordBtn = null;
         removeChild(this._mainUI);
         this._mainUI = null;
      }
   }
}

