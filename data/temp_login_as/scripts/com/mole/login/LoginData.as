package com.mole.login
{
   import flash.utils.*;
   
   public class LoginData
   {
      
      public static var userID:uint;
      
      public static var email:String;
      
      public static var pwd:String;
      
      public static var rem_id:Boolean;
      
      public static var rem_pwd:Boolean;
      
      public static var session:ByteArray;
      
      public static var createdMole:uint;
      
      public static var serverList:Array;
      
      public static var maxServerId:uint;
      
      public static var isVip:Boolean;
      
      public static var friendList:Array;
      
      public static var ip:String;
      
      public static var port:uint;
      
      public static var serverID:uint;
      
      public static var adMsg:String;
      
      public static var loginType:uint = 0;
      
      public function LoginData()
      {
         super();
      }
      
      public static function getAdByte(param1:uint = 64) : ByteArray
      {
         var _loc3_:String = null;
         var _loc2_:ByteArray = new ByteArray();
         _loc2_.length = param1;
         if(adMsg)
         {
            _loc2_.writeUTFBytes(adMsg);
         }
         else
         {
            _loc2_.writeUTFBytes("0");
         }
         return _loc2_;
      }
   }
}

