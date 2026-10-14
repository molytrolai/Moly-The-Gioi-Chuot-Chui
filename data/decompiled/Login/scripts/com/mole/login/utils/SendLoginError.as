package com.mole.login.utils
{
   import flash.events.*;
   import flash.net.*;
   
   public class SendLoginError
   {
      
      private var _msg:String;
      
      private const URL_LIST:Array = ["login.mole.61.com","123.150.163.99","125.39.236.145"];
      
      private var _sendIdx:uint;
      
      public function SendLoginError(param1:String)
      {
         super();
         this.createLoader(this.URL_LIST[0],param1);
      }
      
      private function createLoader(param1:String, param2:String) : void
      {
         this._msg = param2;
         var _loc3_:URLLoader = new URLLoader();
         _loc3_.addEventListener(Event.COMPLETE,this.onLoaderComplete);
         _loc3_.addEventListener(IOErrorEvent.IO_ERROR,this.onSendError);
         _loc3_.addEventListener(SecurityErrorEvent.SECURITY_ERROR,this.onSendError);
         var _loc4_:URLRequest = new URLRequest("http://" + param1 + "/client?" + param2);
         _loc4_.method = URLRequestMethod.GET;
         _loc3_.load(_loc4_);
      }
      
      private function onLoaderComplete(param1:Event) : void
      {
         this.removeLoaderEvent(param1.currentTarget as URLLoader);
      }
      
      private function onSendError(param1:Event) : void
      {
         if(this._sendIdx <= 2)
         {
            ++this._sendIdx;
            this.createLoader(this.URL_LIST[this._sendIdx],this._msg);
         }
         this.removeLoaderEvent(param1.currentTarget as URLLoader);
      }
      
      private function removeLoaderEvent(param1:URLLoader) : void
      {
         if(param1)
         {
            param1.removeEventListener(Event.COMPLETE,this.onLoaderComplete);
            param1.removeEventListener(IOErrorEvent.IO_ERROR,this.onSendError);
            param1.removeEventListener(SecurityErrorEvent.SECURITY_ERROR,this.onSendError);
         }
      }
   }
}

