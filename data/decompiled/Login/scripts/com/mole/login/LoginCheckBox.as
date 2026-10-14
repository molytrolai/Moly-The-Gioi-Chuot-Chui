package com.mole.login
{
   import flash.display.MovieClip;
   import flash.events.*;
   
   public class LoginCheckBox extends EventDispatcher
   {
      
      public static const STATE_CHANGE:String = "LoginCheckBox_StateChange";
      
      private var _checkBox:MovieClip;
      
      public function LoginCheckBox(param1:MovieClip)
      {
         super();
         this._checkBox = param1;
         this._checkBox.buttonMode = true;
         this._checkBox.mouseChildren = false;
         this._checkBox.gotoAndStop(1);
         this._checkBox.addEventListener(MouseEvent.CLICK,this.onChangeState);
      }
      
      private function onChangeState(param1:MouseEvent) : void
      {
         this.selected = !this.selected;
         StatisticsManager.send(460);
      }
      
      public function get selected() : Boolean
      {
         return this._checkBox.currentFrame == 2;
      }
      
      public function set selected(param1:Boolean) : void
      {
         if(param1)
         {
            this._checkBox.gotoAndStop(2);
         }
         else
         {
            this._checkBox.gotoAndStop(1);
         }
         dispatchEvent(new EventTaomee(STATE_CHANGE,this.selected));
      }
      
      public function setState(param1:Boolean) : void
      {
         if(param1)
         {
            this._checkBox.gotoAndStop(2);
         }
         else
         {
            this._checkBox.gotoAndStop(1);
         }
      }
      
      public function destroy() : void
      {
         this._checkBox.addEventListener(MouseEvent.CLICK,this.onChangeState);
      }
   }
}

