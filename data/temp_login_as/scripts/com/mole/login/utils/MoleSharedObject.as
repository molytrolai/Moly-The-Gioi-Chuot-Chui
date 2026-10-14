package com.mole.login.utils
{
   import flash.events.*;
   import flash.net.*;
   import flash.utils.*;
   
   public class MoleSharedObject
   {
      
      private static var _moleSO:SharedObject;
      
      private static var _isFlush:Boolean = true;
      
      private static var _timeID:uint = 0;
      
      public function MoleSharedObject()
      {
         super();
      }
      
      public static function flush(param1:int = 0) : void
      {
         var minDiskSpace:int = param1;
         clearTimeout(_timeID);
         try
         {
            _moleSO.flush(minDiskSpace);
         }
         catch(e:Error)
         {
         }
      }
      
      public static function getMoleData(param1:uint) : SharedObject
      {
         var _loc2_:SharedObject = SharedObject.getLocal("mole/" + param1,"/");
         _loc2_.addEventListener(NetStatusEvent.NET_STATUS,onSOFail);
         _loc2_.addEventListener(AsyncErrorEvent.ASYNC_ERROR,onSOFail);
         return _loc2_;
      }
      
      private static function onSOFail(param1:Event) : void
      {
      }
   }
}

