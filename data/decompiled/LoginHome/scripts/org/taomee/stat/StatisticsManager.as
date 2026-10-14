package org.taomee.stat
{
   import flash.events.Event;
   import flash.events.IOErrorEvent;
   import flash.events.SecurityErrorEvent;
   import flash.net.URLLoader;
   import flash.net.URLRequest;
   
   public class StatisticsManager
   {
      
      private static const dirtyKeyList:Array = ["=",":",",",";",".","|","\t","&"];
      
      private static var _gameId:int = 0;
      
      private static var _enabled:Boolean = true;
      
      public function StatisticsManager()
      {
         super();
      }
      
      public static function setup(param1:int) : void
      {
         _gameId = param1;
      }
      
      public static function setEnabled(param1:Boolean) : void
      {
         _enabled = param1;
      }
      
      public static function sendHttpStat(param1:String, param2:String, param3:String = null, param4:int = 0) : String
      {
         var _loc8_:String = null;
         var _loc5_:String = encodeURI(replaceKey(param1));
         var _loc6_:String = encodeURI(replaceKey(param2));
         var _loc7_:String = "http://newmisc.taomee.com/misc.js?gameid=" + _gameId + "&stid=" + _loc5_ + "&sstid=" + _loc6_;
         if(param4)
         {
            _loc7_ += "&uid=" + param4;
         }
         if(param3)
         {
            _loc8_ = encodeURI(replaceKey(param3));
            _loc7_ += "&item=" + _loc8_ + "&itemlen=" + _loc8_.length;
         }
         _loc7_ += "&stidlen=" + _loc5_.length + "&sstidlen=" + _loc6_.length;
         send(_loc7_);
         return _loc7_;
      }
      
      public static function sentHttpValueStat(param1:String, param2:uint = 1) : void
      {
         send("http://newmisc.taomee.com/misc.txt?type=" + param1 + "&count=" + param2);
      }
      
      public static function send(param1:String) : void
      {
         var _loc2_:URLLoader = null;
         if(_enabled)
         {
            _loc2_ = new URLLoader();
            addLoaderEvent(_loc2_);
            _loc2_.load(new URLRequest(param1));
         }
      }
      
      private static function addLoaderEvent(param1:URLLoader) : void
      {
         param1.addEventListener(SecurityErrorEvent.SECURITY_ERROR,securityErrorHandler);
         param1.addEventListener(IOErrorEvent.IO_ERROR,ioErrorHandler);
         param1.addEventListener(Event.COMPLETE,completeHandler);
      }
      
      private static function removeLoaderEvent(param1:URLLoader) : void
      {
         param1.removeEventListener(SecurityErrorEvent.SECURITY_ERROR,securityErrorHandler);
         param1.removeEventListener(IOErrorEvent.IO_ERROR,ioErrorHandler);
         param1.removeEventListener(Event.COMPLETE,completeHandler);
      }
      
      private static function securityErrorHandler(param1:SecurityErrorEvent) : void
      {
         var _loc2_:URLLoader = param1.target as URLLoader;
         removeLoaderEvent(_loc2_);
      }
      
      private static function ioErrorHandler(param1:IOErrorEvent) : void
      {
         var _loc2_:URLLoader = param1.target as URLLoader;
         removeLoaderEvent(_loc2_);
      }
      
      private static function completeHandler(param1:Event) : void
      {
         var _loc2_:URLLoader = param1.target as URLLoader;
         _loc2_.close();
         removeLoaderEvent(_loc2_);
      }
      
      public static function replaceKey(param1:String) : String
      {
         var _loc2_:String = null;
         if(param1)
         {
            for each(_loc2_ in dirtyKeyList)
            {
               if(param1.indexOf(_loc2_) >= 0)
               {
                  param1 = replaceText(param1,_loc2_,"_");
               }
            }
         }
         return param1;
      }
      
      private static function replaceText(param1:String, param2:String, param3:String) : String
      {
         while(param1.indexOf(param2) >= 0)
         {
            param1 = param1.replace(param2,param3);
         }
         return param1;
      }
   }
}

