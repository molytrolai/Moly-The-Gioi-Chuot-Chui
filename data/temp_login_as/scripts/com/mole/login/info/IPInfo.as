package com.mole.login.info
{
   public class IPInfo
   {
      
      private var _ip:String;
      
      private var _port:uint;
      
      public function IPInfo(param1:XML)
      {
         super();
         this._ip = param1.@ip;
         this._port = param1.@port;
      }
      
      public function get ip() : String
      {
         return this._ip;
      }
      
      public function get port() : uint
      {
         return this._port;
      }
   }
}

