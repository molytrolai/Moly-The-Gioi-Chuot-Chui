package com.mole.login.utils
{
   import com.adobe.crypto.*;
   import flash.utils.*;
   
   public class LoginUtil
   {
      
      public function LoginUtil()
      {
         super();
      }
      
      public static function changeRemenberedPwdPos(param1:String) : String
      {
         var _loc3_:String = null;
         var _loc4_:String = null;
         var _loc5_:String = null;
         var _loc6_:String = null;
         var _loc7_:String = null;
         var _loc2_:String = param1;
         if(_loc2_)
         {
            if(_loc2_.length == 32)
            {
               _loc3_ = _loc2_;
               _loc4_ = _loc3_.slice(0,8);
               _loc5_ = _loc3_.slice(8,16);
               _loc6_ = _loc3_.slice(16,24);
               _loc7_ = _loc3_.slice(24,32);
               _loc2_ = "";
               _loc2_ = _loc5_.concat(_loc4_,_loc7_,_loc6_);
            }
         }
         return _loc2_;
      }
      
      public static function upsetPwd(param1:String) : String
      {
         var _loc2_:String = null;
         var _loc3_:String = null;
         var _loc4_:String = null;
         var _loc5_:String = null;
         var _loc6_:String = null;
         if(param1.length != 32)
         {
            _loc2_ = MD5.hash(MD5.hash(param1));
            _loc3_ = _loc2_.slice(0,8);
            _loc4_ = _loc2_.slice(8,16);
            _loc5_ = _loc2_.slice(16,24);
            _loc6_ = _loc2_.slice(24,32);
            param1 = "";
            param1 = _loc4_.concat(_loc3_,_loc6_,_loc5_);
         }
         return param1;
      }
      
      public static function FillString(param1:String, param2:int) : ByteArray
      {
         var _loc3_:int = 0;
         var _loc6_:int = 0;
         var _loc4_:ByteArray = new ByteArray();
         var _loc5_:int = 0;
         _loc4_.writeUTFBytes(param1);
         _loc3_ = int(_loc4_.length);
         if(_loc3_ < param2)
         {
            _loc6_ = _loc3_;
            while(_loc6_ < param2)
            {
               _loc4_.writeByte(_loc5_);
               _loc6_++;
            }
            return _loc4_;
         }
         return _loc4_;
      }
      
      public static function get loginSession() : Object
      {
         var _loc2_:Object = null;
         var _loc3_:ByteArray = null;
         var _loc1_:ByteArray = BringTagoutLogin.get_URL_Session();
         if(_loc1_)
         {
            _loc2_ = new Object();
            _loc1_.position = 0;
            _loc2_.userID = _loc1_.readUnsignedInt();
            _loc3_ = new ByteArray();
            _loc1_.readBytes(_loc3_);
            _loc2_.session = _loc3_;
            return _loc2_;
         }
         return null;
      }
   }
}

