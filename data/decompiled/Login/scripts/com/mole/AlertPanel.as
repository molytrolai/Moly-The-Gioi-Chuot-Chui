package com.mole
{
   import flash.display.SimpleButton;
   import flash.display.Sprite;
   import flash.events.MouseEvent;
   import flash.text.TextField;
   
   public class AlertPanel extends Sprite
   {
      
      private var _mainUI:UI_Register_Alert_panel;
      
      private var _msgTxt:TextField;
      
      private var _applyFun:Function;
      
      private var _cancleFun:Function;
      
      private var _applyBtn:SimpleButton;
      
      private var _cancleBtn:SimpleButton;
      
      public function AlertPanel()
      {
         super();
         this._mainUI = new UI_Register_Alert_panel();
         this._msgTxt = this._mainUI.msgTxt;
         this._applyBtn = this._mainUI.applyBtn;
         this._cancleBtn = this._mainUI.cancleBtn;
         addChild(this._mainUI);
         this._applyBtn.addEventListener(MouseEvent.CLICK,this.onAppClick);
         this._cancleBtn.addEventListener(MouseEvent.CLICK,this.onCancleClick);
      }
      
      private function onCancleClick(param1:MouseEvent) : void
      {
         if(this._cancleFun != null)
         {
            this._cancleFun();
         }
      }
      
      private function onAppClick(param1:MouseEvent) : void
      {
         if(this._applyFun != null)
         {
            this._applyFun();
         }
      }
      
      public function setTxt(param1:String, param2:Function, param3:Function) : void
      {
         this._msgTxt.htmlText = param1;
         this._applyFun = param2;
         this._cancleFun = param3;
         if(param3 == null)
         {
            this._cancleBtn.visible = this._cancleBtn.enabled = false;
            this._applyBtn.x = 120;
         }
         else
         {
            this._cancleBtn.visible = this._cancleBtn.enabled = true;
            this._cancleBtn.x = 184;
            this._applyBtn.x = 58;
         }
      }
      
      public function destory() : void
      {
         this._applyBtn.addEventListener(MouseEvent.CLICK,this.onAppClick);
         this._cancleBtn.addEventListener(MouseEvent.CLICK,this.onCancleClick);
         this._applyFun = null;
         this._cancleFun = null;
         removeChild(this._mainUI);
         this._mainUI = null;
      }
   }
}

class Single
{
   
   public function Single()
   {
      super();
   }
}
