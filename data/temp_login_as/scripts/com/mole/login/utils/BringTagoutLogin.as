package com.mole.login.utils
{
   import flash.external.*;
   import flash.net.*;
   import flash.utils.*;
   
   public class BringTagoutLogin
   {
      
      public static var requestSessionByOnline:Function;
      
      public function BringTagoutLogin()
      {
         super();
      }
      
      public static function addEvent() : void
      {
         if(!ExternalInterface.available)
         {
            return;
         }
         ExternalInterface.addCallback("getSession",requestSessionByOnline);
      }
      
      public static function get_URL_Session() : ByteArray
      {
         if(!ExternalInterface.available)
         {
            return null;
         }
         var _loc1_:String = ExternalInterface.call("get_sid");
         if(_loc1_)
         {
            return S2B(_loc1_);
         }
         return null;
      }
      
      public static function set_URL_Session(param1:ByteArray, param2:Boolean) : void
      {
         if(!ExternalInterface.available)
         {
            return;
         }
         var _loc3_:String = B2S(param1);
         ExternalInterface.call("set_sid",_loc3_,param2);
      }
      
      public static function set_game_URL_Session(param1:ByteArray) : void
      {
         var _loc2_:String = null;
         if(!ExternalInterface.available)
         {
            navigateToURL(new URLRequest("http://hero.61.com?sid=" + B2S(param1)),"_blank");
         }
         else
         {
            _loc2_ = B2S(param1);
            ExternalInterface.call("showHero",_loc2_);
         }
      }
      
      public static function jump_To_Product(param1:ByteArray, param2:String = "mole") : void
      {
         var _loc3_:String = "http://" + param2 + ".61.com?sid=" + B2S(param1);
         navigateToURL(new URLRequest(_loc3_),"_blank");
      }
      
      public static function jump_To_Xiaoba(param1:uint, param2:ByteArray, param3:String = "mole") : void
      {
         var _loc4_:String = "http://" + param3 + ".61.com?userid=" + param1 + "&gameid=9&session=" + B2S(param2);
         navigateToURL(new URLRequest(_loc4_),"_blank");
      }
      
      public static function jump_To_Recharge(param1:uint, param2:ByteArray, param3:String = "pay") : void
      {
         var _loc4_:String = "http://" + param3 + ".61.com/buy/paytype?type=cardpay&userid=" + param1 + "&gameid=1&session=" + B2S(param2);
         navigateToURL(new URLRequest(_loc4_),"_blank");
      }
      
      public static function jump_lamu_Recharge(param1:uint, param2:ByteArray, param3:String = "pay") : void
      {
         var _loc4_:String = "http://" + param3 + ".61.com/lahm/lahmPay&userid=" + param1 + "&gameid=1&session=" + B2S(param2);
         navigateToURL(new URLRequest(_loc4_),"_blank");
      }
      
      public static function jump_To_BusWeb(param1:uint, param2:uint, param3:ByteArray, param4:uint) : void
      {
         var _loc5_:String = "http://bus.61.com/sign?type=reg&uid=" + param1 + "&suid=" + param2 + "&session=" + B2S(param3) + "&invitecode=" + param4 + "&game=mole";
         navigateToURL(new URLRequest(_loc5_),"_blank");
      }
      
      public static function jump_To_BusWebForEmail(param1:uint, param2:ByteArray) : void
      {
         var _loc3_:String = "http://bus.61.com/sign/common/?uid=" + param1 + "&session=" + B2S(param2) + "&game=mole" + "&target_app=dou";
         navigateToURL(new URLRequest(_loc3_),"_blank");
      }
      
      public static function B2S(param1:ByteArray) : String
      {
         var _loc4_:String = null;
         var _loc2_:String = "";
         var _loc3_:uint = param1.position;
         param1.position = 0;
         while(param1.bytesAvailable)
         {
            _loc4_ = param1.readUnsignedByte().toString(16);
            _loc2_ += _loc4_.length == 1 ? "0" + _loc4_ : _loc4_;
         }
         param1.position = _loc3_;
         return _loc2_;
      }
      
      public static function S2B(param1:String) : ByteArray
      {
         var _loc2_:ByteArray = new ByteArray();
         var _loc3_:uint = uint(param1.length);
         if(_loc3_ == 0 || Boolean(_loc3_ % 2))
         {
            throw new Error("字符长度为" + String(_loc3_) + ",参数非偶数或为空!");
         }
         var _loc4_:uint = 0;
         while(_loc4_ < _loc3_)
         {
            _loc2_.writeByte(parseInt(param1.substr(_loc4_,2),16));
            _loc4_ += 2;
         }
         _loc2_.position = 0;
         return _loc2_;
      }
   }
}

