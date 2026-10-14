package com.mole.login
{
   import flash.net.URLRequest;
   
   public class VersionManager
   {
      
      private static var _o:Object;
      
      public function VersionManager()
      {
         super();
      }
      
      public static function setup(param1:Object) : void
      {
         _o = param1;
      }
      
      public static function get versionTime() : Number
      {
         return (_o.getInstance().lastModifiedDate as Date).time * 0.001;
      }
      
      public static function get version() : String
      {
         return getVersionView(_o.getInstance().lastModifiedDate as Date);
      }
      
      private static function getVersionView(param1:Date) : String
      {
         return param1.fullYear + "." + (param1.month + 1) + "." + param1.date + " " + param1.hours + ":" + param1.minutes + ":" + param1.seconds + " " + (param1.hours >= 12 ? "PM" : "AM");
      }
      
      public static function getURL(param1:String) : String
      {
         return _o.getVerURLByNameSpace(param1) as String;
      }
      
      public static function getURLRequest(param1:String) : URLRequest
      {
         return _o.getInstance().getURLRequest(param1);
      }
      
      public static function getFileSize(param1:String) : uint
      {
         return 1;
      }
   }
}

